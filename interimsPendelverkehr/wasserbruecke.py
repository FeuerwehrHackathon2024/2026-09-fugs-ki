"""Wasserbrücke (Pendelverkehr) – Hauptberechnung."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import httpx

from .hydranten import Hydrant, get_hydranten
from .routing import RouteErgebnis, get_route
from .wachen_mapping import (
    Fahrzeug,
    FahrzeugMitStandort,
    FeuerwehrTyp,
    Wache,
    lade_fahrzeuge_mit_standort,
)

# ── Konstanten ──────────────────────────────────────────────────
FUELLRATE_LPM = 800
ENTLEERRATE_LPM = 1600
AUSRUECKEZEIT_BF = 1.5  # Minuten
AUSRUECKEZEIT_FF = 10.0  # Minuten
HYDRANTEN_RADIEN_M = [5000, 10000, 20000]


# ── Typen ───────────────────────────────────────────────────────
@dataclass
class FahrzeugEinsatz:
    fahrzeug: Fahrzeug
    wache: Wache
    typ: FeuerwehrTyp
    ausrueckezeit_min: float
    anfahrt_min: float
    fahrzeit_hydrant_hin_min: float
    fahrzeit_hydrant_rueck_min: float
    umlaufzeit_min: float
    abgabe_lpm: float


@dataclass
class WasserbrueckeErgebnis:
    einsatzort: dict[str, float]
    hydrant: Hydrant
    suchradius_m: int
    distanz_hydrant_m: int
    geforderte_lpm: float
    gewichtung: float
    aufbauzeit_min: float
    ausreichend: bool
    fahrzeuge: list[FahrzeugEinsatz]
    gesamt_lpm: float


@dataclass
class WasserbrueckeOptionen:
    gewichtung: float = 0.5
    ausfall: list[str] = field(default_factory=list)
    ausfall_wache: list[str] = field(default_factory=list)
    auto_ausfall: float = 0.0
    seed: int | None = None
    kein_grundschutz: bool = False


# ── Hilfsfunktionen ─────────────────────────────────────────────
def _mulberry32(seed: int):
    """Seeded PRNG (Mulberry32), identisch zur TS-Version."""
    seed = seed & 0xFFFF_FFFF

    def _next() -> float:
        nonlocal seed
        seed = (seed + 0x6D2B79F5) & 0xFFFF_FFFF
        t = ((seed ^ (seed >> 15)) * (1 | seed)) & 0xFFFF_FFFF
        t = ((t + ((t ^ (t >> 7)) * (61 | t)) & 0xFFFF_FFFF) ^ t) & 0xFFFF_FFFF
        return ((t ^ (t >> 14)) & 0xFFFF_FFFF) / 4_294_967_296

    return _next


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6_371_000
    to_rad = math.radians
    d_lat = to_rad(lat2 - lat1)
    d_lon = to_rad(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(to_rad(lat1)) * math.cos(to_rad(lat2)) * math.sin(d_lon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ── Hauptfunktion ───────────────────────────────────────────────
async def berechne_wasserbruecke(
    lat: float,
    lon: float,
    geforderte_lpm: float,
    optionen: WasserbrueckeOptionen | None = None,
) -> WasserbrueckeErgebnis:
    if optionen is None:
        optionen = WasserbrueckeOptionen()

    gewichtung = optionen.gewichtung
    ausfall_fzg = {s.strip() for s in optionen.ausfall}
    ausfall_wache = {s.strip().lower() for s in optionen.ausfall_wache}
    auto_ausfall = optionen.auto_ausfall
    kein_grundschutz = optionen.kein_grundschutz

    import random
    if optionen.seed is not None:
        rng = _mulberry32(optionen.seed)
    else:
        rng = _mulberry32(random.randint(0, 2**32 - 1))

    async with httpx.AsyncClient(timeout=60) as client:
        # 1. Nächsten Hydranten finden
        hydranten: list[Hydrant] = []
        genutzter_radius = 0

        for radius in HYDRANTEN_RADIEN_M:
            print(f"🔍 Suche Hydranten im Umkreis von {radius}m...")
            hydranten = await get_hydranten(lat, lon, radius, client=client)
            genutzter_radius = radius
            if hydranten:
                break
            print("   Keine gefunden, erhöhe Radius...")

        if not hydranten:
            raise RuntimeError(
                f"Kein Hydrant im Umkreis von {HYDRANTEN_RADIEN_M[-1]}m gefunden"
            )

        print(f"   {len(hydranten)} Hydrant(en) in {genutzter_radius}m gefunden")

        hydranten.sort(key=lambda h: _haversine(lat, lon, h.lat, h.lon))

        # 2. Routbaren Hydranten finden
        hydrant: Hydrant | None = None
        distanz_hydrant = 0.0
        route_zum_hydrant: RouteErgebnis | None = None
        route_vom_hydrant: RouteErgebnis | None = None

        for i, kandidat in enumerate(hydranten):
            dist = _haversine(lat, lon, kandidat.lat, kandidat.lon)
            print(
                f"💧 Teste Hydrant {i + 1}/{len(hydranten)}: {round(dist)}m entfernt "
                f"({kandidat.type or 'unbekannt'}, Ø {kandidat.diameter or '?'})"
            )
            try:
                route_zum_hydrant = await get_route(
                    lat, lon, kandidat.lat, kandidat.lon, client=client
                )
                route_vom_hydrant = await get_route(
                    kandidat.lat, kandidat.lon, lat, lon, client=client
                )
                hydrant = kandidat
                distanz_hydrant = dist
                break
            except RuntimeError as err:
                if "404" in str(err):
                    print("   ⚠️ Nicht routbar, versuche nächsten...")
                    continue
                raise

        if hydrant is None or route_zum_hydrant is None or route_vom_hydrant is None:
            raise RuntimeError("Kein routbarer Hydrant gefunden")

        print(f"✅ Hydrant gewählt: {round(distanz_hydrant)}m Luftlinie")
        print(
            f"   Hin: {route_zum_hydrant.dauer_min:.1f} min "
            f"({round(route_zum_hydrant.distanz_m)}m)"
        )
        print(
            f"   Rück: {route_vom_hydrant.dauer_min:.1f} min "
            f"({round(route_vom_hydrant.distanz_m)}m)"
        )

        # 3. Fahrzeuge laden
        print("🚒 Lade Fahrzeuge mit Wachen-Zuordnung...")
        alle_fahrzeuge = lade_fahrzeuge_mit_standort()

        if ausfall_fzg:
            alle_fahrzeuge = [
                f for f in alle_fahrzeuge
                if f.fahrzeug.FUNKRUFNAME_KURZ not in ausfall_fzg
            ]
        if ausfall_wache:
            alle_fahrzeuge = [
                f for f in alle_fahrzeuge
                if f.wache.name.lower() not in ausfall_wache
            ]

        bf_count = sum(1 for f in alle_fahrzeuge if f.typ == "BF")
        ff_count = sum(1 for f in alle_fahrzeuge if f.typ == "FF")
        print(
            f"   {len(alle_fahrzeuge)} Fahrzeuge zugeordnet "
            f"({bf_count} BF, {ff_count} FF)"
        )

        # Auto-Ausfall
        if auto_ausfall > 0 and alle_fahrzeuge:
            anzahl_ausfall = round(len(alle_fahrzeuge) * auto_ausfall)
            indices = list(range(len(alle_fahrzeuge)))
            for i in range(len(indices) - 1, 0, -1):
                j = int(rng() * (i + 1))
                indices[i], indices[j] = indices[j], indices[i]
            ausfall_indices = set(indices[:anzahl_ausfall])
            ausgefallen = [
                alle_fahrzeuge[i]
                for i in range(len(alle_fahrzeuge))
                if i in ausfall_indices
            ]
            alle_fahrzeuge = [
                alle_fahrzeuge[i]
                for i in range(len(alle_fahrzeuge))
                if i not in ausfall_indices
            ]
            print(
                f"   🎲 Auto-Ausfall: {anzahl_ausfall} Fahrzeuge entfernt "
                f"({round(auto_ausfall * 100)}%)"
            )
            if len(ausgefallen) <= 10:
                for f in ausgefallen:
                    print(
                        f"      ✘ {f.fahrzeug.FUNKRUFNAME_KURZ} ({f.wache.name})"
                    )

        # 4. Fahrzeuge nach Wache gruppieren
        wachen_gruppen: dict[str, list[FahrzeugMitStandort]] = {}
        for fms in alle_fahrzeuge:
            key = f"{fms.wache.lat},{fms.wache.lon}"
            wachen_gruppen.setdefault(key, []).append(fms)

        # Grundschutz
        if not kein_grundschutz:
            grundschutz_count = 0
            for key, gruppe in wachen_gruppen.items():
                if len(gruppe) <= 1:
                    continue
                gruppe.sort(
                    key=lambda f: f.fahrzeug.tankvolumen_liter or 0,
                    reverse=True,
                )
                gruppe.pop(0)  # größtes bleibt zurück
                grundschutz_count += 1
            print(
                f"   🛡️ Grundschutz: {grundschutz_count} Fahrzeuge bleiben an Wachen"
            )

        # 5. Anfahrtsrouten pro Wache berechnen
        wachen_keys = list(wachen_gruppen.keys())
        print(
            f"🗺️  Berechne Anfahrtsrouten für {len(wachen_keys)} Wachen..."
        )
        anfahrt_routen: dict[str, RouteErgebnis] = {}

        for i, key in enumerate(wachen_keys):
            wache = wachen_gruppen[key][0].wache
            try:
                route = await get_route(
                    wache.lat, wache.lon, lat, lon, client=client
                )
                anfahrt_routen[key] = route
                print(
                    f"   [{i + 1}/{len(wachen_keys)}] {wache.name}: "
                    f"{route.dauer_min:.1f} min"
                )
            except RuntimeError as err:
                print(
                    f"   [{i + 1}/{len(wachen_keys)}] {wache.name}: ⚠️ {err}"
                )

        # 6. Kennzahlen pro Fahrzeug
        kandidaten: list[FahrzeugEinsatz] = []

        for key, gruppe in wachen_gruppen.items():
            anfahrt = anfahrt_routen.get(key)
            if anfahrt is None:
                continue

            for fms in gruppe:
                tank = fms.fahrzeug.tankvolumen_liter or 0
                t_fuell = tank / FUELLRATE_LPM
                t_entleer = tank / ENTLEERRATE_LPM
                t_umlauf = (
                    t_entleer
                    + route_zum_hydrant.dauer_min
                    + t_fuell
                    + route_vom_hydrant.dauer_min
                )
                abgabe_lpm = tank / t_umlauf
                ausrueckezeit = (
                    AUSRUECKEZEIT_FF if fms.typ == "FF" else AUSRUECKEZEIT_BF
                )

                kandidaten.append(
                    FahrzeugEinsatz(
                        fahrzeug=fms.fahrzeug,
                        wache=fms.wache,
                        typ=fms.typ,
                        ausrueckezeit_min=ausrueckezeit,
                        anfahrt_min=ausrueckezeit + anfahrt.dauer_min,
                        fahrzeit_hydrant_hin_min=route_zum_hydrant.dauer_min,
                        fahrzeit_hydrant_rueck_min=route_vom_hydrant.dauer_min,
                        umlaufzeit_min=round(t_umlauf * 10) / 10,
                        abgabe_lpm=round(abgabe_lpm * 10) / 10,
                    )
                )

        # 7. Greedy-Auswahl
        max_anfahrt = max((k.anfahrt_min for k in kandidaten), default=1)
        max_abgabe = max((k.abgabe_lpm for k in kandidaten), default=1)

        def sort_score(k: FahrzeugEinsatz) -> float:
            return (1 - gewichtung) * (k.anfahrt_min / max_anfahrt) + gewichtung * (
                1 - k.abgabe_lpm / max_abgabe
            )

        kandidaten.sort(key=sort_score)

        ausgewaehlt: list[FahrzeugEinsatz] = []
        gesamt_lpm = 0.0

        for k in kandidaten:
            ausgewaehlt.append(k)
            gesamt_lpm += k.abgabe_lpm
            if gesamt_lpm >= geforderte_lpm:
                break

        aufbauzeit = (
            max(f.anfahrt_min for f in ausgewaehlt) if ausgewaehlt else 0
        )

        print(
            f"\n✅ {len(ausgewaehlt)} Fahrzeuge ausgewählt → "
            f"{round(gesamt_lpm)} L/min (gefordert: {geforderte_lpm})"
        )

        return WasserbrueckeErgebnis(
            einsatzort={"lat": lat, "lon": lon},
            hydrant=hydrant,
            suchradius_m=genutzter_radius,
            distanz_hydrant_m=round(distanz_hydrant),
            geforderte_lpm=geforderte_lpm,
            gewichtung=gewichtung,
            aufbauzeit_min=round(aufbauzeit * 10) / 10,
            ausreichend=gesamt_lpm >= geforderte_lpm,
            fahrzeuge=ausgewaehlt,
            gesamt_lpm=round(gesamt_lpm * 10) / 10,
        )
