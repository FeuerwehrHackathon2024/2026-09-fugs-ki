import { useCallback, useEffect, useRef, useState } from "react";
import { useDropzone } from "react-dropzone";
import { cn } from "@/lib/utils";

// ── Types ─────────────────────────────────────────────────────────────────────

type Document = { name: string; chunks: number; pages: number };
type SearchResult = { source: string; page: number | null; score: number; text: string };
type ServiceStatus = { name: string; ok: boolean; latency?: number };
type PreviewChunk = { text: string; page: number; enabled: boolean };
type PreviewState = { sessionId: string; filename: string; chunks: PreviewChunk[] };

type Tab = "documents" | "search" | "status";

// ── Sub-components ────────────────────────────────────────────────────────────

function TabBar({ active, onChange }: { active: Tab; onChange: (t: Tab) => void }) {
  const tabs: { id: Tab; label: string }[] = [
    { id: "documents", label: "Dokumente" },
    { id: "search", label: "Suche" },
    { id: "status", label: "Status" },
  ];
  return (
    <div className="flex border-b border-[var(--color-border)]">
      {tabs.map((t) => (
        <button
          key={t.id}
          type="button"
          onClick={() => onChange(t.id)}
          className={cn(
            "px-5 py-3 text-sm font-medium transition-colors border-b-2 -mb-px",
            active === t.id
              ? "border-[var(--color-accent)] text-[var(--color-accent)]"
              : "border-transparent text-[var(--color-text-muted)] hover:text-[var(--color-text)]",
          )}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
}

// ── Documents Tab ─────────────────────────────────────────────────────────────

function DocumentsTab() {
  const [docs, setDocs] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [previewing, setPreviewing] = useState(false);
  const [ingesting, setIngesting] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [deleteTarget, setDeleteTarget] = useState<string | null>(null);
  const [preview, setPreview] = useState<PreviewState | null>(null);

  const fetchDocs = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/documents");
      if (res.ok) setDocs(await res.json());
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDocs();
  }, [fetchDocs]);

  const onDrop = useCallback(async (accepted: File[]) => {
    const file = accepted[0];
    if (!file) return;
    setPreviewing(true);
    setStatusMessage(`PDF wird gelesen...`);
    setPreview(null);

    const body = new FormData();
    body.append("file", file);

    console.log("[preview] sending request for", file.name, file.size, "bytes");
    try {
      setStatusMessage(`PDF wird analysiert (${(file.size / 1024).toFixed(0)} KB)...`);
      const res = await fetch("/api/preview", { method: "POST", body });
      console.log("[preview] response status:", res.status);
      const data = await res.json();
      console.log("[preview] response data:", data);
      if (res.ok) {
        setPreview({
          sessionId: data.sessionId,
          filename: data.filename,
          chunks: data.chunks.map((c: { text: string; page: number }) => ({
            ...c,
            enabled: true,
          })),
        });
        setStatusMessage("");
      } else {
        setStatusMessage(`Fehler: ${data.error}`);
      }
    } catch (e) {
      console.error("[preview] fetch error:", e);
      setStatusMessage(`Fehler: ${e instanceof Error ? e.message : "Unbekannt"}`);
    } finally {
      setPreviewing(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    multiple: false,
    disabled: previewing || ingesting || preview !== null,
  });

  const toggleChunk = (index: number) => {
    setPreview((p) => {
      if (!p) return p;
      const chunks = p.chunks.map((c, i) => (i === index ? { ...c, enabled: !c.enabled } : c));
      return { ...p, chunks };
    });
  };

  const toggleAll = (enabled: boolean) => {
    setPreview((p) => {
      if (!p) return p;
      return { ...p, chunks: p.chunks.map((c) => ({ ...c, enabled })) };
    });
  };

  const handleIngest = async () => {
    if (!preview) return;
    setIngesting(true);
    setStatusMessage("Speichere ausgewählte Chunks...");

    const keep = preview.chunks
      .map((c, i) => (c.enabled ? i : -1))
      .filter((i) => i !== -1);

    try {
      const res = await fetch("/api/ingest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId: preview.sessionId, keep }),
      });
      const data = await res.json();
      if (res.ok) {
        setStatusMessage(`Fertig: ${data.chunks} Chunks indiziert.`);
        setPreview(null);
        await fetchDocs();
        setTimeout(() => setStatusMessage(""), 4000);
      } else {
        setStatusMessage(`Fehler: ${data.error}`);
      }
    } catch (e) {
      setStatusMessage(`Fehler: ${e instanceof Error ? e.message : "Unbekannt"}`);
    } finally {
      setIngesting(false);
    }
  };

  const handleDelete = async (name: string) => {
    try {
      await fetch(`/api/documents/${encodeURIComponent(name)}`, { method: "DELETE" });
      setDeleteTarget(null);
      await fetchDocs();
    } catch {
      // noop
    }
  };

  const enabledCount = preview?.chunks.filter((c) => c.enabled).length ?? 0;

  return (
    <div className="flex flex-col gap-6">
      {/* Upload / Preview */}
      <section>
        <h2 className="mb-3 text-sm font-semibold text-[var(--color-text-muted)] uppercase tracking-wide">
          Dokument hinzufügen
        </h2>

        {!preview ? (
          <div
            {...getRootProps()}
            className={cn(
              "flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-8 py-10 text-center transition-colors",
              isDragActive
                ? "border-[var(--color-accent)] bg-[var(--color-accent-soft)]"
                : "border-[var(--color-border)] bg-[var(--color-surface-alt)] hover:border-[var(--color-accent)]/50",
              (previewing || ingesting) && "cursor-not-allowed opacity-60",
            )}
          >
            <input {...getInputProps()} />
            <svg
              width="32"
              height="32"
              viewBox="0 0 24 24"
              fill="none"
              stroke="var(--color-accent)"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="mb-3"
              aria-hidden="true"
            >
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
            <p className="text-sm font-medium text-[var(--color-text)]">
              {isDragActive ? "PDF hier ablegen" : "PDF hierher ziehen oder klicken"}
            </p>
            <p className="mt-1 text-xs text-[var(--color-text-muted)]">Nur PDF-Dateien</p>
          </div>
        ) : (
          <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-alt)] overflow-hidden">
            {/* Preview header */}
            <div className="flex items-center justify-between gap-3 px-4 py-3 border-b border-[var(--color-border)] bg-white">
              <div>
                <p className="text-sm font-medium text-[var(--color-text)]">{preview.filename}</p>
                <p className="text-xs text-[var(--color-text-muted)]">
                  {enabledCount} von {preview.chunks.length} Chunks ausgewählt
                </p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => toggleAll(true)}
                  className="text-xs text-[var(--color-accent)] hover:underline"
                >
                  Alle
                </button>
                <span className="text-xs text-[var(--color-text-muted)]">·</span>
                <button
                  type="button"
                  onClick={() => toggleAll(false)}
                  className="text-xs text-[var(--color-text-muted)] hover:underline"
                >
                  Keine
                </button>
                <button
                  type="button"
                  onClick={() => { setPreview(null); setStatusMessage(""); }}
                  className="ml-2 text-xs text-[var(--color-text-muted)] hover:text-red-600"
                >
                  Abbrechen
                </button>
                <button
                  type="button"
                  onClick={handleIngest}
                  disabled={ingesting || enabledCount === 0}
                  className="ml-1 rounded-lg bg-[var(--color-accent)] px-4 py-1.5 text-xs font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
                >
                  {ingesting ? "Speichere..." : `${enabledCount} Chunks speichern`}
                </button>
              </div>
            </div>

            {/* Chunk list */}
            <div className="max-h-96 overflow-y-auto divide-y divide-[var(--color-border)]">
              {preview.chunks.map((chunk, i) => (
                <label
                  key={`chunk-${i}`}
                  className={cn(
                    "flex gap-3 px-4 py-3 cursor-pointer transition-colors",
                    chunk.enabled ? "bg-white" : "bg-[var(--color-surface-alt)] opacity-50",
                  )}
                >
                  <input
                    type="checkbox"
                    checked={chunk.enabled}
                    onChange={() => toggleChunk(i)}
                    className="mt-0.5 flex-shrink-0 accent-[var(--color-accent)]"
                  />
                  <div className="min-w-0">
                    <p className="text-xs text-[var(--color-text-muted)] mb-1">
                      Seite {chunk.page} · Chunk {i + 1}
                    </p>
                    <p className="text-xs text-[var(--color-text)] leading-relaxed line-clamp-3">
                      {chunk.text}
                    </p>
                  </div>
                </label>
              ))}
            </div>
          </div>
        )}

        {statusMessage && (
          <div className="mt-3 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-alt)] px-4 py-3">
            <p className="text-xs text-[var(--color-text-muted)]">{statusMessage}</p>
          </div>
        )}
      </section>

      {/* Documents list */}
      <section>
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-[var(--color-text-muted)] uppercase tracking-wide">
            Indizierte Dokumente
          </h2>
          <button
            type="button"
            onClick={fetchDocs}
            className="text-xs text-[var(--color-accent)] hover:underline"
          >
            Aktualisieren
          </button>
        </div>

        {loading ? (
          <div className="py-8 text-center text-sm text-[var(--color-text-muted)]">Lade...</div>
        ) : docs.length === 0 ? (
          <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-alt)] py-10 text-center">
            <p className="text-sm text-[var(--color-text-muted)]">Noch keine Dokumente indiziert.</p>
          </div>
        ) : (
          <div className="overflow-hidden rounded-xl border border-[var(--color-border)]">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-[var(--color-border)] bg-[var(--color-surface-alt)]">
                  <th className="px-4 py-3 text-left font-medium text-[var(--color-text-muted)]">
                    Dokument
                  </th>
                  <th className="px-4 py-3 text-right font-medium text-[var(--color-text-muted)]">
                    Chunks
                  </th>
                  <th className="px-4 py-3 text-right font-medium text-[var(--color-text-muted)]">
                    Seiten
                  </th>
                  <th className="px-4 py-3" />
                </tr>
              </thead>
              <tbody>
                {docs.map((doc, i) => (
                  <tr
                    key={doc.name}
                    className={cn(
                      "border-b border-[var(--color-border)] last:border-0",
                      i % 2 === 0 ? "bg-white" : "bg-[var(--color-surface)]",
                    )}
                  >
                    <td className="px-4 py-3 font-medium text-[var(--color-text)]">{doc.name}</td>
                    <td className="px-4 py-3 text-right tabular-nums text-[var(--color-text-muted)]">
                      {doc.chunks}
                    </td>
                    <td className="px-4 py-3 text-right tabular-nums text-[var(--color-text-muted)]">
                      {doc.pages}
                    </td>
                    <td className="px-4 py-3 text-right">
                      {deleteTarget === doc.name ? (
                        <span className="inline-flex items-center gap-2">
                          <button
                            type="button"
                            onClick={() => handleDelete(doc.name)}
                            className="text-xs font-medium text-red-600 hover:underline"
                          >
                            Bestätigen
                          </button>
                          <button
                            type="button"
                            onClick={() => setDeleteTarget(null)}
                            className="text-xs text-[var(--color-text-muted)] hover:underline"
                          >
                            Abbrechen
                          </button>
                        </span>
                      ) : (
                        <button
                          type="button"
                          onClick={() => setDeleteTarget(doc.name)}
                          className="text-xs text-[var(--color-text-muted)] hover:text-red-600 transition-colors"
                        >
                          Löschen
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

// ── Search Tab ────────────────────────────────────────────────────────────────

function SearchTab({ docs }: { docs: Document[] }) {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [docFilter, setDocFilter] = useState("(alle)");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searching, setSearching] = useState(false);
  const [searched, setSearched] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setSearching(true);
    setSearched(false);
    try {
      const res = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          topK,
          document: docFilter === "(alle)" ? undefined : docFilter,
        }),
      });
      if (res.ok) setResults(await res.json());
    } finally {
      setSearching(false);
      setSearched(true);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <section>
        <div className="flex gap-3">
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            placeholder="Suchanfrage eingeben..."
            className="flex-1 rounded-lg border border-[var(--color-border)] bg-white px-4 py-2.5 text-sm outline-none focus:border-[var(--color-accent)]/50 focus:ring-2 focus:ring-[var(--color-accent)]/10"
          />
          <button
            type="button"
            onClick={handleSearch}
            disabled={searching || !query.trim()}
            className="rounded-lg bg-[var(--color-accent)] px-5 py-2.5 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            {searching ? "Suche..." : "Suchen"}
          </button>
        </div>

        <div className="mt-3 flex items-center gap-4">
          <label className="flex items-center gap-2 text-sm text-[var(--color-text-muted)]">
            Treffer:
            <input
              type="number"
              min={1}
              max={20}
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              className="w-16 rounded border border-[var(--color-border)] px-2 py-1 text-sm text-center"
            />
          </label>
          <label className="flex items-center gap-2 text-sm text-[var(--color-text-muted)]">
            Dokument:
            <select
              value={docFilter}
              onChange={(e) => setDocFilter(e.target.value)}
              className="rounded border border-[var(--color-border)] px-2 py-1 text-sm"
            >
              <option value="(alle)">(alle)</option>
              {docs.map((d) => (
                <option key={d.name} value={d.name}>
                  {d.name}
                </option>
              ))}
            </select>
          </label>
        </div>
      </section>

      {searched && results.length === 0 && (
        <p className="text-sm text-[var(--color-text-muted)]">Keine Treffer gefunden.</p>
      )}

      {results.length > 0 && (
        <div className="flex flex-col gap-3">
          {results.map((r, i) => (
            <div
              key={`${r.source}-${i}`}
              className="rounded-xl border border-[var(--color-border)] bg-white p-4"
            >
              <div className="mb-2 flex items-center justify-between gap-3">
                <span className="text-xs font-semibold text-[var(--color-accent)]">
                  Treffer {i + 1}
                </span>
                <span className="text-xs text-[var(--color-text-muted)]">
                  {r.source}
                  {r.page != null ? ` · Seite ${r.page}` : ""} · Relevanz {r.score.toFixed(3)}
                </span>
              </div>
              <p className="text-sm leading-relaxed text-[var(--color-text)]">{r.text}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ── Status Tab ────────────────────────────────────────────────────────────────

function StatusTab() {
  const [services, setServices] = useState<ServiceStatus[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const res = await fetch("/api/health");
        if (res.ok) setServices(await res.json());
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <div>
      <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-[var(--color-text-muted)]">
        Service-Status
      </h2>
      {loading ? (
        <p className="text-sm text-[var(--color-text-muted)]">Prüfe Services...</p>
      ) : (
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {services.map((s) => (
            <div
              key={s.name}
              className="flex items-center gap-3 rounded-xl border border-[var(--color-border)] bg-white px-4 py-4"
            >
              <span
                className={cn(
                  "inline-block h-2.5 w-2.5 rounded-full flex-shrink-0",
                  s.ok ? "bg-green-500" : "bg-red-500",
                )}
              />
              <div className="min-w-0">
                <p className="text-sm font-medium text-[var(--color-text)]">{s.name}</p>
                <p className="text-xs text-[var(--color-text-muted)]">
                  {s.ok
                    ? `OK${s.latency != null ? ` · ${s.latency}ms` : ""}`
                    : "Nicht erreichbar"}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export function KnowledgeHubPage() {
  const [tab, setTab] = useState<Tab>("documents");
  const [docs, setDocs] = useState<Document[]>([]);

  useEffect(() => {
    fetch("/api/documents")
      .then((r) => r.json())
      .then(setDocs)
      .catch(() => {});
  }, [tab]);

  return (
    <div className="flex flex-col h-full">
      <div className="border-b border-[var(--color-border)] bg-white px-8 py-5">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[var(--color-accent-soft)]">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="var(--color-accent)"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
            </svg>
          </div>
          <div>
            <h1 className="text-base font-semibold text-[var(--color-text)]">Knowledge Hub</h1>
            <p className="text-xs text-[var(--color-text-muted)]">
              Dokumente indizieren und durchsuchen
            </p>
          </div>
        </div>
        <div className="mt-4">
          <TabBar active={tab} onChange={setTab} />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-8">
        <div className="mx-auto max-w-4xl">
          {tab === "documents" && <DocumentsTab />}
          {tab === "search" && <SearchTab docs={docs} />}
          {tab === "status" && <StatusTab />}
        </div>
      </div>
    </div>
  );
}
