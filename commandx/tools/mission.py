from typing import Any
from mcp.server.fastmcp import FastMCP
from client import CIMgateClient
from tools._dates import to_utc_iso
from tools._writes import ensure_success, readback_from_list, CommandXWriteError
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("commandx")

client = CIMgateClient()

def get_missions(
    is_deleted: bool = False,
    is_locked: bool | None = None,
    els: bool | None = None,
    is_takenover: bool | None = None,
    has_end_date: bool | None = None,
    start_date_min: str | None = None,
) -> list[dict]:
    log.info("TOOL  get_missions  is_deleted=%s is_locked=%s els=%s is_takenover=%s has_end_date=%s start_date_min=%s", is_deleted, is_locked, els, is_takenover, has_end_date, start_date_min)
    params: dict[str, Any] = {"isDeleted": str(is_deleted).lower()}

    if is_locked is not None:
        params["isLocked"] = str(is_locked).lower()
    if els is not None:
        params["Els"] = str(els).lower()
    if is_takenover is not None:
        params["isTakenover"] = str(is_takenover).lower()
    if has_end_date is not None:
        params["HasEndDate"] = str(has_end_date).lower()
    if start_date_min is not None:
        params["StartDateMin"] = start_date_min

    return client.get("Mission", params=params)


def get_mission(mission_id: str) -> dict:
    log.info("TOOL  get_mission  mission_id=%s", mission_id)
    return client.get(f"Mission/{mission_id}")


def get_mission_by_external_id(external_id: str) -> dict:
    log.info("TOOL  get_mission_by_external_id  external_id=%s", external_id)
    return client.get(f"Mission/ExternalID/{external_id}")


def get_mission_resources(mission_id: str) -> list[dict]:
    log.info("TOOL  get_mission_resources  mission_id=%s", mission_id)
    resources = client.get(f"mission/{mission_id}/mission-resource")
    allowed_fields = [
        "id",
        "name",
        "serviceType",
        "opta",
        "mapLongitude",
        "mapLatitude",
        "mapAddress",
        "resourceType",
        "resourceWorkingStatusEnum",
    ]

    return [
        {field: resource.get(field) for field in allowed_fields}
        for resource in resources
        if isinstance(resource, dict)
    ]


def get_active_missions() -> list[dict]:
    log.info("TOOL  get_active_missions")
    params = {
        "isDeleted": "false",
        "isLocked": "false",
        "HasEndDate": "false",
    }
    return client.get("Mission", params=params)


def get_missions_since(iso_date: str) -> list[dict]:
    log.info("TOOL  get_missions_since  iso_date=%s", iso_date)
    params = {
        "isDeleted": "false",
        "StartDateMin": iso_date,
    }
    return client.get("Mission", params=params)


def get_mission_resource_groups(mission_id: str) -> list[dict]:
    log.info("TOOL  get_mission_resource_groups  mission_id=%s", mission_id)
    return client.get(f"mission/{mission_id}/mission-resource-group")


def get_organogram_areas(mission_id: str) -> list[dict]:
    """Führungsorganisation (Abschnitte, Stäbe, Bereitstellungsräume) eines Einsatzes."""
    log.info("TOOL  get_organogram_areas  mission_id=%s", mission_id)
    return client.get(f"mission/{mission_id}/organogramarea")


def get_mission_victims(mission_id: str) -> list[dict]:
    """Verletzte/Betroffene eines Einsatzes."""
    log.info("TOOL  get_mission_victims  mission_id=%s", mission_id)
    return client.get(f"mission/{mission_id}/victim")


def get_organogram_damages(mission_id: str, organogram_area_id: str) -> list[dict]:
    """Schadensmeldungen innerhalb eines Abschnitts/Bereichs."""
    log.info("TOOL  get_organogram_damages  mission_id=%s organogram_area_id=%s", mission_id, organogram_area_id)
    return client.get(f"mission/{mission_id}/organogramarea/{organogram_area_id}/damage")


_department_cache: dict[str, str] | None = None


