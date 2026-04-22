import { useEffect, useRef, useState } from "react";

type Status = "idle" | "loading" | "saving" | "saved" | "error";

export function SystemPromptPage() {
  const [content, setContent] = useState("");
  const [status, setStatus] = useState<Status>("loading");
  const [errorMsg, setErrorMsg] = useState("");
  const originalRef = useRef("");

  useEffect(() => {
    fetch("/api/system-prompt")
      .then((r) => r.json())
      .then((data: { content?: string; error?: string }) => {
        if (data.error) throw new Error(data.error);
        const text = data.content ?? "";
        setContent(text);
        originalRef.current = text;
        setStatus("idle");
      })
      .catch((e) => {
        setErrorMsg(String(e));
        setStatus("error");
      });
  }, []);

  async function handleSave() {
    setStatus("saving");
    setErrorMsg("");
    try {
      const res = await fetch("/api/system-prompt", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content }),
      });
      const data = await res.json() as { ok?: boolean; error?: string };
      if (!res.ok || data.error) throw new Error(data.error ?? `HTTP ${res.status}`);
      originalRef.current = content;
      setStatus("saved");
      setTimeout(() => setStatus("idle"), 2500);
    } catch (e) {
      setErrorMsg(String(e));
      setStatus("error");
    }
  }

  const isDirty = content !== originalRef.current;

  return (
    <div className="flex h-full flex-col gap-6 p-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-[var(--color-text)]">System Prompt</h1>
          <p className="mt-0.5 text-sm text-[var(--color-muted)]">
            Wird bei jedem Chat-Request an den Agenten übergeben. Änderungen wirken sofort.
          </p>
        </div>

        <div className="flex items-center gap-3">
          {status === "error" && (
            <span className="text-sm text-red-500">{errorMsg}</span>
          )}
          {status === "saved" && (
            <span className="text-sm text-green-500">Gespeichert</span>
          )}
          <button
            type="button"
            onClick={handleSave}
            disabled={!isDirty || status === "saving" || status === "loading"}
            className="rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white transition-opacity disabled:opacity-40 hover:opacity-90"
          >
            {status === "saving" ? "Speichern…" : "Speichern"}
          </button>
        </div>
      </div>

      <textarea
        value={content}
        onChange={(e) => {
          setContent(e.target.value);
          if (status === "saved") setStatus("idle");
        }}
        disabled={status === "loading"}
        spellCheck={false}
        className="flex-1 resize-none rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-2)] p-4 font-mono text-sm text-[var(--color-text)] outline-none focus:ring-1 focus:ring-[var(--color-accent)] disabled:opacity-50"
        placeholder="System Prompt wird geladen…"
      />
    </div>
  );
}
