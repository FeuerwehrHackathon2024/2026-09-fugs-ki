from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP
from client import CIMgateClient
from tools._dates import to_utc_iso
from tools._writes import ensure_success, readback_from_list
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("commandx")

client = CIMgateClient()

def read_messages(mission_id: str, limit: int | None = None) -> list[dict]:
    log.info("TOOL  read_messages")
    messages = client.get(("mission/" + mission_id + "/message"))
    if limit is not None:
        messages = messages[:limit]
    allowed_keys = {
        "date",
        "text",
        "senderName",
        "receiverName",
        "priority",
        "messageNumber",
        "messageStatus",
        "id",
    }
    return [
        {key: message.get(key) for key in allowed_keys if key in message}
        for message in messages
    ]

def _normalize_message_date(value: str | None) -> str:
    """Wrapper um `to_utc_iso` für Message-Datumsfelder."""
    return to_utc_iso(value) or to_utc_iso("now")  # type: ignore[return-value]


def send_message(
    mission_id: str,
    message: str,
    receiver_name: str = "unbekannter Empfänger",
    sender_name: str = "AI",
    message_date: str | None = None,
    priority: int = 1,
) -> dict:
    """Schreibt eine Nachricht/Funkmeldung in den Einsatz.

    Pflicht-API-Felder werden automatisch befüllt:
      - date:              `message_date` oder aktueller Zeitpunkt (ISO 8601 mit TZ)
      - externalTimestamp: identisch zu `date` (für Sortierung/Quellzeit)
      - sendername / recivername / messagestatus

    Args:
        mission_id:    GUID des Einsatzes
        message:       Nachrichtentext
        receiver_name: Empfängerkennung (Funkrufname, Stab, …)
        sender_name:   Absenderkennung (default "AI")
        message_date:  ISO-8601-Zeitstempel der Meldung. Wenn None oder "now"
                       wird die aktuelle Systemzeit verwendet. Bei historischen
                       Lagemeldungen den realen Meldezeitpunkt eintragen.
        priority:      1=normal, 2=dringend, 3=blitz (konfigabhängig)
    """
    log.info("TOOL  send_message  mission=%s date=%s", mission_id, message_date)
    ts = _normalize_message_date(message_date)
    env = ensure_success(
        client.post(("mission/" + mission_id + "/message"), json={
            "date": ts,
            "externalTimestamp": ts,
            "text": message,
            "sendername": sender_name,
            "recivername": receiver_name,
            "messagestatus": 1,
            "priority": priority,
        }),
        label="send_message",
    )
    return readback_from_list(
        client,
        f"mission/{mission_id}/message",
        env["id"],
        label="send_message",
        envelope=env,
    )


def get_message_types() -> list[dict]:
    """Verfügbare Nachrichtentypen (z.B. Funkspruch, Meldung, Lagemeldung)."""
    log.info("TOOL  get_message_types")
    return client.get("MessageType")


def get_message_attachments(mission_id: str, message_id: str) -> list[dict]:
    """Anhänge einer bestimmten Nachricht (Name, Typ, Größe)."""
    log.info("TOOL  get_message_attachments  mission_id=%s message_id=%s", mission_id, message_id)
    attachments = client.get(f"mission/{mission_id}/message/{message_id}/attachment")
    allowed_keys = {"id", "name", "attachmentType", "sizeBytes"}
    return [
        {k: a.get(k) for k in allowed_keys if k in a}
        for a in attachments
        if isinstance(a, dict)
    ]


def add_message_attachment(
    mission_id: str,
    message_id: str,
    name: str,
    content_base64: str,
    attachment_type: int = 1,
) -> dict:
    """Hängt eine Datei (Base64-kodiert) an eine Nachricht an.

    Pflicht:
        mission_id, message_id
        name:           Dateiname inkl. Erweiterung (z.B. "lagebild.jpg")
        content_base64: Inhalt Base64-kodiert
        attachment_type: 1=Bild, 2=Dokument, ... (konfigabhängig)
    """
    log.info("TOOL  add_message_attachment  mission=%s msg=%s name=%s", mission_id, message_id, name)
    payload = {
        "name": name,
        "attachmentType": attachment_type,
        "content": content_base64,
    }
    env = ensure_success(
        client.post(
            f"mission/{mission_id}/message/{message_id}/attachment",
            json=payload,
        ),
        label=f"add_message_attachment({name})",
    )
    return readback_from_list(
        client,
        f"mission/{mission_id}/message/{message_id}/attachment",
        env["id"],
        label=f"add_message_attachment({name})",
        envelope=env,
    )


