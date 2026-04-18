"""CLI für Wasserbrücke-Berechnung.

Verwendung:
  python -m python --lat 48.1374 --lon 11.5755 --lpm 800
"""

from __future__ import annotations

import argparse
import asyncio
import sys

from .simulation import ZeitverlaufErgebnis, berechne_zeitverlauf
from .wasserbruecke import WasserbrueckeOptionen, berechne_wasserbruecke


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Wasserbrücke (Pendelverkehr) berechnen")
    p.add_argument("--lat", type=float, required=True, help="Breitengrad")
    p.add_argument("--lon", type=float, required=True, help="Längengrad")
    p.add_argument("--lpm", type=float, required=True, help="Geforderte L/min")
    p.add_argument(
        "-g", "--gewichtung", type=float, default=0.5,
        help="0 = schnellste Anfahrt, 1 = wenigste Fahrzeuge (Standard: 0.5)",
    )
    p.add_argument(
        "-d", "--dauer", type=int, default=0,
        help="Zeitverlauf-Dauer in Minuten (Standard: automatisch)",
    )
    p.add_argument(
        "--ausfall", type=str, default="",
        help='Fahrzeuge ausschließen (kommagetrennt, z.B. "HLF 1/1,TLF 5/1")',
    )
    p.add_argument(
        "--ausfall-wache", type=str, default="",
        help='Ganze Wachen ausschließen (z.B. "Feuerwache 3")',
    )
    p.add_argument(
        "--auto-ausfall", type=float, default=0.0,
        help="Anteil zufällig ausfallender Fahrzeuge, 0-1 (z.B. 0.3)",
    )
    p.add_argument("--seed", type=int, default=None, help="Seed für Zufall")
    p.add_argument(
        "--kein-grundschutz", action="store_true",
        help="Grundschutz deaktivieren",
    )
    return p.parse_args()


def render_timeline(sim: ZeitverlaufErgebnis) -> None:
    BAR_WIDTH = 40
    max_puffer = sim.max_puffer_liter or 1

    print("\n⏱️  WASSER-ZEITVERLAUF (Puffer am Einsatzort)")
    print("═" * 100)
    print(
        " Min │ "
        + "Puffer".ljust(BAR_WIDTH)
        + " │ "
        + "Liter".rjust(8)
        + " │ Ereignisse"
    )
    print("─────┼─" + "─" * BAR_WIDTH + "─┼─" + "─" * 8 + "─┼" + "─" * 40)

    for s in sim.schritte:
        bar_len = round((s.puffer_liter / max_puffer) * BAR_WIDTH)
        bar = "░" * BAR_WIDTH if s.engpass else "█" * bar_len
        marker = " ⚠️" if s.engpass else ""
        events = "  ".join(s.ereignisse)
        print(
            f"{str(s.zeit_min).rjust(4)}' │ "
            f"{bar.ljust(BAR_WIDTH)} │ "
            f"{f'{s.puffer_liter} L'.rjust(8)}"
            f"{marker} │ {events}"
        )

    print("─────┴─" + "─" * BAR_WIDTH + "─┴─" + "─" * 8 + "─┴" + "─" * 40)

    if sim.erster_engpass_min is not None:
        print(
            f"\n⚠️  Erster Engpass bei Minute {sim.erster_engpass_min} — Puffer = 0 L"
        )
    else:
        print("\n✅ Kein Engpass — durchgehende Wasserversorgung")
    print(f"📊 Max. Puffer: {sim.max_puffer_liter} L")
    last = sim.schritte[-1] if sim.schritte else None
    print(
        f"💧 Gesamt geliefert: {last.geliefert_liter if last else 0} L"
        f" │ Verbraucht: {last.verbraucht_liter if last else 0} L"
        f" │ Dauer: {sim.dauer_min} min"
    )


async def main() -> None:
    args = parse_args()

    if args.gewichtung < 0 or args.gewichtung > 1:
        print("Fehler: Gewichtung muss zwischen 0 und 1 liegen.")
        sys.exit(1)

    ausfall = [s.strip() for s in args.ausfall.split(",") if s.strip()]
    ausfall_wache = [
        s.strip() for s in args.ausfall_wache.split(",") if s.strip()
    ]

    optionen = WasserbrueckeOptionen(
        gewichtung=args.gewichtung,
        ausfall=ausfall,
        ausfall_wache=ausfall_wache,
        auto_ausfall=args.auto_ausfall,
        seed=args.seed,
        kein_grundschutz=args.kein_grundschutz,
    )

    ergebnis = await berechne_wasserbruecke(args.lat, args.lon, args.lpm, optionen)

    print("\n═══════════════════════════════════════════════")
    print("📊 ERGEBNIS WASSERBRÜCKE")
    print("═══════════════════════════════════════════════")
    print(f"Einsatzort:  {ergebnis.einsatzort['lat']}, {ergebnis.einsatzort['lon']}")
    print(
        f"Hydrant:     {ergebnis.distanz_hydrant_m}m entfernt "
        f"(Suchradius: {ergebnis.suchradius_m}m, "
        f"{ergebnis.hydrant.type or '?'}, Ø {ergebnis.hydrant.diameter or '?'})"
    )
    print(f"Gefordert:   {ergebnis.geforderte_lpm} L/min")
    print(f"Gewichtung:  {ergebnis.gewichtung} (0=Anfahrt, 1=Effizienz)")
    print(f"Geliefert:   {ergebnis.gesamt_lpm} L/min")
    print(f"Ausreichend: {'✅ Ja' if ergebnis.ausreichend else '❌ Nein'}")
    print(f"Aufbauzeit:  {ergebnis.aufbauzeit_min} min")
    print(f"\n🚒 Eingesetzte Fahrzeuge ({len(ergebnis.fahrzeuge)}):")
    print("─" * 115)
    print(
        "Funkrufname".ljust(18)
        + "Typ".ljust(5)
        + "Tank".rjust(7)
        + "Anfahrt".rjust(10)
        + "Umlauf".rjust(10)
        + "L/min".rjust(8)
        + "  Wache"
    )
    print("─" * 115)
    for f in ergebnis.fahrzeuge:
        print(
            f.fahrzeug.FUNKRUFNAME_KURZ.ljust(18)
            + f.typ.ljust(5)
            + f"{f.fahrzeug.tankvolumen_liter} L".rjust(7)
            + f"{f.anfahrt_min:.1f} min".rjust(10)
            + f"{f.umlaufzeit_min} min".rjust(10)
            + f"{f.abgabe_lpm}".rjust(8)
            + f"  {f.wache.name}"
        )
    print("─" * 115)

    sim = berechne_zeitverlauf(ergebnis, args.dauer)
    render_timeline(sim)


if __name__ == "__main__":
    asyncio.run(main())
