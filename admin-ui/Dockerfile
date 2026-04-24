FROM oven/bun:1 AS builder

WORKDIR /app

COPY package.json bun.lock* ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun run build

FROM oven/bun:1-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY package.json bun.lock* ./
RUN bun install --frozen-lockfile --production

COPY server/ ./server/
COPY --from=builder /app/dist ./dist

ENV NODE_ENV=production PORT=3004

EXPOSE 3004

CMD ["bun", "server/index.ts"]
