from mcp.server.fastmcp import FastMCP
from client import CIMgateClient
from tools._dates import to_utc_iso
from tools._writes import ensure_success
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("commandx")

client = CIMgateClient()

_RESOURCE_SUMMARY_FIELDS = [
    "id",
    "externalId",
    "name",
    "resourceType",
    "serviceType",
    "opta",
    "radioCall",
    "radioChannel",
    "licensePlate",
    "station",
    "homeStation",
    "isActive",
    "isDoctorResource",
    "isTransportResource",
    "monitoringId",
]


def _summarize(resource: dict) -> dict:
    return {k: resource.get(k) for k in _RESOURCE_SUMMARY_FIELDS if k in resource}


def get_resources() -> list[dict]:
    """Alle angelegten Einsatzmittel (Fahrzeuge/Kräfte), kompakte Zusammenfassung."""
    log.info("TOOL  get_resources")
    data = client.get("Resource")
    if isinstance(data, list):
        return [_summarize(r) for r in data if isinstance(r, dict)]
    return data


def get_resource(resource_id: str) -> dict:
    """Ein einzelnes Einsatzmittel anhand seiner GUID."""
    log.info("TOOL  get_resource  resource_id=%s", resource_id)
    return client.get(f"Resource/{resource_id}")


def get_resource_types() -> list[dict]:
    """Alle Einsatzmitteltypen (LF, HLF, DLK, RTW, ...)."""
    log.info("TOOL  get_resource_types")
    return client.get("resource-type")


def get_resource_positions() -> list[dict]:
    """Aktuelle GPS-Positionen aller Einsatzmittel."""
    log.info("TOOL  get_resource_positions")
    return client.get("resource-position")


def get_resource_fms_status() -> list[dict]:
    """Aktuelle FMS-Status aller Einsatzmittel (Status 1-9)."""
    log.info("TOOL  get_resource_fms_status")
    return client.get("resource-fms")


def get_radio_channels() -> list[dict]:
    """Alle konfigurierten Funkkanäle."""
    log.info("TOOL  get_radio_channels")
    return client.get("RadioChannel")


def report_ssr_detection(
    mission_resource_id: str,
    latitude: float,
    longitude: float,
    detection_datetime: str | None = None,
    person_index: int = 0,
) -> dict:
    """Meldet eine SSR-Detektion (Suchhund/USAR-Sensor) für ein Einsatzmittel.

    SSR (Search and Rescue Sensor) übermittelt GPS-Position + Personenindex
    wenn ein Sensor einen Fund meldet.

    Args:
        mission_resource_id: GUID des Einsatzmittels (im Einsatz zugewiesen)
        latitude:            Breitengrad der Detektion (WGS-84)
        longitude:           Längengrad der Detektion (WGS-84)
        detection_datetime:  ISO-8601-Zeitstempel oder None/"now" für jetzt
        person_index:        Index der detektierten Person (0 = erster Fund)
    """
    log.info("TOOL  report_ssr_detection  resource=%s lat=%s lon=%s", mission_resource_id, latitude, longitude)
    ts = to_utc_iso(detection_datetime) or to_utc_iso("now")
    return ensure_success(
        client.post("ssr/detection", json={
            "missionResourceId": mission_resource_id,
            "detectionDateTime": ts,
            "latitude": latitude,
            "longitude": longitude,
            "personIndex": person_index,
        }),
        label="report_ssr_detection",
    )


def register_resource_tools(mcp: FastMCP) -> None:
    mcp.add_tool(
        get_resources,
        name="get_resources",
        description="""Gibt alle angelegten Einsatzmittel (Fahrzeuge/Kräfte) kompakt zurück
    (Name, Typ, Funkrufname, Standort, Kennzeichen, MonitoringID).
    Für Details zu einem bestimmten Einsatzmittel `get_resource` verwenden.""",
    )
    mcp.add_tool(
        get_resource,
        name="get_resource",
        description="""Gibt ein Einsatzmittel anhand seiner GUID mit allen Details zurück.

    Args:
        resource_id: GUID des Einsatzmittels""",
    )
    mcp.add_tool(
        get_resource_types,
        name="get_resource_types",
        description="""Gibt alle Einsatzmitteltypen (LF, HLF, DLK, RTW ...) inklusive
    Soll-Besatzung (ResourceLeader/GroupLeader/Staff) zurück.""",
    )
    mcp.add_tool(
        get_resource_positions,
        name="get_resource_positions",
        description="""Gibt die aktuellen GPS-Positionen aller Einsatzmittel zurück
    (Latitude, Longitude, Adresse, Zeitstempel). Nützlich für Lagekarten.""",
    )
    mcp.add_tool(
        get_resource_fms_status,
        name="get_resource_fms_status",
        description="""Gibt den aktuellen FMS-Status aller Einsatzmittel zurück
    (Status 1=Einsatzbereit Wache, 2=Einsatzbereit Funk, 3=Anfahrt, 4=Einsatzstelle,
    5=Sprechwunsch, 6=Nicht einsatzbereit, usw.).""",
    )
    mcp.add_tool(
        get_radio_channels,
        name="get_radio_channels",
        description="Gibt alle konfigurierten Funkkanäle zurück (Name, Gruppe, Typ).",
    )
    mcp.add_tool(
        report_ssr_detection,
        name="report_ssr_detection",
        description="""Meldet eine SSR-Detektion (USAR-Sensor / Suchhund) für ein Einsatzmittel.

        Übermittelt GPS-Koordinaten und optionalen Personenindex wenn ein
        Suchhund- oder USAR-Sensor einen Fund meldet.

        Args:
            mission_resource_id: GUID des Einsatzmittels (im Einsatz zugewiesen)
            latitude:            Breitengrad WGS-84
            longitude:           Längengrad WGS-84
            detection_datetime:  ISO-8601 mit TZ oder None/"now" für jetzt
            person_index:        Index der detektierten Person (Standard 0)""",
    )
