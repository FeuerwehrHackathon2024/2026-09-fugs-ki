import { join } from "node:path";
import * as pdfjs from "pdfjs-dist/legacy/build/pdf.mjs";
import type { TextItem } from "pdfjs-dist/types/src/display/api";

// Point to the worker file so pdfjs-dist can run it in-process (Bun/Node)
pdfjs.GlobalWorkerOptions.workerSrc = Bun.resolveSync(
  "pdfjs-dist/legacy/build/pdf.worker.mjs",
  import.meta.dir,
);

const QDRANT_URL = process.env.QDRANT_URL ?? "http://localhost:6333";
const EMBEDDING_URL = process.env.EMBEDDING_SERVICE_URL ?? "http://localhost:8001";
const AGENTV2_URL = process.env.AGENTV2_URL ?? "http://localhost:3001";
const COLLECTION = process.env.COLLECTION_NAME ?? "pdf_knowledge";
const VECTOR_DIM = 384;
const CHUNK_SIZE = 512;
const CHUNK_OVERLAP = 64;
const PORT = Number(process.env.PORT ?? 3004);
const IS_PROD = process.env.NODE_ENV === "production";

// ── PDF extraction ────────────────────────────────────────────────────────────

async function extractPages(buffer: ArrayBuffer): Promise<{ page: number; text: string }[]> {
  const pdf = await pdfjs.getDocument({ data: new Uint8Array(buffer) }).promise;
  const pages: { page: number; text: string }[] = [];
  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    const text = content.items
      .filter((item): item is TextItem => "str" in item)
      .map((item) => item.str)
      .join(" ")
      .replace(/\s+/g, " ")
      .trim();
    if (text) pages.push({ page: i, text });
  }
  return pages;
}

// ── Chunking ──────────────────────────────────────────────────────────────────

function chunkText(text: string): string[] {
  const chunks: string[] = [];
  let start = 0;
  while (start < text.length) {
    let end = Math.min(start + CHUNK_SIZE, text.length);
    if (end < text.length) {
      for (const sep of ["\n\n", "\n", ". ", " "]) {
        const idx = text.lastIndexOf(sep, end);
        if (idx > start + CHUNK_OVERLAP) {
          end = idx + sep.length;
          break;
        }
      }
    }
    const chunk = text.slice(start, end).trim();
    if (chunk) chunks.push(chunk);
    if (end >= text.length) break;
    start = end - CHUNK_OVERLAP;
  }
  return chunks;
}

// ── Embedding ────────────────────────────────────────────────────────────────

async function embed(texts: string[]): Promise<number[][]> {
  const res = await fetch(`${EMBEDDING_URL}/embed`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ texts }),
    signal: AbortSignal.timeout(120_000),
  });
  if (!res.ok) throw new Error(`Embedding service error: ${res.status}`);
  // biome-ignore lint/suspicious/noExplicitAny: external API response
  return ((await res.json()) as any).embeddings as number[][];
}

// ── Qdrant helpers ────────────────────────────────────────────────────────────

async function ensureCollection() {
  const res = await fetch(`${QDRANT_URL}/collections/${COLLECTION}`);
  if (res.status === 404) {
    await fetch(`${QDRANT_URL}/collections/${COLLECTION}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        vectors: { size: VECTOR_DIM, distance: "Cosine" },
      }),
    });
  }
}

async function deleteDocumentVectors(name: string) {
  await fetch(`${QDRANT_URL}/collections/${COLLECTION}/points/delete`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      filter: { must: [{ key: "source", match: { value: name } }] },
    }),
  });
}

async function upsertPoints(
  points: { id: number; vector: number[]; payload: Record<string, unknown> }[],
) {
  await fetch(`${QDRANT_URL}/collections/${COLLECTION}/points`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ points }),
  });
}

async function scrollAll(): Promise<{ source: string; page?: number }[]> {
  const all: { source: string; page?: number }[] = [];
  let offset: string | number | null = null;
  while (true) {
    const body: Record<string, unknown> = { limit: 100, with_payload: true, with_vector: false };
    if (offset !== null) body.offset = offset;
    const res = await fetch(`${QDRANT_URL}/collections/${COLLECTION}/points/scroll`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) break;
    // biome-ignore lint/suspicious/noExplicitAny: external API response
    const data = await res.json() as any;
    for (const pt of data.result?.points ?? []) {
      all.push({ source: pt.payload?.source ?? "?", page: pt.payload?.page });
    }
    offset = data.result?.next_page_offset ?? null;
    if (offset === null) break;
  }
  return all;
}

async function searchVectors(
  vector: number[],
  topK: number,
  documentFilter?: string,
): Promise<{ source: string; page: number | null; score: number; text: string }[]> {
  const body: Record<string, unknown> = {
    vector,
    limit: topK,
    with_payload: true,
  };
  if (documentFilter) {
    body.filter = { must: [{ key: "source", match: { value: documentFilter } }] };
  }
  const res = await fetch(`${QDRANT_URL}/collections/${COLLECTION}/points/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) return [];
  // biome-ignore lint/suspicious/noExplicitAny: external API response
  const data = await res.json() as any;
  return (data.result ?? []).map(
    (hit: { payload: Record<string, unknown>; score: number }) => ({
      source: hit.payload?.source ?? "?",
      page: hit.payload?.page ?? null,
      score: Math.round(hit.score * 1000) / 1000,
      text: hit.payload?.text ?? "",
    }),
  );
}

// ── Hash helper (deterministic int ID from string) ────────────────────────────

function stableId(str: string): number {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = (Math.imul(31, h) + str.charCodeAt(i)) | 0;
  }
  return Math.abs(h);
}

