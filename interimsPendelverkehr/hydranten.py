"""Hydranten aus OpenStreetMap (Overpass API) abfragen."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

import httpx

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


@dataclass
class Hydrant:
    id: int
    lat: float
    lon: float
    type: str | None = None
    diameter: str | None = None
    pressure: str | None = None
    operator: str | None = None


async def get_hydranten(
    lat: float,
    lon: float,
    radius_m: int = 500,
    *,
    client: httpx.AsyncClient | None = None,
) -> list[Hydrant]:
    """Gibt Hydranten aus OSM zurück, die im Umkreis liegen."""
    query = f"""
    [out:json][timeout:30];
    (
      node["emergency"="fire_hydrant"](around:{radius_m},{lat},{lon});
    );
    out body;
    """

    own_client = client is None
    if own_client:
        client = httpx.AsyncClient(timeout=60)

    max_retries = 3
    try:
        for attempt in range(1, max_retries + 1):
            resp = await client.post(
                OVERPASS_URL,
                data={"data": query},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            if resp.status_code == 200:
                data = resp.json()
                return [
                    Hydrant(
                        id=el["id"],
                        lat=el.get("lat") or el["center"]["lat"],
                        lon=el.get("lon") or el["center"]["lon"],
                        type=(el.get("tags") or {}).get("fire_hydrant:type"),
                        diameter=(el.get("tags") or {}).get("fire_hydrant:diameter"),
                        pressure=(el.get("tags") or {}).get("fire_hydrant:pressure"),
                        operator=(el.get("tags") or {}).get("operator"),
                    )
                    for el in data["elements"]
                ]

            if attempt < max_retries:
                print(
                    f"Versuch {attempt} fehlgeschlagen ({resp.status_code}), "
                    f"neuer Versuch in 30s..."
                )
                await asyncio.sleep(30)
            else:
                raise RuntimeError(
                    f"Overpass API Fehler nach {max_retries} Versuchen: "
                    f"{resp.status_code}"
                )
    finally:
        if own_client:
            await client.aclose()

    raise RuntimeError("Unreachable")
