"""Find nearest DWD MOSMIX weather station for a given location.

The MOSMIX station catalogue is downloaded lazily on first use and cached
in-process. The parsed list stores id, name, lat, lon, elevation.
"""
from __future__ import annotations

import math
import threading
from typing import Any, Dict, List, Optional

import httpx
from mcp.server.fastmcp import FastMCP

CATALOG_URL = (
    "https://www.dwd.de/DE/leistungen/met_verfahren_mosmix/"
    "mosmix_stationskatalog.cfg?view=nasPublication&nn=16102"
    "&lang=en&download=true"
)
WARN_API_BASE = "https://app-prod-ws.warnwetter.de/v30/"
MISSING_VALUE = 32767

_cache_lock = threading.Lock()
_stations_cache: Optional[List[Dict[str, Any]]] = None


def _parse_lat_lon(token: str) -> Optional[float]:
    token = token.strip()
    if not token:
        return None
    try:
        return float(token)
    except ValueError:
        return None


def _load_catalog() -> List[Dict[str, Any]]:
    global _stations_cache
    with _cache_lock:
        if _stations_cache is not None:
            return _stations_cache

        with httpx.Client(timeout=30, follow_redirects=True) as client:
            resp = client.get(CATALOG_URL)
            resp.raise_for_status()
            text = resp.content.decode("utf-8", errors="replace")

        stations: List[Dict[str, Any]] = []
        for raw_line in text.splitlines():
            stripped = raw_line.strip()
            if not stripped:
                continue
            # Skip header ("ID    ICAO NAME ...") and dash separator.
            if stripped.startswith("ID "):
                continue
            if set(stripped) <= {"-", " "}:
                continue

            # Format: "ID ICAO NAME... LAT LON ELEV"
            # Trailing 3 tokens are lat, lon, elev.
            tokens = stripped.split()
            if len(tokens) < 5:
                continue
            try:
                elev = int(tokens[-1])
                lon = float(tokens[-2])
                lat = float(tokens[-3])
            except ValueError:
                continue

            station_id = tokens[0]
            icao = tokens[1] if tokens[1] != "----" else None
            name = " ".join(tokens[2:-3])

            if not station_id:
                continue

            stations.append(
                {
                    "id": station_id,
                    "icao": icao,
                    "name": name,
                    "lat": lat,
                    "lon": lon,
                    "elevation_m": elev,
                }
            )

        if not stations:
            raise RuntimeError("DWD CDC station catalog parsed to zero rows")
        _stations_cache = stations
        return stations


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dl / 2) ** 2
    )
    return 2 * r * math.asin(math.sqrt(a))


def find_nearest_dwd_station(
    lat: float,
    lon: float,
    count: int = 3,
    only_germany: bool = True,
) -> Dict[str, Any]:
    """Find the nearest DWD MOSMIX weather station(s) for a coordinate.

    Args:
        lat: Latitude in decimal degrees (WGS84).
        lon: Longitude in decimal degrees (WGS84).
        count: Number of nearest stations to return (1-10).
        only_germany: If true, restrict to stations inside the rough
            German bounding box (47-55 N, 5.5-15.5 E).

    Returns:
        Dictionary with ``query`` and ``stations`` list ordered by
        distance. Each station entry includes ``id``, ``name``, ``lat``,
        ``lon``, ``elevation_m`` and ``distance_km``. The station ``id``
        can be fed directly into ``get_weather_from_station`` (wetterdienst
        MCP) or ``get_weather_for_location``.
    """
    count = max(1, min(int(count), 10))
    stations = _load_catalog()

    candidates = stations
    if only_germany:
        candidates = [
            s
            for s in stations
            if 47.0 <= s["lat"] <= 55.5 and 5.5 <= s["lon"] <= 15.5
        ]
        if not candidates:
            candidates = stations

    ranked = sorted(
        candidates,
        key=lambda s: _haversine_km(lat, lon, s["lat"], s["lon"]),
    )[:count]

    return {
        "query": {"lat": lat, "lon": lon, "only_germany": only_germany},
        "stations": [
            {
                **s,
                "distance_km": round(
                    _haversine_km(lat, lon, s["lat"], s["lon"]), 2
                ),
            }
            for s in ranked
        ],
    }