def _resolve_default_department_id() -> str | None:
    """Ermittelt die Ziel-Department-ID für neue Einsätze.

    Priorität:
      1. `COMMANDX_DEFAULT_DEPARTMENT_ID` (ENV)
      2. Department mit Name == `COMMANDX_DEFAULT_DEPARTMENT_NAME` (Default "Hackathon")
      3. None → CIMgate verwendet dann sein internes Default (meist „Übungsleitung")
    """
    global _department_cache
    settings = client.settings
    if settings.commandx_default_department_id:
        return settings.commandx_default_department_id
    if _department_cache is None:
        try:
            _department_cache = {
                (d.get("name") or "").strip(): d["id"]
                for d in client.get("Department")
                if isinstance(d, dict) and d.get("id")
            }
        except Exception as e:  # noqa: BLE001
            log.warning("Department-Auflösung fehlgeschlagen: %s", e)
            _department_cache = {}
    return _department_cache.get(settings.commandx_default_department_name)


def create_mission(
    alarm_keyword: str,
    alarm_detail: str,
    description: str,
    mission_type: int,
    start_date: str | None = None,
    mission_state: int = 1,
    alarm_definition: str | None = None,
    map_latitude: float | None = None,
    map_longitude: float | None = None,
    map_address: str | None = None,
    street: str | None = None,
    street_number: str | None = None,
    post_code: str | None = None,
    city: str | None = None,
    object_name: str | None = None,
    additional_information: str | None = None,
    reporter_contact_person: str | None = None,
    external_id: str | None = None,
    department_id: str | None = None,
    auto_takeover: bool = True,
) -> dict:
    """Legt einen neuen Einsatz in CIMgate an und macht ihn sofort sichtbar.

    Pflicht (vom Aufrufer ZWINGEND zu setzen — kein Default):
      alarm_keyword:  Kurzes Alarmstichwort, z.B. "HOCHWASSER", "B3 WOHNUNGSBRAND", "THL P".
      alarm_detail:   1 konkreter Satz zum Geschehen, z.B. "Keller unter Wasser, ca. 40 cm".
      description:    Längere Lagemeldung (mind. 1 Satz, narrativer Kontext).
      mission_type:   1=Standard (nur Übung/Probe/Sonstiges), 2=Fire (alle Brände),
                      3=Technical (THL: Hochwasser, Sturm, ABC, Gefahrstoff, Türöffnung,
                      VU ohne Brand, Bahn, Tierrettung, Personenrettung ohne Brand).

    Der Aufruf führt intern bis zu drei Requests aus:
      1. POST /Mission mit `missionCategory=4` (ELS) — fester Wert, NICHT parametrisierbar,
         weil CIMgate-Konfiguration nur ELS-Einsätze akzeptiert (Fehler sonst:
         "MissionCategory must be ELS").
      2. PUT /Mission/{id} setzt `mainDepartmentStationId` = Ziel-Department
         (default: „Hackathon") damit der Einsatz in der Standard-Einsatzliste erscheint.
      3. PUT /Mission/{id} setzt `isElsTakenover=true`, überführt die Mission damit
         aus dem ELS-Eingang in die reguläre Bearbeitung.

    Danach wird der Einsatz per GET erneut gelesen und zurückgegeben — inklusive `id`,
    `missionState` und `mainDepartmentStationId` zur Verifikation.

    Bei jedem Fehler wird `CommandXWriteError` geworfen; der Agent muss dem Nutzer
    den Fehler dann transparent melden.

    Pflichtfelder:
      alarm_keyword: Alarmstichwort (String, z.B. "B3 WOHNUNGSBRAND", "HOCHWASSER")
      description:   Lagemeldung, was passiert ist (mind. 1 Satz)

    Sehr empfohlen (sonst fragt der Agent nach):
      city + street + street_number + post_code ODER map_latitude + map_longitude
      object_name, reporter_contact_person, additional_information
    """
    log.info("TOOL  create_mission  keyword=%s desc=%.60s", alarm_keyword, description)

    # 1) POST /Mission — Kategorie IMMER 4 (ELS), sonst weist CIMgate ab
    payload: dict[str, Any] = {
        "startDate": to_utc_iso(start_date),
        "alarmKeyword": alarm_keyword,
        "description": description,
        "missionType": mission_type,
        "missionCategory": 4,  # ELS — hart, sonst "MissionCategory must be ELS"
        "missionState": mission_state,
    }
    optional = {
        "alarmDefinition": alarm_definition,
        "alarmDetail": alarm_detail,
        "mapLatitude": map_latitude,
        "mapLongitude": map_longitude,
        "mapAddress": map_address,
        "street": street,
        "streetNumber": street_number,
        "postCode": post_code,
        "city": city,
        "objectName": object_name,
        "additionalInformation": additional_information,
        "reporterContactPerson": reporter_contact_person,
        "externalId": external_id,
    }
    for k, v in optional.items():
        if v is not None:
            payload[k] = v

    created = ensure_success(client.post("Mission", json=payload), label="create_mission")
    mid = created["id"]

    # 2) Department-Zuweisung
    target_dept = department_id or _resolve_default_department_id()

    # 3) Takeover + Department in einem PUT (wir brauchen ohnehin das volle Objekt)
    try:
        current = client.get(f"Mission/{mid}")
    except Exception as e:  # noqa: BLE001
        log.warning("Read-back nach create_mission fehlgeschlagen: %s", e)
        current = dict(payload, id=mid)

    put_body = dict(current)
    put_body["id"] = mid
    put_body["missionType"] = mission_type
    put_body["missionCategory"] = 4
    put_body["missionState"] = mission_state
    if target_dept:
        put_body["mainDepartmentStationId"] = target_dept
    if auto_takeover:
        put_body["isElsTakenover"] = True

    try:
        ensure_success(
            client.put(f"Mission/{mid}", json=put_body),
            label="create_mission:takeover",
        )
    except CommandXWriteError as e:
        log.warning("Takeover/Department-Zuweisung fehlgeschlagen (Einsatz existiert trotzdem): %s", e)

    # 4) Finalen Zustand zurückgeben
    final = client.get(f"Mission/{mid}")
    return {
        "id": mid,
        "alarmKeyword": final.get("alarmKeyword"),
        "missionState": final.get("missionState"),
        "missionCategory": final.get("missionCategory"),
        "mainDepartmentStationId": final.get("mainDepartmentStationId"),
        "mapAddress": final.get("mapAddress"),
        "startDate": final.get("startDate"),
        "city": final.get("city"),
        "description": final.get("description"),
    }


