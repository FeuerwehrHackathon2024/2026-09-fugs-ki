"""Routing über OpenRouteService."""

from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass

import httpx

ORS_BASE = "https://api.openrouteservice.org/v2/directions/driving-car"


@dataclass
class RouteErgebnis:
    dauer_min: float
    distanz_m: float


class _RateLimiter:
    def __init__(self, max_requests: int, fenster_ms: int) -> None:
        self._max_requests = max_requests
        self._fenster_ms = fenster_ms
        self._timestamps: list[float] = []

    async def warte(self) -> None:
        now = time.monotonic() * 1000
        self._timestamps = [
            t for t in self._timestamps if t > now - self._fenster_ms
        ]
        if len(self._timestamps) >= self._max_requests:
            wartezeit = (
                self._timestamps[0] + self._fenster_ms - now + 100
            )
            print(
                f"⏳ Rate-Limit erreicht, warte {int(wartezeit / 1000)}s..."
            )
            await asyncio.sleep(wartezeit / 1000)
            now_after = time.monotonic() * 1000
            self._timestamps = [
                t for t in self._timestamps if t > now_after - self._fenster_ms
            ]
        self._timestamps.append(time.monotonic() * 1000)


_limiter = _RateLimiter(38, 60_000)


async def get_route(
    von_lat: float,
    von_lon: float,
    nach_lat: float,
    nach_lon: float,
    *,
    client: httpx.AsyncClient | None = None,
) -> RouteErgebnis:
    api_key = os.environ.get("OPENROUTERKEY")
    if not api_key:
        raise RuntimeError("OPENROUTERKEY nicht in Umgebungsvariablen gesetzt")

    url = f"{ORS_BASE}?start={von_lon},{von_lat}&end={nach_lon},{nach_lat}"

    own_client = client is None
    if own_client:
        client = httpx.AsyncClient(timeout=60)

    max_retries = 5
    try:
        for versuch in range(1, max_retries + 1):
            await _limiter.warte()

            resp = await client.get(url, headers={"Authorization": api_key})

            if resp.status_code == 429:
                print(
                    f"⏳ 429 Rate-Limit von ORS, warte 60s "
                    f"(Versuch {versuch}/{max_retries})..."
                )
                await asyncio.sleep(60)
                continue

            if resp.status_code != 200:
                raise RuntimeError(
                    f"ORS Fehler {resp.status_code}: {resp.text}"
                )

            data = resp.json()
            props = data["features"][0]["properties"]
            summary = props.get("summary")

            duration = summary.get("duration") if summary else None
            distance = summary.get("distance") if summary else None

            if duration is None or distance is None:
                segments = props.get("segments", [])
                duration = sum(seg.get("duration", 0) for seg in segments)
                distance = sum(seg.get("distance", 0) for seg in segments)

            return RouteErgebnis(
                dauer_min=duration / 60,
                distanz_m=distance,
            )
    finally:
        if own_client:
            await client.aclose()

    raise RuntimeError(
        f"ORS: Rate-Limit nach {max_retries} Versuchen nicht aufgelöst"
    )