def get_no_mission_messages(limit: int | None = None) -> list[dict]:
    """Einsatzunabhängige Nachrichten / Lagemeldungen ohne zugehörigen Einsatz."""
    log.info("TOOL  get_no_mission_messages")
    messages = client.get("no-mission-message")
    if not isinstance(messages, list):
        return messages  # type: ignore[return-value]
    if limit is not None:
        messages = messages[:limit]
    allowed_keys = {
        "id", "date", "text", "senderName", "receiverName", "priority",
        "messageNumber", "messageStatus", "messageCategory",
        "isSituationReport", "isPressRelease", "isNewsMessage",
    }
    return [{k: m.get(k) for k in allowed_keys if k in m} for m in messages]


def send_no_mission_message(
    message: str,
    receiver_name: str = "Stab",
    sender_name: str = "AI",
    message_date: str | None = None,
    priority: int = 1,
    is_situation_report: bool = False,
    is_press_release: bool = False,
    is_news_message: bool = False,
) -> dict:
    """Schreibt eine einsatzunabhängige Nachricht (z.B. allgemeine Lagemeldung).

    Args:
        message:             Nachrichtentext
        receiver_name:       Empfängerkennung
        sender_name:         Absenderkennung (default "AI")
        message_date:        ISO-8601-Zeitstempel oder None/"now" für jetzt
        priority:            1=normal, 2=dringend, 3=blitz
        is_situation_report: Als Lagebericht markieren
        is_press_release:    Als Pressemitteilung markieren
        is_news_message:     Als Nachrichtenmeldung markieren
    """
    log.info("TOOL  send_no_mission_message  date=%s", message_date)
    ts = _normalize_message_date(message_date)
    env = ensure_success(
        client.post("no-mission-message", json={
            "date": ts,
            "externalTimerstamp": ts,
            "text": message,
            "senderName": sender_name,
            "receiverName": receiver_name,
            "messageStatus": 1,
            "priority": priority,
            "isSituationReport": is_situation_report,
            "isPressRelease": is_press_release,
            "isNewsMessage": is_news_message,
        }),
        label="send_no_mission_message",
    )
    return readback_from_list(
        client,
        "no-mission-message",
        env["id"],
        label="send_no_mission_message",
        envelope=env,
    )


def get_external_message_attachments(
    mission_id: str,
    message_external_id: str,
) -> list[dict]:
    """Anhänge einer Nachricht, referenziert über externe ID.

    Args:
        mission_id:          GUID des Einsatzes
        message_external_id: Externe ID der Nachricht (externalId-Feld)
    """
    log.info("TOOL  get_external_message_attachments  mission=%s ext=%s", mission_id, message_external_id)
    return client.get(
        f"ExternalMessageAttachment?missionId={mission_id}&messageExternalId={message_external_id}"
    )


def add_external_message_attachment(
    mission_id: str,
    message_external_id: str,
    name: str,
    content_base64: str,
    attachment_type: int = 1,
) -> dict:
    """Hängt eine Datei an eine Nachricht an — Identifikation über externe IDs.

    Nützlich wenn nur die externalId der Nachricht bekannt ist (nicht die GUID).

    Args:
        mission_id:          GUID des Einsatzes
        message_external_id: Externe ID der Nachricht
        name:                Dateiname inkl. Erweiterung
        content_base64:      Inhalt Base64-kodiert
        attachment_type:     1=Bild, 2=Dokument, ...
    """
    log.info("TOOL  add_external_message_attachment  mission=%s ext=%s name=%s", mission_id, message_external_id, name)
    env = ensure_success(
        client.post("ExternalMessageAttachment", json={
            "missionId": mission_id,
            "messageExternalId": message_external_id,
            "name": name,
            "attachmentType": attachment_type,
            "content": content_base64,
        }),
        label=f"add_external_message_attachment({name})",
    )
    return readback_from_list(
        client,
        f"ExternalMessageAttachment?missionId={mission_id}&messageExternalId={message_external_id}",
        env["id"],
        label=f"add_external_message_attachment({name})",
        envelope=env,
    )