def add_mission_resource(
    mission_id: str,
    name: str,
    resource_type: str,
    service_type: int = 1,
    resource_mission_status: int = 1,
    resource_working_status: int = 1,
    resource_id: str | None = None,
    radio_call: str | None = None,
    opta: str | None = None,
    license_plate: str | None = None,
    station: str | None = None,
    home_station: str | None = None,
    information: str | None = None,
    organogram_area_id: str | None = None,
    map_latitude: float | None = None,
    map_longitude: float | None = None,
    map_address: str | None = None,
    alarm_date: str | None = None,
) -> dict:
    """Ordnet ein Einsatzmittel (Fahrzeug/Kraft) einem Einsatz zu.

    resource_id verlinkt ein bestehendes Einsatzmittel aus dem Resource-Stamm
    (siehe `get_resources`). Wenn nicht angegeben, wird ein ad-hoc Eintrag erzeugt.

    resource_mission_status:  1=alarmiert, 2=ausgerückt, 3=an Einsatzstelle, 4=zurück,
                              5=verfügbar, 6=außer Dienst (siehe CIMgate-Config)
    resource_working_status:  Arbeitsstatus / FMS-ähnlich
    """
    log.info("TOOL  add_mission_resource  mission=%s name=%s type=%s", mission_id, name, resource_type)
    payload: dict = {
        "name": name,
        "resourceType": resource_type,
        "serviceType": service_type,
        "resourceMissionStatusEnum": resource_mission_status,
        "resourceWorkingStatusEnum": resource_working_status,
    }
    optional = {
        "resourceId": resource_id,
        "radioCall": radio_call,
        "opta": opta,
        "licensePlate": license_plate,
        "station": station,
        "homeStation": home_station,
        "information": information,
        "organogramAreaId": organogram_area_id,
        "mapLatitude": map_latitude,
        "mapLongitude": map_longitude,
        "mapAddress": map_address,
        "alarmDate": to_utc_iso(alarm_date),
    }
    for k, v in optional.items():
        if v is not None:
            payload[k] = v
    env = ensure_success(
        client.post(f"mission/{mission_id}/mission-resource", json=payload),
        label=f"add_mission_resource({name})",
    )
    return readback_from_list(
        client,
        f"mission/{mission_id}/mission-resource",
        env["id"],
        label=f"add_mission_resource({name})",
        envelope=env,
    )


