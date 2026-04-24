import { join } from "node:path";
import { toPublicRuntimeConfig, type RuntimeConfig } from "../config/models";
import { parseSessionCookie, createSessionCookieHeader } from "./cookies";
import { loadSession, saveSession, getSystemPrompt, setSystemPrompt } from "../db/persistence";
import { getMCPServerStatus } from "../services/mcp";

interface HttpHandlerOptions {
  runtimeConfig: RuntimeConfig;
  distDir: string;
}

export function createHttpHandler({ runtimeConfig, distDir }: HttpHandlerOptions) {
  return async function handleHttp(req: Request) {
    const url = new URL(req.url);

    if (req.method === "GET" && url.pathname === "/api/health") {
      return Response.json({ ok: true });
    }

    if (req.method === "GET" && url.pathname === "/api/mcp/status") {
      return Response.json(getMCPServerStatus());
    }

    if (req.method === "GET" && url.pathname === "/api/system-prompt") {
      return Response.json({ content: getSystemPrompt() ?? "" });
    }

    if (req.method === "PUT" && url.pathname === "/api/system-prompt") {
      const body = await req.json() as { content?: unknown };
      if (typeof body.content !== "string") {
        return Response.json({ error: "content must be a string" }, { status: 400 });
      }
      setSystemPrompt(body.content);
      return Response.json({ ok: true });
    }

    if (req.method === "GET" && url.pathname === "/api/models") {
      return Response.json(toPublicRuntimeConfig(runtimeConfig).models);
    }

    if (req.method === "GET" && url.pathname === "/api/runtime-config") {
      return Response.json(toPublicRuntimeConfig(runtimeConfig));
    }

    // Session recovery endpoint
    if (req.method === "GET" && url.pathname === "/api/session") {
      const cookieHeader = req.headers.get("cookie");
      const sessionId = parseSessionCookie(cookieHeader ?? undefined);
      
      if (sessionId) {
        const session = loadSession(sessionId);
        if (session) {
          return Response.json({ session, recovered: true });
        }
      }
      
      return Response.json({ recovered: false }, { status: 404 });
    }

    // Chat history endpoint
    if (req.method === "GET" && url.pathname === "/api/session/chats") {
      const cookieHeader = req.headers.get("cookie");
      const sessionId = parseSessionCookie(cookieHeader ?? undefined);
      
      if (!sessionId) {
        return Response.json({ error: "No session" }, { status: 401 });
      }
      
      const session = loadSession(sessionId);
      if (!session) {
        return Response.json({ error: "Session not found" }, { status: 404 });
      }
      
      // Return chat summaries (for history list)
      const chatSummaries = session.chats.map((chat) => ({
        id: chat.id,
        title: chat.title,
        messageCount: chat.messages.length,
        createdAt: chat.createdAt,
        updatedAt: chat.updatedAt,
      }));
      
      return Response.json({ chats: chatSummaries });
    }

    if (process.env.NODE_ENV === "production") {
      const filePath = join(distDir, url.pathname === "/" ? "index.html" : url.pathname);
      const file = Bun.file(filePath);
      if (await file.exists()) {
        return new Response(file);
      }
      return new Response(Bun.file(join(distDir, "index.html")));
    }

    return new Response("Not Found", { status: 404 });
  };
}