def register_message_tools(mcp: FastMCP) -> None:
    mcp.add_tool(
        send_message,
        name="send_message",
        description="""Schreibt eine Nachricht / Funkmeldung in einen Einsatz.

        Pflichtfeld `date` wird automatisch korrekt gesetzt:
          - Bei aktuellen Meldungen: `message_date` weglassen oder "now" → es wird der
            aktuelle Zeitpunkt (mit Zeitzone) eingetragen.
          - Bei nachträglich dokumentierten oder historischen Meldungen IMMER den
            tatsächlichen Meldezeitpunkt als ISO-8601 mit Zeitzone übergeben,
            z.B. "2026-04-21T08:17:00+02:00". Vorher `get_current_time` verwenden,
            um Datum/Zeitzone korrekt zu bilden.

        Args:
            mission_id:    GUID des Einsatzes
            message:       Nachrichtentext
            receiver_name: Empfänger-Funkrufname / Stab. Default "unbekannter Empfänger".
            sender_name:   Absender-Kennung. Default "AI".
            message_date:  ISO-8601-Zeitstempel mit TZ ODER None/"now" für jetzt.
            priority:      1=normal, 2=dringend, 3=blitz (konfigabhängig)
        """)
    mcp.add_tool(
        read_messages,
        name="read_messages",
        description="""Reads messages from CommandX.
        
        Args:
            mission_id (uuid as str): The ID of the mission for which messages should be read.
            limit (int optional): Maximum number of messages to return. If not provided, all messages will be returned.
        """)
    mcp.add_tool(
        get_message_types,
        name="get_message_types",
        description="Gibt alle konfigurierten Nachrichtentypen (MessageTypes) zurück.",
    )
    mcp.add_tool(
        get_message_attachments,
        name="get_message_attachments",
        description="""Gibt die Anhänge einer Nachricht (ohne Inhalt, nur Metadaten) zurück.

        Args:
            mission_id: GUID des Einsatzes
            message_id: GUID der Nachricht""",
    )
    mcp.add_tool(
        add_message_attachment,
        name="add_message_attachment",
        description="""Hängt eine Datei (Base64-kodiert) an eine Nachricht an.

        Args:
            mission_id:     GUID des Einsatzes
            message_id:     GUID der Nachricht
            name:           Dateiname inkl. Erweiterung (z.B. "lagebild.jpg")
            content_base64: Inhalt Base64-kodiert
            attachment_type: 1=Bild, 2=Dokument, ... (Standard 1)""",
    )
    mcp.add_tool(
        get_no_mission_messages,
        name="get_no_mission_messages",
        description="""Gibt einsatzunabhängige Nachrichten zurück (allgemeine Lage-
        meldungen, Pressemitteilungen, Neuigkeiten ohne Einsatzbezug).

        Args:
            limit: Max. Anzahl zurückzugebender Nachrichten (optional)""",
    )
    mcp.add_tool(
        send_no_mission_message,
        name="send_no_mission_message",
        description="""Schreibt eine einsatzunabhängige Nachricht / Lagemeldung.

        Verwenden wenn keine Einsatz-GUID bekannt ist oder die Meldung keinem
        konkreten Einsatz zugeordnet werden soll.

        Args:
            message:             Nachrichtentext
            receiver_name:       Empfängerkennung (default "Stab")
            sender_name:         Absenderkennung (default "AI")
            message_date:        ISO-8601 mit TZ oder None/"now" für jetzt
            priority:            1=normal, 2=dringend, 3=blitz
            is_situation_report: Als Lagebericht markieren (true/false)
            is_press_release:    Als Pressemitteilung markieren (true/false)
            is_news_message:     Als Nachrichtenmeldung markieren (true/false)""",
    )
    mcp.add_tool(
        get_external_message_attachments,
        name="get_external_message_attachments",
        description="""Gibt Anhänge einer Nachricht zurück, wenn nur die externe ID
        der Nachricht bekannt ist (nicht die interne GUID).

        Args:
            mission_id:          GUID des Einsatzes
            message_external_id: Externe ID der Nachricht (externalId-Feld)""",
    )
    mcp.add_tool(
        add_external_message_attachment,
        name="add_external_message_attachment",
        description="""Hängt eine Datei an eine Nachricht an — Identifikation via externalId.

        Nützlich wenn nur die externalId der Nachricht bekannt ist.

        Args:
            mission_id:          GUID des Einsatzes
            message_external_id: Externe ID der Nachricht
            name:                Dateiname inkl. Erweiterung
            content_base64:      Inhalt Base64-kodiert
            attachment_type:     1=Bild, 2=Dokument, ... (Standard 1)""",
    )