def add_mission_resource_group(
    mission_id: str,
    name: str,
    service_type: int = 1,
    resource_mission_status: int = 1,
    resource_working_status: int = 1,
    radio_call: str | None = None,
    information: str | None = None,
) -> dict:
    """Legt eine Einsatzmittelgruppe (z.B. Löschzug) innerhalb eines Einsatzes an."""
    log.info("TOOL  add_mission_resource_group  mission=%s name=%s", mission_id, name)
    payload: dict = {
        "name": name,
        "serviceType": service_type,
        "resourceMissionStatusEnum": resource_mission_status,
        "resourceWorkingStatusEnum": resource_working_status,
    }
    if radio_call is not None:
        payload["radioCall"] = radio_call
    if information is not None:
        payload["information"] = information
    env = ensure_success(
        client.post(f"mission/{mission_id}/mission-resource-group", json=payload),
        label=f"add_mission_resource_group({name})",
    )
    return readback_from_list(
        client,
        f"mission/{mission_id}/mission-resource-group",
        env["id"],
        label=f"add_mission_resource_group({name})",
        envelope=env,
    )


def add_organogram_area(
    mission_id: str,
    name: str,
    type_: int = 1,
    abbreviation: str | None = None,
    leader: str | None = None,
    radio_call: str | None = None,
    radio_channel: str | None = None,
    phone_number: str | None = None,
    email: str | None = None,
    description: str | None = None,
    parent_area_id: str | None = None,
    map_latitude: float | None = None,
    map_longitude: float | None = None,
    map_address: str | None = None,
) -> dict:
    """Legt einen Führungsabschnitt / Bereitstellungsraum / Stab im Einsatz an.

    type_:  1=Abschnitt, 2=Bereitstellungsraum, 3=Stab (siehe CIMgate-Config)
    parent_area_id: Für hierarchische Struktur (Abschnitt innerhalb eines Stabs).
    """
    log.info("TOOL  add_organogram_area  mission=%s name=%s", mission_id, name)
    payload: dict = {"name": name, "type": type_}
    optional = {
        "abbreviation": abbreviation,
        "leader": leader,
        "radioCall": radio_call,
        "radioChannel": radio_channel,
        "phoneNumber": phone_number,
        "email": email,
        "description": description,
        "parentAreaId": parent_area_id,
        "mapLatitude": map_latitude,
        "mapLongitude": map_longitude,
        "mapAddress": map_address,
    }
    for k, v in optional.items():
        if v is not None:
            payload[k] = v
    env = ensure_success(
        client.post(f"mission/{mission_id}/organogramarea", json=payload),
        label=f"add_organogram_area({name})",
    )
    return readback_from_list(
        client,
        f"mission/{mission_id}/organogramarea",
        env["id"],
        label=f"add_organogram_area({name})",
        envelope=env,
    )


def add_mission_victim(
    mission_id: str,
    number: int,
    triage_enum: int,
    triage_date: str,
    first_name: str | None = None,
    last_name: str | None = None,
    age: int | None = None,
    gender_enum: int | None = None,
    found_at_map_latitude: float | None = None,
    found_at_map_longitude: float | None = None,
    found_at_map_address: str | None = None,
    current_map_latitude: float | None = None,
    current_map_longitude: float | None = None,
    current_map_address: str | None = None,
    diagnose: str | None = None,
    notes: str | None = None,
    needs_oxygen: bool | None = None,
    is_doctor_needed: bool | None = None,
    is_reanimation_needed: bool | None = None,
    transport_type_enum: int | None = None,
    hospital_object_id: str | None = None,
) -> dict:
    """Erfasst einen/eine Verletzte(n) im Einsatz.

    Pflicht: number (fortlaufende Nummer), triage_enum, triage_date (ISO 8601).
    triage_enum:   1=rot (sofort), 2=gelb (dringend), 3=grün (leicht),
                   4=blau/schwarz (verstorben), 5=kontaminiert (konfigabhängig)
    gender_enum:   1=männlich, 2=weiblich, 3=divers (konfigabhängig)
    """
    log.info("TOOL  add_mission_victim  mission=%s number=%s triage=%s", mission_id, number, triage_enum)
    payload: dict = {
        "number": number,
        "triageEnum": triage_enum,
        "triageDate": to_utc_iso(triage_date),
    }
    optional = {
        "firstName": first_name,
        "lastName": last_name,
        "age": age,
        "genderEnum": gender_enum,
        "foundAtMapLatitude": found_at_map_latitude,
        "foundAtMapLongitude": found_at_map_longitude,
        "foundAtMapAddress": found_at_map_address,
        "currentMapLatitude": current_map_latitude,
        "currentMapLongitude": current_map_longitude,
        "currentMapAddress": current_map_address,
        "diagnose": diagnose,
        "notes": notes,
        "needsOxygen": needs_oxygen,
        "isDoctorNeeded": is_doctor_needed,
        "isReanimationNeeded": is_reanimation_needed,
        "transportTypeEnum": transport_type_enum,
        "hospitalObjectId": hospital_object_id,
    }
    for k, v in optional.items():
        if v is not None:
            payload[k] = v
    env = ensure_success(
        client.post(f"mission/{mission_id}/victim", json=payload),
        label=f"add_mission_victim(#{number})",
    )
    return readback_from_list(
        client,
        f"mission/{mission_id}/victim",
        env["id"],
        label=f"add_mission_victim(#{number})",
        envelope=env,
    )