// ── Preview session store ─────────────────────────────────────────────────────

type PreviewSession = { filename: string; chunks: { text: string; page: number }[] };
const previewSessions = new Map<string, PreviewSession>();

// ── Routing ───────────────────────────────────────────────────────────────────

const STATIC_DIR = join(import.meta.dir, "../dist");

Bun.serve({
  port: PORT,
  idleTimeout: 255,
  async fetch(req) {
    const url = new URL(req.url);
    const { pathname } = url;

    // CORS preflight
    if (req.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    const cors = { "Access-Control-Allow-Origin": "*" };

    // ── GET /api/health ──────────────────────────────────────────────────────
    if (pathname === "/api/health" && req.method === "GET") {
      const checks = [
        { name: "Qdrant", url: `${QDRANT_URL}/healthz` },
        { name: "Embedding Service", url: `${EMBEDDING_URL}/health` },
      ];
      const results = await Promise.all(
        checks.map(async ({ name, url }) => {
          const t0 = Date.now();
          try {
            const r = await fetch(url, { signal: AbortSignal.timeout(3000) });
            return { name, ok: r.ok, latency: Date.now() - t0 };
          } catch {
            return { name, ok: false };
          }
        }),
      );
      return Response.json(results, { headers: cors });
    }

    // ── GET /api/system-prompt ───────────────────────────────────────────────
    if (pathname === "/api/system-prompt" && req.method === "GET") {
      try {
        const res = await fetch(`${AGENTV2_URL}/api/system-prompt`, { signal: AbortSignal.timeout(5000) });
        const data = await res.json();
        return Response.json(data, { headers: cors });
      } catch (e) {
        return Response.json({ error: String(e) }, { status: 502, headers: cors });
      }
    }

    // ── PUT /api/system-prompt ───────────────────────────────────────────────
    if (pathname === "/api/system-prompt" && req.method === "PUT") {
      try {
        const body = await req.json();
        const res = await fetch(`${AGENTV2_URL}/api/system-prompt`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
          signal: AbortSignal.timeout(5000),
        });
        const data = await res.json();
        return Response.json(data, { status: res.status, headers: cors });
      } catch (e) {
        return Response.json({ error: String(e) }, { status: 502, headers: cors });
      }
    }

    // ── GET /api/documents ───────────────────────────────────────────────────
    if (pathname === "/api/documents" && req.method === "GET") {
      try {
        const points = await scrollAll();
        const map = new Map<string, { chunks: number; pages: Set<number> }>();
        for (const pt of points) {
          if (!map.has(pt.source)) map.set(pt.source, { chunks: 0, pages: new Set() });
          const entry = map.get(pt.source)!;
          entry.chunks++;
          if (pt.page != null) entry.pages.add(pt.page);
        }
        const docs = Array.from(map.entries())
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([name, info]) => ({ name, chunks: info.chunks, pages: info.pages.size }));
        return Response.json(docs, { headers: cors });
      } catch (e) {
        return Response.json({ error: String(e) }, { status: 500, headers: cors });
      }
    }

    // ── DELETE /api/documents/:name ──────────────────────────────────────────
    if (pathname.startsWith("/api/documents/") && req.method === "DELETE") {
      const name = decodeURIComponent(pathname.slice("/api/documents/".length));
      try {
        await deleteDocumentVectors(name);
        return Response.json({ ok: true }, { headers: cors });
      } catch (e) {
        return Response.json({ error: String(e) }, { status: 500, headers: cors });
      }
    }

    // ── POST /api/preview ────────────────────────────────────────────────────
    if (pathname === "/api/preview" && req.method === "POST") {
      try {
        console.log("[preview] request received");
        const form = await req.formData();
        const file = form.get("file") as File | null;
        if (!file) return Response.json({ error: "Keine Datei" }, { status: 400, headers: cors });

        console.log(`[preview] file: ${file.name}, size: ${file.size} bytes`);
        const buffer = await file.arrayBuffer();
        console.log("[preview] buffer read, starting PDF extraction...");

        const pages = await extractPages(buffer);
        console.log(`[preview] extracted ${pages.length} pages`);

        if (pages.length === 0)
          return Response.json({ error: "Kein Text in PDF gefunden" }, { status: 422, headers: cors });

        const chunks: { text: string; page: number }[] = [];
        for (const { page, text } of pages) {
          for (const chunk of chunkText(text)) {
            chunks.push({ text: chunk, page });
          }
        }
        console.log(`[preview] created ${chunks.length} chunks`);

        const sessionId = crypto.randomUUID();
        previewSessions.set(sessionId, { filename: file.name, chunks });
        setTimeout(() => previewSessions.delete(sessionId), 30 * 60 * 1000);

        console.log(`[preview] session ${sessionId} stored, responding`);
        return Response.json({ sessionId, filename: file.name, chunks }, { headers: cors });
      } catch (e) {
        console.error("[preview] error:", e);
        return Response.json({ error: String(e) }, { status: 500, headers: cors });
      }
    }

    // ── POST /api/ingest ─────────────────────────────────────────────────────
    if (pathname === "/api/ingest" && req.method === "POST") {
      try {
        // biome-ignore lint/suspicious/noExplicitAny: request body
        const { sessionId, keep } = await req.json() as any;
        const session = previewSessions.get(sessionId as string);
        if (!session)
          return Response.json(
            { error: "Session nicht gefunden oder abgelaufen" },
            { status: 404, headers: cors },
          );

        const { filename, chunks } = session;
        const selected = (keep as number[]).map((i) => chunks[i]).filter(Boolean);

        previewSessions.delete(sessionId);

        if (selected.length === 0) return Response.json({ chunks: 0 }, { headers: cors });

        console.log(`[ingest] ${filename}: ${selected.length} chunks, embedding-url=${EMBEDDING_URL}`);
        await ensureCollection();
        await deleteDocumentVectors(filename);

        const batchSize = 32;
        for (let i = 0; i < selected.length; i += batchSize) {
          const batch = selected.slice(i, i + batchSize);
          console.log(`[ingest] batch ${i / batchSize + 1}/${Math.ceil(selected.length / batchSize)}`);
          const embeddings = await embed(batch.map((c) => c.text));
          await upsertPoints(
            batch.map((chunk, j) => ({
              id: stableId(`${filename}_${i + j}`),
              vector: embeddings[j],
              payload: { source: filename, page: chunk.page, text: chunk.text },
            })),
          );
        }

        console.log(`[ingest] done: ${filename}`);
        return Response.json({ chunks: selected.length }, { headers: cors });
      } catch (e) {
        console.error("[ingest] error:", e);
        return Response.json({ error: String(e) }, { status: 500, headers: cors });
      }
    }

    // ── POST /api/search ─────────────────────────────────────────────────────
    if (pathname === "/api/search" && req.method === "POST") {
      try {
        // biome-ignore lint/suspicious/noExplicitAny: request body
        const { query, topK = 5, document: docFilter } = await req.json() as any;
        const [vector] = await embed([query]);
        const results = await searchVectors(vector, topK, docFilter);
        return Response.json(results, { headers: cors });
      } catch (e) {
        return Response.json({ error: String(e) }, { status: 500, headers: cors });
      }
    }

    // ── Static files (production) ────────────────────────────────────────────
    if (IS_PROD) {
      const filePath = join(STATIC_DIR, pathname === "/" ? "index.html" : pathname);
      const file = Bun.file(filePath);
      if (await file.exists()) return new Response(file);
      return new Response(Bun.file(join(STATIC_DIR, "index.html")));
    }

    return new Response("Not found", { status: 404 });
  },
});

console.log(`Admin UI backend running on http://localhost:${PORT}`);
