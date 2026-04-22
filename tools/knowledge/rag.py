import os

import httpx
from mcp.server.fastmcp import FastMCP
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
EMBEDDING_URL = os.getenv("EMBEDDING_SERVICE_URL", "http://localhost:8001")
COLLECTION = os.getenv("COLLECTION_NAME", "pdf_knowledge")
TOP_K_DEFAULT = 5

_qdrant: QdrantClient | None = None


def get_qdrant() -> QdrantClient:
    global _qdrant
    if _qdrant is None:
        _qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    return _qdrant


async def _embed(text: str) -> list[float]:
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(f"{EMBEDDING_URL}/embed", json={"texts": [text]})
        resp.raise_for_status()
        return resp.json()["embeddings"][0]


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool(
        name="query_knowledge",
        description=(
            "Durchsucht die Wissensbasis nach relevanten Informationen zu einer Frage. "
            "Gibt die passendsten Textabschnitte aus indizierten Dokumenten zurück."
        ),
    )
    async def query_knowledge(
        question: str,
        document: str | None = None,
        top_k: int = TOP_K_DEFAULT,
    ) -> str:
        try:
            vector = await _embed(question)
        except Exception as e:
            return f"Fehler beim Embedding: {e}"

        query_filter = None
        if document:
            query_filter = Filter(
                must=[FieldCondition(key="source", match=MatchValue(value=document))]
            )

        try:
            results = get_qdrant().query_points(
                collection_name=COLLECTION,
                query=vector,
                query_filter=query_filter,
                limit=top_k,
                with_payload=True,
            ).points
        except Exception as e:
            return f"Fehler bei der Datenbankabfrage: {e}"

        if not results:
            return "Keine relevanten Informationen gefunden."

        parts = []
        for i, hit in enumerate(results, 1):
            payload = hit.payload or {}
            source = payload.get("source", "Unbekannt")
            page = payload.get("page", "?")
            text = payload.get("text", "")
            score = round(hit.score, 3)
            parts.append(
                f"**Treffer {i}** | Quelle: {source} | Seite: {page} | Relevanz: {score}\n\n{text}"
            )

        return "\n\n---\n\n".join(parts)

    @mcp.tool(
        name="list_knowledge_documents",
        description="Listet alle indizierten Dokumente in der Wissensbasis auf.",
    )
    def list_knowledge_documents() -> str:
        try:
            sources: dict[str, dict] = {}
            offset = None
            while True:
                records, offset = get_qdrant().scroll(
                    collection_name=COLLECTION,
                    limit=100,
                    offset=offset,
                    with_payload=True,
                    with_vectors=False,
                )
                for record in records:
                    payload = record.payload or {}
                    src = payload.get("source", "Unbekannt")
                    if src not in sources:
                        sources[src] = {"chunks": 0, "pages": set()}
                    sources[src]["chunks"] += 1
                    page = payload.get("page")
                    if page is not None:
                        sources[src]["pages"].add(page)
                if offset is None:
                    break

            if not sources:
                return "Keine Dokumente in der Wissensbasis."

            lines = ["**Indizierte Dokumente:**\n"]
            for name, info in sorted(sources.items()):
                page_count = len(info["pages"])
                lines.append(f"- **{name}** — {info['chunks']} Chunks, {page_count} Seiten")

            return "\n".join(lines)
        except Exception as e:
            return f"Fehler beim Laden der Dokumente: {e}"