def add_organogram_damage(
    mission_id: str,
    organogram_area_id: str,
    external_id: str,
    count: int = 1,
    symbol_id: str | None = None,
    map_latitude: float | None = None,
    map_longitude: float | None = None,
    map_address: str | None = None,
) -> dict:
    """Erfasst eine Schadensmeldung innerhalb eines Führungsabschnitts.

    external_id ist Pflicht laut API (eindeutige externe Kennung des Schadens).
    symbol_id verweist auf ein taktisches Zeichen (optional).
    """
    log.info("TOOL  add_organogram_damage  mission=%s area=%s count=%s", mission_id, organogram_area_id, count)
    payload: dict = {
        "count": count,
        "externalId": external_id,
        "organogramAreaId": organogram_area_id,
    }
    optional = {
        "symbolId": symbol_id,
        "mapLatitude": map_latitude,
        "mapLongitude": map_longitude,
        "mapAddress": map_address,
    }
    for k, v in optional.items():
        if v is not None:
            payload[k] = v
    env = ensure_success(
        client.post(
            f"mission/{mission_id}/organogramarea/{organogram_area_id}/damage",
            json=payload,
        ),
        label=f"add_organogram_damage({external_id})",
    )
    return readback_from_list(
        client,
        f"mission/{mission_id}/organogramarea/{organogram_area_id}/damage",
        env["id"],
        label=f"add_organogram_damage({external_id})",
        envelope=env,
    )


