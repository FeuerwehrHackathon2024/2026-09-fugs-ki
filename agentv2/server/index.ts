import { join } from "node:path";
import { loadRuntimeConfig } from "./config/models";
import { initializeToolRegistry } from "./config/tools";
import { createHttpHandler } from "./http/routes";
import { createWebSocketHandlers, type ConnectionState } from "./ws/connection";
import { createSession } from "./state";
import { initSystemPromptIfMissing } from "./db/persistence";

const PORT = 3001;
const distDir = join(import.meta.dir, "..", "dist");

// Seed system prompt into DB from file if not yet stored
const systemPromptPath = new URL("../system-prompt.md", import.meta.url);
const defaultSystemPrompt = await Bun.file(systemPromptPath).text();
initSystemPromptIfMissing(defaultSystemPrompt);

const runtimeConfig = loadRuntimeConfig();
await initializeToolRegistry();
const handleHttp = createHttpHandler({ runtimeConfig, distDir });
const websocket = createWebSocketHandlers(runtimeConfig);

const server = Bun.serve<ConnectionState>({
  port: PORT,
  idleTimeout: 255,
  websocket,
  async fetch(req, server) {
    const url = new URL(req.url);

    if (url.pathname === "/ws") {
      if (
        server.upgrade(req, {
          data: {
            modelId: runtimeConfig.autoConnectModelId,
            runtimeConfig,
            session: createSession(),
            status: "idle",
          },
        })
      ) {
        return;
      }
    }

    return handleHttp(req);
  },
});

console.log(`agentv2 listening on http://localhost:${server.port}`);
