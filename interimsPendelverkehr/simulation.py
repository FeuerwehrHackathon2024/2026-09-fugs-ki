"""Zeitverlauf-Simulation für die Wasserbrücke."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .wasserbruecke import (
    ENTLEERRATE_LPM,
    FUELLRATE_LPM,
    WasserbrueckeErgebnis,
)


@dataclass
class ZeitpunktDaten:
    zeit_min: int
    puffer_liter: int
    geliefert_liter: int
    verbraucht_liter: int
    fahrzeuge_aktiv: int
    engpass: bool
    ereignisse: list[str] = field(default_factory=list)


@dataclass
class ZeitverlaufErgebnis:
    schritte: list[ZeitpunktDaten]
    dauer_min: int
    erster_engpass_min: float | None
    max_puffer_liter: int


EventArt = Literal["ankunft", "entleert", "zurueck", "entleert_pendel"]


@dataclass
class _Event:
    zeit: float
    art: EventArt
    name: str
    tank: int


def berechne_zeitverlauf(
    ergebnis: WasserbrueckeErgebnis,
    dauer_min: int = 0,
) -> ZeitverlaufErgebnis:
    """Berechnet den exakten Wasser-Zeitverlauf am Einsatzort."""
    fahrzeuge = ergebnis.fahrzeuge
    geforderte_lpm = ergebnis.geforderte_lpm

    if dauer_min <= 0:
        max_anfahrt = max((f.anfahrt_min for f in fahrzeuge), default=0)
        dauer_min = max(30, int(max_anfahrt + 25) + 1)

    # 1. Alle Events analytisch berechnen
    events: list[_Event] = []

    for fe in fahrzeuge:
        tank = fe.fahrzeug.tankvolumen_liter or 0
        name = fe.fahrzeug.FUNKRUFNAME_KURZ
        t_entleer = tank / ENTLEERRATE_LPM
        t_pendel = (
            fe.fahrzeit_hydrant_hin_min
            + tank / FUELLRATE_LPM
            + fe.fahrzeit_hydrant_rueck_min
        )

        # Erste Ankunft
        t = fe.anfahrt_min
        events.append(_Event(zeit=t, art="ankunft", name=name, tank=tank))
        t += t_entleer
        events.append(_Event(zeit=t, art="entleert", name=name, tank=0))

        # Pendelzyklen
        while t + t_pendel <= dauer_min:
            t += t_pendel
            events.append(_Event(zeit=t, art="zurueck", name=name, tank=tank))
            t += t_entleer
            if t > dauer_min:
                break
            events.append(
                _Event(zeit=t, art="entleert_pendel", name=name, tank=0)
            )

    events.sort(key=lambda e: e.zeit)

    # 2. Puffer analytisch berechnen
    puffer = 0.0
    geliefert = 0.0
    letzte_zeit = 0.0
    entleerend = 0
    angekommen = 0
    erster_engpass: float | None = None
    max_puffer = 0.0

    def advance_to(t: float) -> None:
        nonlocal puffer, geliefert, letzte_zeit, erster_engpass, max_puffer
        dt = t - letzte_zeit
        if dt <= 0:
            return

        zufluss = ENTLEERRATE_LPM * entleerend * dt
        abfluss = geforderte_lpm * dt
        puffer_vorher = puffer
        puffer += zufluss - abfluss
        geliefert += zufluss

        if puffer < 0:
            if erster_engpass is None:
                rate = ENTLEERRATE_LPM * entleerend - geforderte_lpm
                if rate < 0 and puffer_vorher > 0:
                    erster_engpass = round(
                        (letzte_zeit + puffer_vorher / -rate) * 100
                    ) / 100
                else:
                    erster_engpass = round(t * 100) / 100
            puffer = 0

        if puffer > max_puffer:
            max_puffer = puffer
        letzte_zeit = t

    # 3. Events mit Minuten-Marken verschränken
    schritte: list[ZeitpunktDaten] = []
    naechste_minute = 0
    event_idx = 0
    pending_events: list[str] = []

    while naechste_minute <= dauer_min:
        while event_idx < len(events) and events[event_idx].zeit <= naechste_minute:
            ev = events[event_idx]
            advance_to(ev.zeit)

            if ev.art == "ankunft":
                entleerend += 1
                angekommen += 1
                pending_events.append(f"🚒 {ev.name} (+{ev.tank}L)")
            elif ev.art in ("entleert", "entleert_pendel"):
                entleerend -= 1
            elif ev.art == "zurueck":
                entleerend += 1
                pending_events.append(f"🔄 {ev.name} (+{ev.tank}L)")

            event_idx += 1

        advance_to(naechste_minute)
        schritte.append(
            ZeitpunktDaten(
                zeit_min=naechste_minute,
                puffer_liter=round(puffer),
                geliefert_liter=round(geliefert),
                verbraucht_liter=round(geforderte_lpm * naechste_minute),
                fahrzeuge_aktiv=angekommen,
                engpass=puffer <= 0 and naechste_minute > 0,
                ereignisse=list(pending_events),
            )
        )
        pending_events.clear()
        naechste_minute += 1

    return ZeitverlaufErgebnis(
        schritte=schritte,
        dauer_min=dauer_min,
        erster_engpass_min=erster_engpass,
        max_puffer_liter=round(max_puffer),
    )