def register_mission_tools(mcp: FastMCP) -> None:
    mcp.add_tool(
        get_missions,
        name="get_missions",
        description="""Gibt alle Einsätze (Missions) zurück.

    Args:
        is_deleted:    Gelöschte Einsätze einschließen (Standard: False)
        is_locked:     Nur gesperrte / nicht-gesperrte Einsätze (None = kein Filter)
        els:           Nur ELS-Einsätze (None = kein Filter)
        is_takenover:  Nur übernommene Einsätze (None = kein Filter)
        has_end_date:  Nur Einsätze mit/ohne Enddatum (None = kein Filter)
        start_date_min: Einsätze ab diesem Datum, ISO 8601 z.B. "2026-01-01T00:00:00Z\"""",
    )
    mcp.add_tool(
        get_mission,
        name="get_mission",
        description="""Gibt einen einzelnen Einsatz anhand seiner ID zurück.

    Args:
        mission_id: GUID des Einsatzes""",
    )
    mcp.add_tool(
        get_mission_by_external_id,
        name="get_mission_by_external_id",
        description="""Gibt einen Einsatz anhand seiner ExternalID zurück.

    Args:
        external_id: Externe ID des Einsatzes""",
    )
    mcp.add_tool(
        get_mission_resources,
        name="get_mission_resources",
        description="""Gibt alle eingesetzten Kräfte/Fahrzeuge (MissionResources) eines Einsatzes zurück.

    Args:
        mission_id: GUID des Einsatzes""",
    )
    mcp.add_tool(
        get_active_missions,
        name="get_active_missions",
        description="""Gibt alle aktiven (nicht gelöschten, nicht gesperrten) Einsätze ohne Enddatum zurück.
    Kurzform für den häufigsten Anwendungsfall.""",
    )
    mcp.add_tool(
        get_missions_since,
        name="get_missions_since",
        description="""Gibt alle Einsätze ab einem bestimmten Datum zurück.

    Args:
        iso_date: Startdatum im ISO-8601-Format, z.B. "2026-04-01T00:00:00Z\"""",
    )
    mcp.add_tool(
        get_mission_resource_groups,
        name="get_mission_resource_groups",
        description="""Gibt alle Einsatzmittelgruppen (MissionResourceGroups) eines Einsatzes zurück.
    Gruppen fassen mehrere Fahrzeuge/Kräfte als taktische Einheit zusammen (z.B. Löschzug).

    Args:
        mission_id: GUID des Einsatzes""",
    )
    mcp.add_tool(
        get_organogram_areas,
        name="get_organogram_areas",
        description="""Gibt die Führungsorganisation (Abschnitte, Stäbe, Bereitstellungsräume)
    eines Einsatzes zurück – inkl. Leitung, Funkrufnamen, zugeordnete Ressourcen und Nachrichten.

    Args:
        mission_id: GUID des Einsatzes""",
    )
    mcp.add_tool(
        get_mission_victims,
        name="get_mission_victims",
        description="""Gibt alle Verletzten/Betroffenen (Victims) eines Einsatzes zurück
    inklusive Triage-Stufe, Fundort, aktueller Aufenthaltsort und medizinische Angaben.

    Args:
        mission_id: GUID des Einsatzes""",
    )
    mcp.add_tool(
        get_organogram_damages,
        name="get_organogram_damages",
        description="""Gibt Schadensmeldungen innerhalb eines Führungsabschnitts zurück.

    Args:
        mission_id: GUID des Einsatzes
        organogram_area_id: GUID des Abschnitts (siehe get_organogram_areas)""",
    )
    mcp.add_tool(
        create_mission,
        name="create_mission",
        description="""Legt einen neuen Einsatz in CIMgate an, weist ihn dem konfigurierten
    Department zu (default: „Hackathon") und führt automatisch den ELS-Takeover durch,
    damit der Einsatz SOFORT in der Standard-Einsatzliste erscheint.

    Das Tool garantiert keine halben Anlagen: bei Fehlern wird eine Exception mit der
    CIMgate-Fehlermeldung geworfen (z.B. wenn Pflichtfelder fehlen). Nach erfolgreicher
    Anlage wird der Einsatz zurückgelesen und der aktuelle Zustand zurückgegeben.

    Notfallabfrage vor Aufruf: Wenn Pflichtfelder fehlen, FRAG DEN NUTZER (W-Fragen),
    lege NICHT mit Platzhaltern an.

    Pflichtfelder (NIEMALS leer lassen!):
        alarm_keyword:  Alarmstichwort, kurz & einsatztaktisch (z.B. "HOCHWASSER",
                        "B3 WOHNUNGSBRAND", "THL P", "ABC2"). Bei Unsicherheit VORHER
                        `get_alarm_keywords` aufrufen. Max. ~3 Wörter.
        alarm_detail:   1 konkreter Satz, WAS genau passiert ist
                        (z.B. "Keller unter Wasser, ca. 40 cm",
                         "Zimmerbrand 3. OG, Person vermisst"). NICHT dasselbe wie
                        `description` (die ist länger, narrativ).
        description:    Kurze Lagemeldung, Kontext und Entwicklung (mind. 1 Satz).
        mission_type:   Einsatztyp — WICHTIG, BEWUSST WÄHLEN (siehe Tabelle unten).

    `mission_type` Auswahl (nicht blind 1 nehmen!):
        1 = Standard   — nur wenn nichts anderes passt (Übung, Probe, Fehlalarm)
        2 = Fire       — alle Brände (Wohnung, Gebäude, Vegetation, PKW, Kellerbrand …)
        3 = Technical  — Technische Hilfeleistung: Hochwasser, Sturm, Unwetter,
                         Baum umgestürzt, Wasser im Keller, Türöffnung, VU ohne Brand,
                         Ölspur, Tierrettung, ABC/Gefahrstoff, Gasausstrom,
                         Personenrettung, Bahn-Einsätze
        Faustregel: KEIN Feuer → 3 Technical. Nur Feuer → 2 Fire. Rest/Übung → 1.

    Bei fehlender Lokation WEIGERE DICH anzulegen — frag nach Adresse ODER Koordinaten:
        city (+ street + street_number + post_code) ODER (map_latitude + map_longitude)

    Optional, aber wichtig (wenn vorhanden mitgeben, sonst einmal nachfragen):
        start_date:             Alarmzeitpunkt ISO 8601. None oder "now" → aktueller Zeitpunkt.
        map_latitude/longitude: Koordinaten aus `geocode_location`.
        map_address:            Vollständige Adresse (wird in der UI angezeigt).
        street / street_number / post_code / city
        object_name:            Gebäude/Objekt (Schule, Bahnhof, Industriepark …)
        alarm_definition:       Längeres, beschreibendes Label des Alarms
                                (z.B. "Hochwasser — Flächenlage", "B4 + ABC2 — Chlorgas")
        additional_information: Sondermerkmale (Wind, Gefahrstoffe, Stufen, PAK …)
        reporter_contact_person: Meldername + Funktion + Rückrufnummer
        external_id:            externe Kennung (wird nicht interpretiert)

    Technische Parameter (nicht vom Nutzer erfragen, Defaults passen):
        mission_state:  1=aktiv/offen (default)
        department_id:  UUID; überschreibt den Default „Hackathon"
        auto_takeover:  true (default) – setzt `isElsTakenover=true`""",
    )
    mcp.add_tool(
        add_mission_resource,
        name="add_mission_resource",
        description="""Alarmiert/ordnet ein Fahrzeug oder eine Kraft einem Einsatz zu.

    Pflicht:
        mission_id:     GUID des Einsatzes
        name:           Anzeigename (z.B. "HLF 20/1")
        resource_type:  Typ-Kürzel (z.B. "HLF", "DLK", "RTW")

    Optional:
        resource_id:    GUID aus Resource-Stamm (verknüpft echten Eintrag; siehe `get_resources`)
        service_type:   1=Feuerwehr, 2=Rettungsdienst, ...
        resource_mission_status: 1=alarmiert, 2=ausgerückt, 3=an Einsatzstelle
        resource_working_status: FMS-ähnlich
        radio_call, opta, license_plate, station, home_station, information
        organogram_area_id: Zuordnung zu einem Abschnitt (siehe `add_organogram_area`)
        map_latitude, map_longitude, map_address
        alarm_date: ISO 8601""",
    )
    mcp.add_tool(
        add_mission_resource_group,
        name="add_mission_resource_group",
        description="""Legt eine Einsatzmittelgruppe (z.B. Löschzug) im Einsatz an.

    Pflicht: mission_id, name
    Optional: service_type, resource_mission_status, resource_working_status,
              radio_call, information""",
    )
    mcp.add_tool(
        add_organogram_area,
        name="add_organogram_area",
        description="""Legt einen Führungsabschnitt, Bereitstellungsraum oder Stab im Einsatz an.

    Pflicht: mission_id, name (z.B. "Abschnitt Wasser", "Bereitstellungsraum Süd")
    type_:   1=Abschnitt, 2=Bereitstellungsraum, 3=Stab (konfigabhängig)
    Optional: abbreviation, leader, radio_call, radio_channel, phone_number, email,
              description, parent_area_id (für Hierarchie), map_latitude/longitude/address""",
    )
    mcp.add_tool(
        add_mission_victim,
        name="add_mission_victim",
        description="""Erfasst einen Verletzten/eine Betroffene im Einsatz inkl. Triage.

    Pflicht:
        mission_id:    GUID des Einsatzes
        number:        fortlaufende Nummer
        triage_enum:   1=rot (sofort), 2=gelb (dringend), 3=grün (leicht),
                       4=blau/schwarz (verstorben)
        triage_date:   ISO 8601 (vorher `get_current_time` aufrufen!)

    Optional:
        first_name, last_name, age, gender_enum (1=m, 2=w, 3=divers)
        found_at_map_* : Fundort
        current_map_*  : aktueller Aufenthaltsort
        diagnose, notes
        needs_oxygen, is_doctor_needed, is_reanimation_needed
        transport_type_enum, hospital_object_id""",
    )
    mcp.add_tool(
        add_organogram_damage,
        name="add_organogram_damage",
        description="""Erfasst eine Schadensmeldung innerhalb eines Führungsabschnitts.

    Pflicht:
        mission_id, organogram_area_id, external_id (eindeutige externe Kennung)
    Optional:
        count (Anzahl, Standard 1), symbol_id, map_latitude/longitude/address""",
    )

