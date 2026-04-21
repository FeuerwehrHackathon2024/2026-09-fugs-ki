"""Gemeinsame Test-Fixtures.

`commandx/tools/mission.py` & Co. erzeugen beim Import einen `CIMgateClient()`,
der via Pydantic-Settings Env-Variablen lädt. Damit Tests ohne echte CIMgate-
Konfiguration laufen, setzen wir hier Dummy-Werte BEVOR die Tool-Module
importiert werden.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Damit `from tools._dates …` und `from client …` funktionieren, brauchen wir
# `commandx/` im sys.path (pytest startet im Repo-Root oder im commandx/-Ordner).
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("COMMANDX_HOST", "test.invalid")
os.environ.setdefault("COMMANDX_SECURITY_HEADER_VALUE", "dummy-token")
os.environ.setdefault("COMMANDX_BEARER_TOKEN", "dummy-bearer")
os.environ.setdefault("COMMANDX_VERIFY_SSL", "false")
