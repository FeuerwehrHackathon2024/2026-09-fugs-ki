"""Fahrzeuge mit Wachen-Standorten verknüpfen."""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass
class Wache:
    name: str
    lat: float
    lon: float


FeuerwehrTyp = Literal["BF", "FF"]


@dataclass
class Fahrzeug:
    BEZEICHNUNG: str
    ORGANISATION: str
    DIENSTSTELLE: str
    FUNKRUFNAME_KURZ: str
    FUNKRUFNAME_LANG: str
    tankvolumen_liter: int | None = None
    einsatzbereit: bool | None = None


@dataclass
class FahrzeugMitStandort:
    fahrzeug: Fahrzeug
    wache: Wache
    typ: FeuerwehrTyp


def _normalize(s: str) -> str:
    s = s.lower()
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = re.sub(r"[^a-z0-9]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _finde_wache(dienststelle: str, wachen: list[Wache]) -> Wache | None:
    # BF: "Feuerwache N"
    bf_match = re.search(r"Feuerwache\s+(\d+)", dienststelle)
    if bf_match:
        nr = bf_match.group(1)
        muster = re.compile(rf"feuerwache {nr}(?!\d)")
        return next((w for w in wachen if muster.search(_normalize(w.name))), None)

    # FF: "Gerätehaus Ortsname"
    ff_match = re.search(r"Gerätehaus\s+([^(]+)", dienststelle)
    if ff_match:
        ort_norm = _normalize(ff_match.group(1))
        teile = [t for t in ort_norm.split() if len(t) > 3]
        if not teile:
            return None
        return next(
            (
                w
                for w in wachen
                if all(teil in _normalize(w.name) for teil in teile)
            ),
            None,
        )

    return None


def _bestimme_typ(dienststelle: str) -> FeuerwehrTyp:
    return "FF" if "FF-M" in dienststelle else "BF"


def _data_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "data"


def lade_fahrzeuge_mit_standort() -> list[FahrzeugMitStandort]:
    data = _data_dir()
    with open(data / "wachen.json", encoding="utf-8") as f:
        wachen = [Wache(**w) for w in json.load(f)]
    with open(data / "fahrzeuge.json", encoding="utf-8") as f:
        fahrzeuge = [Fahrzeug(**fz) for fz in json.load(f)]

    ergebnis: list[FahrzeugMitStandort] = []
    for fz in fahrzeuge:
        if not fz.tankvolumen_liter or fz.tankvolumen_liter <= 0:
            continue
        if fz.einsatzbereit is False:
            continue

        wache = _finde_wache(fz.DIENSTSTELLE, wachen)
        if wache:
            ergebnis.append(
                FahrzeugMitStandort(
                    fahrzeug=fz,
                    wache=wache,
                    typ=_bestimme_typ(fz.DIENSTSTELLE),
                )
            )

    return ergebnis