def _fetch_station_overview(station_id: str) -> Dict[str, Any]:
    url = f"{WARN_API_BASE}stationOverviewExtended"
    with httpx.Client(timeout=20) as client:
        resp = client.get(url, params={"stationIds": station_id})
        resp.raise_for_status()
        return resp.json()


def get_weather_for_location(lat: float, lon: float) -> Dict[str, Any]:
    """Current temperature + 12h forecast for the nearest DWD station.

    Resolves the nearest MOSMIX station for the coordinate and returns the
    current temperature plus forecast for the next 12 hours from the DWD
    warnwetter ``stationOverviewExtended`` endpoint. If the closest
    station has no forecast data, falls back to the next-closest (up to
    5 stations tried).

    Args:
        lat: Latitude in decimal degrees (WGS84).
        lon: Longitude in decimal degrees (WGS84).

    Returns:
        Dict with the resolved station metadata, current temperature and
        a list of the next 12 hourly temperatures (ISO timestamps, value
        in degrees Celsius).
    """
    nearest = find_nearest_dwd_station(lat, lon, count=5)["stations"]
    if not nearest:
        raise RuntimeError("No DWD station found for coordinate")

    last_error: Optional[str] = None
    for station in nearest:
        try:
            data = _fetch_station_overview(station["id"])
        except Exception as exc:
            last_error = f"{station['id']}: {exc}"
            continue
        if not data:
            last_error = f"{station['id']}: empty response"
            continue

        station_key = next(iter(data.keys()))
        forecast = data[station_key].get("forecast1")
        if not forecast or "temperature" not in forecast:
            last_error = f"{station['id']}: no forecast1.temperature"
            continue

        start_ms = forecast["start"]
        step_ms = forecast["timeStep"]
        temps = forecast["temperature"]

        from datetime import datetime, timezone

        now_ms = datetime.now(tz=timezone.utc).timestamp() * 1000
        # Find index closest to now (but not in the far past); clamp.
        now_idx = max(0, round((now_ms - start_ms) / step_ms))
        now_idx = min(now_idx, len(temps) - 1)

        def point(idx: int) -> Dict[str, Any]:
            raw = temps[idx]
            ts = datetime.fromtimestamp(
                (start_ms + idx * step_ms) / 1000.0, tz=timezone.utc
            )
            value_c = None if raw == MISSING_VALUE else raw / 10.0
            return {
                "timestamp": ts.isoformat().replace("+00:00", "Z"),
                "temperature_c": value_c,
            }

        current = point(now_idx)
        next_12h = [
            point(i)
            for i in range(now_idx + 1, min(now_idx + 13, len(temps)))
        ]
        return {
            "station": station,
            "current": current,
            "next_12h": next_12h,
        }

    raise RuntimeError(
        f"No DWD forecast data available for coordinate (tried "
        f"{len(nearest)} nearest stations; last error: {last_error})"
    )


def register_tools(mcp: FastMCP) -> None:
    mcp.add_tool(
        find_nearest_dwd_station,
        name="find_nearest_dwd_station",
        description=(
            "Find the nearest DWD MOSMIX weather station(s) for a coordinate "
            "(lat/lon in WGS84). Call geocode_location first if you only have "
            "an address. Returns a list of stations with distances. Use the "
            "returned station id with get_weather_from_station (wetterdienst "
            "MCP) or call get_weather_for_location for a one-shot lookup."
        ),
    )
    mcp.add_tool(
        get_weather_for_location,
        name="get_weather_for_location",
        description=(
            "Get current temperature and 12h forecast for a location "
            "(lat/lon in WGS84). Resolves the nearest DWD MOSMIX station "
            "automatically. Call geocode_location first if you only have "
            "an address."
        ),
    )
