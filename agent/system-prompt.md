# CIMGate.CONNECT – KI-Kontextwissen

> Generiert: 2026-04-17 18:30 Uhr
> Datenquelle: CIMGate.CONNECT REST API (https://connect-preview.eurocommand.com:7001)

---

## Systemübersicht

**CIMGate.CONNECT** ist ein digitales Einsatzmanagementsystem (EMS) für den Bevölkerungsschutz.
Es verwaltet Einsätze (Missions), Einsatzkräfte (Resources), Kommunikation (Messages),
Organisationsstrukturen (OrganogramAreas) sowie Opfer-Tracking (Victims).

Aktuelle Systemdaten:
- **Aktive Einsätze:** 3
- **Gesamte Einsatzmittel im System:** 158
- **Abteilungen:** 6
- **Alarmstichworte:** 8
- **Fahrzeug-/Einheitstypen:** 71

---

## Organisationsstruktur (Abteilungen/Stäbe)

### Übungsleitung (ÜL)
- **ID:** `42bdfc8c-9b39-f111-81de-f769d0cdf82d`
- **Hauptstab:** Ja
- **Externer Einsatzträger:** Ja

### Experimental Stab (Stab)
- **ID:** `3e2c1097-9b39-f111-81de-f769d0cdf82d`
- **Hauptstab:** Ja
- **Externer Einsatzträger:** Ja

### Experimental Abschnittsleitung (AL)
- **ID:** `5ec3e7a0-9b39-f111-81de-f769d0cdf82d`
- **Hauptstab:** Ja
- **Externer Einsatzträger:** Ja

### Hackathon (Hackathon)
- **ID:** `b5c77a10-2d3a-f111-81de-f769d0cdf82d`
- **Hauptstab:** Nein
- **Externer Einsatzträger:** Nein

### Abschnittsleitung 1 (AL1)
- **ID:** `368d68f1-2e3a-f111-81de-f769d0cdf82d`
- **Hauptstab:** Nein
- **Externer Einsatzträger:** Nein

### Bereitstellungsraum (BR )
- **ID:** `e11797fa-2e3a-f111-81de-f769d0cdf82d`
- **Hauptstab:** Nein
- **Externer Einsatzträger:** Nein

---

## Alarmstichworte

| Kürzel | Bezeichnung | Typ |
|--------|-------------|-----|
| `AUSN` | Ausnahmezustand | 0 |
| `FEU 3` | Feuer, 3 Löschzüge | 0 |
| `FEU 6` | Feuer, 6 Löschzüge | 0 |
| `FEU G` | Feuer, größer Standard | 0 |
| `TH BAHN R3` | Technische Hilfe im Bahnbereich, > 50 Verletzte | 0 |
| `THGXY` | Technische Hilfe, größer Standard, Gefahrstoff (kein CBRN), Menschenleben in Gefahr | 0 |
| `TH K` | Technische Hilfeleistung kleiner Standard | Technical |

---

## Aktive Einsätze

### Einsatz #5: AUSN – Männergrippe

| Feld | Wert |
|------|------|
| **ID** | `4269c107-55ed-4f3b-8b1a-e0f1274ad811` |
| **Alarmkürzel** | AUSN – Ausnahmezustand |
| **Einsatzart** | Standard |
| **Status** | Active |
| **Start** | 2026-04-17 17:43 Uhr |
| **Ende** | noch aktiv |
| **Lageort** | Kölner Dom |
| **Koordinaten** | 50.941230, 6.958230 |
| **Lagekurzbeschreibung** | Schlimm 7 * keine Lage |
| **Führende Abteilung** | Abschnittsleitung 1 (AL1) |

#### Führungsorganisation (2 Bereiche)

**Einsatzleitung** (Command)
- Abteilung: –

**Leitstelle** (Dispatch)
- Abteilung: –

---

### Einsatz #4: TH K – Explosion in Chemiebetrieb

| Feld | Wert |
|------|------|
| **ID** | `40a81b0a-c185-49dd-806c-ff4f1c3fc23d` |
| **Alarmkürzel** | TH K – Technische Hilfeleistung kleiner Standard |
| **Einsatzart** | Technical |
| **Status** | Active |
| **Start** | 2026-04-17 17:41 Uhr |
| **Ende** | noch aktiv |
| **Lageort** | Weidendamm 50, 30167, Hannover, Nordstadt, Niedersachsen |
| **Koordinaten** | 52.389397, 9.725683 |
| **Lagekurzbeschreibung** | hm * Lage unklar * mehrere Anrufer |
| **Führende Abteilung** | Abschnittsleitung 1 (AL1) |

#### Führungsorganisation (2 Bereiche)

**Einsatzleitung** (Command)
- Abteilung: –

**Leitstelle** (Dispatch)
- Abteilung: –

---

### Einsatz #3: FEU 6 – Waldbrand - München Perlach

| Feld | Wert |
|------|------|
| **ID** | `f0c15c77-643c-49cb-9ed4-e15e23ce48ea` |
| **Alarmkürzel** | FEU 6 – Feuer, 6 Löschzüge |
| **Einsatzart** | Fire |
| **Status** | Active |
| **Start** | 2026-04-17 07:16 Uhr |
| **Ende** | noch aktiv |
| **Lageort** | Perlach Geräumt, 82041, Perlacher Forst, Bayern |
| **Koordinaten** | 48.070534, 11.573511 |
| **Lagekurzbeschreibung** | Waldbrand München Perlach - überörtliche Anforderungen |
| **Führende Abteilung** | Hackathon (Hackathon) |

#### Führungsorganisation (8 Bereiche)

**Einsatzleitung** (Command)
- Leitung: Max Mustermann
- Funkrufname: FloEC 10-11-01
- Führungskanal: TBZ_BRD_1
- Position: Parkackerstraße, 82008, Unterhaching, Bayern
- Abteilung: Hackathon
- Einsatzmittel (1):
  - **FloEC 10-11-01** [ELW 1/Fire] Status: Mission @ Aslan Imbiss
- Nachrichten (5):
  - [2026-04-17 07:44 Uhr] **#12** Lagemeldung von „Einsatzabschnitt 3 - West" → „Einsatzleitung" [Low/Unopen]
    > Lagemeldung Abschnitt West - Wind treibt Feuer in Richtung der Bavaria Studios - Einsatzabschnitt 3.1 gebildet um Gebit zu schützen. Nachforderungen folgen.
  - [2026-04-17 07:58 Uhr] **#24** Anfrage von „AL1: FüAss AL" → „Einsatzleitung" [Low/Open]
    > Anfrage Wetterinformationen alle 2 Stunden für die Abschnittsleitung 1.
  - [2026-04-17 10:10 Uhr] **#49** Nachforderung von „UEA 3.1 Bavaria Studios" → „Einsatzleitung" [Normal/Unopen]
    > Dringend Kräfte zum Schutz der Bavaria Studios benötigt.  Aktuell Werkfeuerwehr mit 1 LZ im Einsatz.   Nachforderung:  2 LZ  Material zur Vegetationsbrandbekämpfung für mind. 2 Gruppen.   Wassertransportzüge und Flatbhälter zur Wasserreserver benötigt.
  - [2026-04-17 10:11 Uhr] **#50** Anfrage von „Bereitstellungsraum 1" → „Einsatzleitung" [Low/Unopen]
    > Wann treffen die 8. BSB SH und 1. BSB SH im Bereitstellungsraum an?
  - [2026-04-17 10:12 Uhr] **#51** Anfrage von „Bereitstellungsraum 1" → „Einsatzleitung" [Low/Unopen]
    > Wie viele Kräfte befinden sich aktuell auf Anfahrt zum BR?  Gibt es eine aktuelle Übersicht angeforderter Kräfte?

**Leitstelle** (Dispatch)
- Abteilung: –
- Nachrichten (8):
  - [2026-04-17 07:30 Uhr] **#1** System von „Hackathon: S3 / S6" → „Leitstelle" [Normal/Unopen]
    > Einsatz: Bereitstellungsraum hinzufügen Name: Bereitstellungsraum 1
  - [2026-04-17 07:33 Uhr] **#2** System von „Hackathon: S3 / S6" → „Leitstelle" [Normal/Unopen]
    > Einsatz: Abschnitt hinzufügen Name: Einsatzabschnitt 2 - Süd
  - [2026-04-17 07:46 Uhr] **#13** Nachforderung von „Hackathon: S2 / S5" → „Leitstelle" [Normal/Unopen]
    > Weitere Kräfte benötigt: Alarmieren Sie 4 Feuerwehrbereitschaften zur Anfahrt der Bereitstellungsraumes BR1 zur sofortigen Verfügung. Einsatzdauer mind. 24h.
  - [2026-04-17 07:48 Uhr] **#16** Nachforderung von „Hackathon: S4" → „Leitstelle" [Normal/Unopen]
    > Anforderung 2 Gruppen Betreuung 2 Fachgruppe N zum BR1 zum Betrieb des BR und Verpflegung der Kräfte - Einsatzdauer vermutlich 48 Stunden.
  - [2026-04-17 08:21 Uhr] **#35** System von „Hackathon: S4" → „Leitstelle" [Normal/Unopen]
    > Einsatz: Abschnitt hinzufügen Name: Logistik & Versorgung
 Aufbau zentrale Versorgung und Logistik für alle Abschnitte.
  - [2026-04-17 08:27 Uhr] **#40** Lagebericht von „Hackathon: S2 / S5" → „Leitstelle" [Low/Unopen]
    > Aktueller Lagebericht 10:25 17.04.2026:   Allgemeine Lage:  Freitagvormitag - meldung über einen Waldbrand im südlichen München, angrenzend Landkreis München.  Waldbrand ausgedehnt pber mehrere ha. Vollfeuer im Wald.   Wetter: Aktuell ca. 13 Grad, ohne Regen, geringe Luftfeuchtigkeit. Aktuell windstill, soll im Verlauf des tages aufdrehen und von Ost nach West verlaufen.  Organisation:  Aktuell 4 Einsatzabschnitte gebildet.  - Nord - Süd - Ost - Logistik  Dazu ein zentraler Bereitstellugsraum.  Einsatzabschnitte arbeiten eigenständig.  Anforerungen über die Einstzleitung/Stab Hackathon.   Kräfte:  Kräfteübersicht aktuell nicht vollständig.  Muss aktalisiert werden.  Anforderungen werden zentral über BR1 und S1 koordiniert.   Externe Kräfte zur Unterstützung angefordert.  Nächste Lagebesprechung: 12 Uhr.
  - [2026-04-17 10:16 Uhr] **#53** Lagebericht von „Hackathon: S2 / S5" → „Leitstelle" [Low/Unopen]
    > Lagebericht 12:15 17.04.2026:   Lageveränderung:  Feuer breitet sich weiter in Richtung Nor-Ost aus.  Feuer weiterhin in keinem  Abschnitt unter Kontrolle. im UEA 3.1 ist das Gebiet der Bavara Studios akut bedroht.   Kräfte:  Vielzahl an Kräften aktuell auf der Anfahrt. Eintreffzeiten verteilt über die Zeit.  Nachforderung:  Hubschrauber mit Außenlastbehälter zur Einsatzstelle. Dafür mit Leitstelle geeignete Landeplätze bestimmen.
  - [2026-04-17 10:16 Uhr] **#54** Anfrage von „Hackathon: S2 / S5" → „Leitstelle" [Low/Unopen]
    > Anfrage aktuelle Wetterinformationen und Vorhersage.

**Bereitstellungsraum 1** (Staging)
- Position: Campeonpark, 85579, Neubiberg, Bayern
- Abteilung: Bereitstellungsraum
- Einsatzmittel (10):
  - **3-ELW2-1** [ELW 2/Other] Status: Staging
  - **10-TLF-5** [TLF/Fire] Status: Staging
  - **8. Brandschutzbereitschaft Schleswig-Holstein** [FwBer/Fire] Status: Staging
  - **10-TLF-6** [TLF/Fire] Status: Staging
  - **Fgr N MUC 1** [FGr N/Usar] Status: Staging
  - **Streife 1 ** [Streife/Police] Status: Staging
  - **FGR N MUC 2** [FGr N/Usar] Status: Staging
  - **Streife 2 ** [Streife/Police] Status: Staging
  - **10-TLF-7** [TLF/Fire] Status: Staging
  - **1. Brandschutzbereitschaft Schleswig-Holstein** [FwBer/Fire] Status: Staging
- Nachrichten (6):
  - [2026-04-17 07:33 Uhr] **#3** System von „Hackathon: S3 / S6" → „Bereitstellungsraum 1" [Normal/Unopen]
    > Einsatz: Abschnitt hinzufügen Name: Einsatzabschnitt 2 - Süd
  - [2026-04-17 08:04 Uhr] **#31** Nachforderung von „AL1: FüAss AL" → „Bereitstellungsraum 1" [Normal/Unopen]
    > Anforderung weiterer Kräfte:  5 Tanklöschfahrzeuge für EInsatzabschnitt1 benötigt.
  - [2026-04-17 10:11 Uhr] **#50** Anfrage von „Bereitstellungsraum 1" → „Einsatzleitung" [Low/Unopen]
    > Wann treffen die 8. BSB SH und 1. BSB SH im Bereitstellungsraum an?
  - [2026-04-17 10:11 Uhr] **#50.1** System von „Bereitstellungsraum 1" → „Einsatzleitung
(Hackathon: S2 / S5)" [Low/Unopen]
    > Anfrage: Wann treffen die 8. BSB SH und 1. BSB SH im Bereitstellungsraum an?
  - [2026-04-17 10:12 Uhr] **#51** Anfrage von „Bereitstellungsraum 1" → „Einsatzleitung" [Low/Unopen]
    > Wie viele Kräfte befinden sich aktuell auf Anfahrt zum BR?  Gibt es eine aktuelle Übersicht angeforderter Kräfte?
  - [2026-04-17 10:12 Uhr] **#51.1** System von „Bereitstellungsraum 1" → „Einsatzleitung
(Hackathon: S2 / S5)" [Low/Unopen]
    > Anfrage: Wie viele Kräfte befinden sich aktuell auf Anfahrt zum BR?  Gibt es eine aktuelle Übersicht angeforderter Kräfte?

**Einsatzabschnitt 1 - Nord** (Sector)
- Funkrufname: 1-ELW2-1
- Führungskanal: TBZ_BRD_2
- Position: Oberbiberger Straße, 82041, Perlacher Forst, Bayern
- Abteilung: Abschnittsleitung 1
- Einsatzmittel (5):
  - **1-ELW2-1** [ELW 2/Fire] Status: Mission
  - **10-TLF-4** [TLF/Fire] Status: Mission
  - **10-TLF-3** [TLF/Fire] Status: Mission
  - **10-TLF-1** [TLF/Fire] Status: Mission
  - **10-TLF-2** [TLF/Fire] Status: Mission
- Nachrichten (2):
  - [2026-04-17 07:43 Uhr] **#11** Lagemeldung von „Einsatzabschnitt 1 - Nord" → „Hackathon: S2 / S5" [Low/Completed]
    > Lagemeldung Abschnitt 1 - Ausgedehnter Waldbrand mit Flammenhöhe 10m im Einsatzabschnitt Nord. Fläche aktuell mehr als 500qm. Brandbekämpfung mit einem Wasserstransportzug mit 4 TLF eingeleitet.
  - [2026-04-17 08:30 Uhr] **#11.1** System von „Hackathon: S2 / S5" → „Einsatzabschnitt 1 - Nord" [Low/Unopen]
    > Lagemeldung in Lagebericht übernommen

**Einsatzabschnitt 2 - Süd** (Sector)
- Funkrufname: 16-LZ-1
- Position: Oberbiberger Straße, 82041, Perlacher Forst, Bayern
- Abteilung: –
- Einsatzmittel (3):
  - **13-LZ-2** [LZ - FW/Fire] Status: Mission
  - **16-LZ-1** [LZ - FW/Fire] Status: Mission
  - **13-KTW-2** [KTW/EMS] Status: Mission

**Einsatzabschnitt 3 - West** (Sector)
- Funkrufname: 2-ELW2-1
- Position: Grenz Geräumt, 82041, Perlacher Forst, Bayern
- Abteilung: –
- Einsatzmittel (6):
  - **38-FGrE-1** [FGr E/Usar] Status: Mission
  - **51-FGrR-C-1** [FGr-R-C/Usar] Status: Mission
  - **36-FGrB-1** [FGr B/Usar] Status: Mission
  - **37-FGrBrB1-1** [FGr BrB/Usar] Status: Mission
  - **2-ELW2-1** [ELW 2/Fire] Status: Mission
  - **50-FGrR-B-1** [FGr-R-B/Usar] Status: Mission
- Nachrichten (4):
  - [2026-04-17 07:36 Uhr] **#5** System von „Hackathon: S4" → „Einsatzabschnitt 3 - West" [Normal/Unopen]
    > Einsatz: Abschnitt hinzufügen Name: UEA 3.1 Bavaria Studios
  - [2026-04-17 07:44 Uhr] **#12** Lagemeldung von „Einsatzabschnitt 3 - West" → „Einsatzleitung" [Low/Unopen]
    > Lagemeldung Abschnitt West - Wind treibt Feuer in Richtung der Bavaria Studios - Einsatzabschnitt 3.1 gebildet um Gebit zu schützen. Nachforderungen folgen.
  - [2026-04-17 07:44 Uhr] **#12.1** System von „Einsatzabschnitt 3 - West" → „Einsatzleitung
(Hackathon: S2 / S5)" [Low/Completed]
    > Lagemeldung: Lagemeldung Abschnitt West - Wind treibt Feuer in Richtung der Bavaria Studios - Einsatzabschnitt 3.1 gebildet um Gebit zu schützen. Nachforderungen folgen.
  - [2026-04-17 08:30 Uhr] **#12.1.1** System von „Hackathon: S2 / S5" → „Einsatzabschnitt 3 - West" [Normal/Open]
    >

**UEA 3.1 Bavaria Studios** (Sector)
- Position: Solubia
- Abteilung: –
- Nachrichten (2):
  - [2026-04-17 10:10 Uhr] **#49** Nachforderung von „UEA 3.1 Bavaria Studios" → „Einsatzleitung" [Normal/Unopen]
    > Dringend Kräfte zum Schutz der Bavaria Studios benötigt.  Aktuell Werkfeuerwehr mit 1 LZ im Einsatz.   Nachforderung:  2 LZ  Material zur Vegetationsbrandbekämpfung für mind. 2 Gruppen.   Wassertransportzüge und Flatbhälter zur Wasserreserver benötigt.
  - [2026-04-17 10:10 Uhr] **#49.1** System von „UEA 3.1 Bavaria Studios" → „Einsatzleitung
(Hackathon: S2 / S5)" [Normal/Unopen]
    > Nachforderung: Dringend Kräfte zum Schutz der Bavaria Studios benötigt.  Aktuell Werkfeuerwehr mit 1 LZ im Einsatz.   Nachforderung:  2 LZ  Material zur Vegetationsbrandbekämpfung für mind. 2 Gruppen.   Wassertransportzüge und Flatbhälter zur Wasserreserver benötigt.

**Logistik & Versorgung** (Sector)
- Position: Unterhachinger Straße, 85521, Ottobrunn, Bayern
- Abteilung: –
- Einsatzmittel (1):
  - **LOG V 1 ** [FGr-Log-V/Usar] Status: Mission

#### Alle Einsatzmittel (39 gesamt)

**Status: Staging** (10)

| Einheit | Typ | Service | Funkrufname |
|---------|-----|---------|-------------|
| 3-ELW2-1 | ELW 2 | Other | – |
| 10-TLF-5 | TLF | Fire | 10-TLF-5 |
| 8. Brandschutzbereitschaft Schleswig-Holstein | FwBer | Fire | 8. BSB SH |
| 10-TLF-6 | TLF | Fire | 10-TLF-6 |
| Fgr N MUC 1 | FGr N | Usar | – |
| Streife 1  | Streife | Police | Peter EC 1  |
| FGR N MUC 2 | FGr N | Usar | – |
| Streife 2  | Streife | Police | Peter EC 2 |
| 10-TLF-7 | TLF | Fire | 10-TLF-7 |
| 1. Brandschutzbereitschaft Schleswig-Holstein | FwBer | Fire | 1. BSB SH  |

**Status: Available** (13)

| Einheit | Typ | Service | Funkrufname |
|---------|-----|---------|-------------|
| 10-AB-Wasser-1 | WLF + AB | Fire | 10-AB-Wasser-1 |
| EC NEF 1  | NEF | EMS | Ret EC 1-82-1 |
| 12-MTF-1 | MTF | Fire | 12-MTF-1 |
| EC NEF 2 | NEF | EMS | Ret EC 2-82-1 |
| 10-AB-Schlauch-1 | WLF + AB | Fire | 10-AB-Schlauch-1 |
| 10-WLF-1 | WLF + AB | Fire | 10-WLF-1 |
| EC NEF 3 | NEF | EMS | Ret EC 3-82-1 |
| EC HLF 20 - 1  | HLF 20 | Fire | Flo EC 1-48-1 |
| EC HLF 20 - 2 | HLF 20 | Fire | Flo EC 1-48-2 |
| 13-KTW-1 | KTW | EMS | 13-KTW-1 |
| 11-LZ-1 | LZ - FW | Fire | 11-LZ-1 |
| EC HLF 20 - 3 | HLF 20 | Fire | Flo EC 1-48-8 |
| 10-TLF-8 | TLF | Fire | 10-TLF-8 |

**Status: Mission** (16)

| Einheit | Typ | Service | Funkrufname |
|---------|-----|---------|-------------|
| 38-FGrE-1 | FGr E | Usar | 38-FGrE-1 |
| 1-ELW2-1 | ELW 2 | Fire | 1-ELW2-1 |
| 51-FGrR-C-1 | FGr-R-C | Usar | 51-FGrR-C-1 |
| 13-LZ-2 | LZ - FW | Fire | 13-LZ-2 |
| LOG V 1  | FGr-Log-V | Usar | – |
| 16-LZ-1 | LZ - FW | Fire | 16-LZ-1 |
| FloEC 10-11-01 | ELW 1 | Fire | FloEC 10-11-01 |
| 36-FGrB-1 | FGr B | Usar | 36-FGrB-1 |
| 37-FGrBrB1-1 | FGr BrB | Usar | 37-FGrBrB1-1 |
| 2-ELW2-1 | ELW 2 | Fire | 2-ELW2-1 |
| 10-TLF-4 | TLF | Fire | 10-TLF-4 |
| 10-TLF-3 | TLF | Fire | 10-TLF-3 |
| 50-FGrR-B-1 | FGr-R-B | Usar | 50-FGrR-B-1 |
| 10-TLF-1 | TLF | Fire | 10-TLF-1 |
| 13-KTW-2 | KTW | EMS | 13-KTW-2 |
| 10-TLF-2 | TLF | Fire | 10-TLF-2 |

#### Patientenübersicht (14 Personen)

| Nummer | Triage | Kategorie | Datum |
|--------|--------|-----------|-------|
| 1 | T1 (Sofortbehandlung) | AdultMale | 2026-04-17 14:17 Uhr |
| 2 | T2 (Aufgeschoben) | AdultFemale | 2026-04-17 14:17 Uhr |
| 3 | T3 (Leichtverletzt) | Senior | 2026-04-17 14:17 Uhr |
| 4 | T2 (Aufgeschoben) | AdultFemale | 2026-04-17 14:17 Uhr |
| 5 | T4 (Verstorben/Hoffnungslos) | AdultFemale | 2026-04-17 14:17 Uhr |
| 6 | T1 (Sofortbehandlung) | AdultMale | 2026-04-17 14:18 Uhr |
| 7 | T3 (Leichtverletzt) | AdultMale | 2026-04-17 14:18 Uhr |
| 8 | T3 (Leichtverletzt) | AdultMale | 2026-04-17 14:18 Uhr |
| 9 | ohne Triage | AdultMale | 2026-04-17 14:18 Uhr |
| 10 | ohne Triage | AdultMale | 2026-04-17 14:18 Uhr |
| 11 | ohne Triage | AdultMale | 2026-04-17 14:18 Uhr |
| 12 | ohne Triage | AdultMale | 2026-04-17 14:18 Uhr |
| 13 | ohne Triage | AdultMale | 2026-04-17 14:18 Uhr |
| 14 | Psychosoziale Betreuung | AdultMale | 2026-04-17 14:18 Uhr |

**Triage-Zusammenfassung:**
- T1 (Sofortbehandlung): **2**
- T2 (Aufgeschoben): **2**
- T3 (Leichtverletzt): **3**
- T4 (Verstorben/Hoffnungslos): **1**
- ohne Triage: **5**
- Psychosoziale Betreuung: **1**

#### Nachrichtenverkehr gesamt (170 Nachrichten)

**System** (137)

- [2026-04-17 07:30 Uhr] **#1** von „Hackathon: S3 / S6" → „Leitstelle" [Normal/Unopen]
  > Einsatz: Bereitstellungsraum hinzufügen Name: Bereitstellungsraum 1
- [2026-04-17 07:30 Uhr] **#1.1** von „Hackathon: S3 / S6" → „Leitstelle
(Hackathon: S2 / S5)" [Normal/Completed]
  > Einsatz: Bereitstellungsraum hinzufügen Name: Bereitstellungsraum 1
- [2026-04-17 07:33 Uhr] **#2** von „Hackathon: S3 / S6" → „Leitstelle" [Normal/Unopen]
  > Einsatz: Abschnitt hinzufügen Name: Einsatzabschnitt 2 - Süd
- [2026-04-17 07:33 Uhr] **#3** von „Hackathon: S3 / S6" → „Bereitstellungsraum 1" [Normal/Unopen]
  > Einsatz: Abschnitt hinzufügen Name: Einsatzabschnitt 2 - Süd
- [2026-04-17 07:33 Uhr] **#4** von „Hackathon: S3 / S6" → „AL1" [Normal/Completed]
  > Einsatz: Abschnitt hinzufügen Name: Einsatzabschnitt 2 - Süd
- [2026-04-17 07:33 Uhr] **#2.1** von „Hackathon: S3 / S6" → „Leitstelle,
Bereitstellungsraum 1,
AL1
(Hackathon: S2 / S5)" [Normal/Completed]
  > Einsatz: Abschnitt hinzufügen Name: Einsatzabschnitt 2 - Süd
- [2026-04-17 07:36 Uhr] **#5** von „Hackathon: S4" → „Einsatzabschnitt 3 - West" [Normal/Unopen]
  > Einsatz: Abschnitt hinzufügen Name: UEA 3.1 Bavaria Studios
- [2026-04-17 07:36 Uhr] **#5.1** von „Hackathon: S4" → „Einsatzabschnitt 3 - West
(Hackathon: S2 / S5)" [Normal/Completed]
  > Einsatz: Abschnitt hinzufügen Name: UEA 3.1 Bavaria Studios
- [2026-04-17 07:37 Uhr] **#6** von „Hackathon: S4" → „1-ELW2-1" [Normal/Unopen]
  > Führung des Einsatzabschnittes 1 Nord - Kräfte werden zugewiesen
- [2026-04-17 07:37 Uhr] **#6.1** von „Hackathon: S4" → „1-ELW2-1
(Hackathon: S2 / S5)" [Normal/Completed]
  > Führung des Einsatzabschnittes 1 Nord - Kräfte werden zugewiesen
- [2026-04-17 07:38 Uhr] **#7** von „Hackathon: S3 / S6" → „10-TLF-2" [Normal/Unopen]
  > Zusammführung als Wasserransportzug im Abschnitt 1 - Ansprechpartner 1-ELW 2-1
- [2026-04-17 07:38 Uhr] **#7.1** von „Hackathon: S3 / S6" → „10-TLF-2
(Hackathon: S2 / S5)" [Normal/Completed]
  > Zusammführung als Wasserransportzug im Abschnitt 1 - Ansprechpartner 1-ELW 2-1
- [2026-04-17 07:38 Uhr] **#8** von „Hackathon: S3 / S6" → „10-TLF-7" [Normal/Unopen]
  > Pause zur Bereitstellung in BR 1
- [2026-04-17 07:38 Uhr] **#8.1** von „Hackathon: S3 / S6" → „10-TLF-7
(Hackathon: S2 / S5)" [Normal/Completed]
  > Pause zur Bereitstellung in BR 1
- [2026-04-17 07:39 Uhr] **#9** von „Hackathon: S3 / S6" → „2-ELW2-1" [Normal/Unopen]
  > Führung Einsatzabschnitt - West
- [2026-04-17 07:39 Uhr] **#9.1** von „Hackathon: S3 / S6" → „2-ELW2-1
(Hackathon: S2 / S5)" [Normal/Completed]
  > Führung Einsatzabschnitt - West
- [2026-04-17 07:40 Uhr] **#10** von „Hackathon: S3 / S6" → „13-KTW-2" [Normal/Unopen]
  > Kräftezuführung zu EA 2 - Süd - Eintreffzeit geplant 23:30
- [2026-04-17 07:40 Uhr] **#10.1** von „Hackathon: S3 / S6" → „13-KTW-2
(Hackathon: S2 / S5)" [Normal/Completed]
  > Kräftezuführung zu EA 2 - Süd - Eintreffzeit geplant 23:30
- [2026-04-17 07:44 Uhr] **#12.1** von „Einsatzabschnitt 3 - West" → „Einsatzleitung
(Hackathon: S2 / S5)" [Low/Completed]
  > Lagemeldung: Lagemeldung Abschnitt West - Wind treibt Feuer in Richtung der Bavaria Studios - Einsatzabschnitt 3.1 gebildet um Gebit zu schützen. Nachforderungen folgen.
- [2026-04-17 07:46 Uhr] **#14** von „Hackathon: FüAss AL" → „50-FGrR-B-1" [Normal/Unopen]
  > Ressourcen: 38-FGrE-1 38-FGrE-1, 51-FGrR-C-1 51-FGrR-C-1, 36-FGrB-1 36-FGrB-1, 37-FGrBrB1-1 37-FGrBrB1-1, 50-FGrR-B-1 50-FGrR-B-1 Verschieben in Abschnitt: Einsatzabschnitt 3 - West - EA 3 Adresse: Grenz Geräumt, 82041, Perlacher Forst, Bayern Koordinaten: 48.06, 11.56
 Nach Ankunft bei EAL 2-ELW2-1 melden
- [2026-04-17 07:46 Uhr] **#14.1** von „Hackathon: FüAss AL" → „50-FGrR-B-1
(Hackathon: S2 / S5)" [Normal/Completed]
  > Ressourcen: 38-FGrE-1 38-FGrE-1, 51-FGrR-C-1 51-FGrR-C-1, 36-FGrB-1 36-FGrB-1, 37-FGrBrB1-1 37-FGrBrB1-1, 50-FGrR-B-1 50-FGrR-B-1 Verschieben in Abschnitt: Einsatzabschnitt 3 - West - EA 3 Adresse: Grenz Geräumt, 82041, Perlacher Forst, Bayern Koordinaten: 48.06, 11.56
 Nach Ankunft bei EAL 2-ELW2-1 melden
- [2026-04-17 07:47 Uhr] **#15.1** von „Hackathon: S3 / S6" → „Hackathon: S4
(Hackathon: S2 / S5)" [Low/Completed]
  > Notiz: Aktuell über 200 Kräfte im Einsatz - Verpflegung wird alle 4 Stunden für alle Kräfte benötigt. Verpflegung muss auf Abschnitte verteilt werden. Zentraler Verpflegungspunkt am BR1 in aufzubauen.
- [2026-04-17 07:48 Uhr] **#16.1** von „Hackathon: S4" → „Leitstelle
(Hackathon: S2 / S5)" [Normal/Completed]
  > Nachforderung: Anforderung 2 Gruppen Betreuung 2 Fachgruppe N zum BR1 zum Betrieb des BR und Verpflegung der Kräfte - Einsatzdauer vermutlich 48 Stunden.
- [2026-04-17 07:50 Uhr] **#17** von „Hackathon: Leitung Stab" → „Hackathon: S4" [null/Completed]
  > Anforderung Kraftstoffe und Verteilung in allen Einsatzabschnitten
- [2026-04-17 07:50 Uhr] **#17.1** von „Hackathon: Leitung Stab" → „Hackathon: S4
(Hackathon: S2 / S5)" [Low/Completed]
  > Anforderung Kraftstoffe und Verteilung in allen Einsatzabschnitten
- [2026-04-17 07:51 Uhr] **#18** von „Hackathon: Leitung Stab" → „Hackathon: S1" [null/InProgress]
  > Planung Austausch Stabspersonal Stab Hackathon
- [2026-04-17 07:51 Uhr] **#18.1** von „Hackathon: Leitung Stab" → „Hackathon: S1
(Hackathon: S2 / S5)" [Low/Completed]
  > Planung Austausch Stabspersonal Stab Hackathon
- [2026-04-17 07:52 Uhr] **#19** von „Hackathon: Leitung Stab" → „Hackathon: FüAss AL" [null/Unopen]
  > Aufbau zentraler Stellen zur Wasserentnahme für Wasserstransportzüge für alle Einsatzabschnitte
- [2026-04-17 07:52 Uhr] **#19.1** von „Hackathon: Leitung Stab" → „Hackathon: FüAss AL
(Hackathon: S2 / S5)" [Low/Completed]
  > Aufbau zentraler Stellen zur Wasserentnahme für Wasserstransportzüge für alle Einsatzabschnitte
- [2026-04-17 07:53 Uhr] **#20** von „Hackathon: Leitung Stab" → „Hackathon: S1" [null/Unopen]
  > Verpflegung Stabspersonal
- [2026-04-17 07:53 Uhr] **#20.1** von „Hackathon: Leitung Stab" → „Hackathon: S1
(Hackathon: S2 / S5)" [Low/Completed]
  > Verpflegung Stabspersonal
- [2026-04-17 07:55 Uhr] **#21.1** von „Hackathon: S2 / S5" → „An alle: AL1,
An alle: BR ,
An alle: Hackathon
(AL1: S2 / S5)" [High/Unopen]
  > Eilmeldung: Wetterinformationen 17.04.2026 9:50:  Temperatur 13°C  Niederschlag: 0% Luftfeuchte: 63% Wind: 5 km/h  Aussicht:  Wind wird in den nächsten Stunden auffrischen. Wind von Ost nach West.   Lageentwicklung ist abzuwarten und zu bewerten.
- [2026-04-17 07:55 Uhr] **#23.1** von „Hackathon: S2 / S5" → „Hackathon: S2 / S5" [High/Unknown]
  >
- [2026-04-17 07:56 Uhr] **#4.1** von „AL1: FüAss AL" → „Hackathon: S3 / S6" [Normal/Unopen]
  > Änderung belannt.
- [2026-04-17 07:56 Uhr] **#4.1.1** von „AL1: FüAss AL" → „Hackathon: S3 / S6
(AL1: S2 / S5)" [Normal/Unopen]
  > Änderung belannt.
- [2026-04-17 07:56 Uhr] **#4.1.2** von „AL1: FüAss AL" → „Hackathon: S3 / S6
(Hackathon: S2 / S5)" [Normal/Completed]
  > Änderung belannt.
- [2026-04-17 07:57 Uhr] **#21.2** von „AL1: FüAss AL" → „Hackathon: S2 / S5" [High/Completed]
  > Für die Abschnittsleitung alle 2 Stunden Update zum Wetter erwartet.
- [2026-04-17 07:57 Uhr] **#21.2.1** von „AL1: FüAss AL" → „Hackathon: S2 / S5
(AL1: S2 / S5)" [High/Unopen]
  > Für die Abschnittsleitung alle 2 Stunden Update zum Wetter erwartet.
- [2026-04-17 07:58 Uhr] **#24.1** von „AL1: FüAss AL" → „Einsatzleitung
(AL1: S2 / S5)" [Low/Unopen]
  > Anfrage: Anfrage Wetterinformationen alle 2 Stunden für die Abschnittsleitung 1.
- [2026-04-17 08:00 Uhr] **#25.1** von „AL1: FüAss AL" → „Hackathon
(AL1: S2 / S5)" [Low/Unopen]
  > Anfrage: Gibt es Informationen zur Begahrbarkeit von Wegen im Waldgebiet?
- [2026-04-17 08:00 Uhr] **#25.2** von „AL1: FüAss AL" → „Hackathon
(Hackathon: S2 / S5)" [Low/Completed]
  > Anfrage: Gibt es Informationen zur Begahrbarkeit von Wegen im Waldgebiet?
- [2026-04-17 08:01 Uhr] **#26.1** von „AL1: FüAss AL" → „Hackathon
(AL1: S2 / S5)" [High/Unopen]
  > Eilmeldung: Kräfte aktuell vom Feuer an angehäängter Position eingeschlossen.
- [2026-04-17 08:01 Uhr] **#26.2** von „AL1: FüAss AL" → „Hackathon
(Hackathon: S2 / S5)" [High/Completed]
  > Eilmeldung: Kräfte aktuell vom Feuer an angehäängter Position eingeschlossen.
- [2026-04-17 08:01 Uhr] **#27.1** von „AL1: FüAss AL" → „Hackathon
(AL1: S2 / S5)" [Low/Unopen]
  > Sonstiges: Wasserentnahmestelle am Hydrantennetz nicht nutzbar. Defekt.
- [2026-04-17 08:01 Uhr] **#27.2** von „AL1: FüAss AL" → „Hackathon
(Hackathon: S2 / S5)" [Low/Completed]
  > Sonstiges: Wasserentnahmestelle am Hydrantennetz nicht nutzbar. Defekt.
- [2026-04-17 08:02 Uhr] **#28.1** von „AL1: FüAss AL" → „Hackathon
(AL1: S2 / S5)" [Low/Unopen]
  > Anfrage: Übermitteln Sie aktuelle Verfügbarkeit von Wasserentnahmestellen für Einsatzabschnitt 1
- [2026-04-17 08:02 Uhr] **#28.2** von „AL1: FüAss AL" → „Hackathon
(Hackathon: S2 / S5)" [Low/Completed]
  > Anfrage: Übermitteln Sie aktuelle Verfügbarkeit von Wasserentnahmestellen für Einsatzabschnitt 1
- [2026-04-17 08:03 Uhr] **#29.1** von „AL1: FüAss AL" → „Hackathon
(AL1: S2 / S5)" [Low/Unopen]
  > Lagemeldung: Lagemeldung aus Abschnitt 1:  Feuer auf einer Flächen von 1ha.  Feuer nicht unter Kontrolle.   Aktueller Einsatz: Mit Wasserstransportzug Wasser zu einzenen Stelle zu liefern und Schneisen zu schlagen.
- [2026-04-17 08:03 Uhr] **#29.2** von „AL1: FüAss AL" → „Hackathon
(Hackathon: S2 / S5)" [Low/Completed]
  > Lagemeldung: Lagemeldung aus Abschnitt 1:  Feuer auf einer Flächen von 1ha.  Feuer nicht unter Kontrolle.   Aktueller Einsatz: Mit Wasserstransportzug Wasser zu einzenen Stelle zu liefern und Schneisen zu schlagen.
- [2026-04-17 08:04 Uhr] **#30** von „Hackathon: Übungsleitung" → „Hackathon: S2 / S5" [null/Unopen]
  > Vorplanung Lagebesprechung 16.00 Uhr
- [2026-04-17 08:04 Uhr] **#31.1** von „AL1: FüAss AL" → „Bereitstellungsraum 1
(AL1: S2 / S5)" [Normal/Unopen]
  > Nachforderung: Anforderung weiterer Kräfte:  5 Tanklöschfahrzeuge für EInsatzabschnitt1 benötigt.
- [2026-04-17 08:05 Uhr] **#22.1** von „BR : AL" → „Hackathon: S2 / S5" [High/Unknown]
  >
- [2026-04-17 08:07 Uhr] **#32.1** von „BR : AL" → „Einsatzleitung
(BR : S2 / S5)" [Normal/Unopen]
  > Nachforderung: Anforderungen für BR 1:  - Mobile Tankstelle Diesel 2000l und regelmäßige Befüllung - AdBlue  - Personal zum Betrieb des BR 1 Zug Verpflegung, 2 Fachgruppen N THW
- [2026-04-17 08:07 Uhr] **#32.2** von „BR : AL" → „Einsatzleitung
(Hackathon: S2 / S5)" [Normal/Completed]
  > Nachforderung: Anforderungen für BR 1:  - Mobile Tankstelle Diesel 2000l und regelmäßige Befüllung - AdBlue  - Personal zum Betrieb des BR 1 Zug Verpflegung, 2 Fachgruppen N THW
- [2026-04-17 08:15 Uhr] **#33.1** von „BR : AL" → „Einsatzleitung
(BR : S2 / S5)" [Low/Unopen]
  > Lagemeldung: Lagemeldung aus BR 1: Bereitstellungsraum wird aufgebaut.  Aktuelle Planungen gegen von 250 Kräften aus.   Für Externe Kräfte aus Norddeutschland werden Sammelräume zum Abruf in der Nähe der Autobahn benötigt.
- [2026-04-17 08:15 Uhr] **#33.2** von „BR : AL" → „Einsatzleitung
(Hackathon: S2 / S5)" [Low/Completed]
  > Lagemeldung: Lagemeldung aus BR 1: Bereitstellungsraum wird aufgebaut.  Aktuelle Planungen gegen von 250 Kräften aus.   Für Externe Kräfte aus Norddeutschland werden Sammelräume zum Abruf in der Nähe der Autobahn benötigt.
- [2026-04-17 08:16 Uhr] **#34.1** von „BR : AL" → „
(BR : S2 / S5)" [Low/Unopen]
  > Notiz: Meldkopf BR ist einzurichen. Es ist ein System einzuführen Kräfte am Meldekopf zu getrieren und dem BR zuzuweisen. Verantwortlich: Meldekopf.
- [2026-04-17 08:17 Uhr] **#26.3.1** von „AL1: FüAss AL" → „2026-3 - Hackathon: S3 / S6
(AL1: S2 / S5)" [High/Unopen]
  > Eilmeldung: Kräfte aktuell vom Feuer an angehäängter Position eingeschlossen.
- [2026-04-17 08:17 Uhr] **#26.3.2** von „AL1: FüAss AL" → „2026-3 - Hackathon: S3 / S6
(Hackathon: S2 / S5)" [High/Completed]
  > Eilmeldung: Kräfte aktuell vom Feuer an angehäängter Position eingeschlossen.
- [2026-04-17 08:18 Uhr] **#32.3.1** von „BR : AL" → „2026-3 - Hackathon: S1
(BR : S2 / S5)" [Normal/Unopen]
  > Nachforderung: Anforderungen für BR 1:  - Mobile Tankstelle Diesel 2000l und regelmäßige Befüllung - AdBlue  - Personal zum Betrieb des BR 1 Zug Verpflegung, 2 Fachgruppen N THW
- [2026-04-17 08:18 Uhr] **#32.3.2** von „BR : AL" → „2026-3 - Hackathon: S1
(Hackathon: S2 / S5)" [Normal/Completed]
  > Nachforderung: Anforderungen für BR 1:  - Mobile Tankstelle Diesel 2000l und regelmäßige Befüllung - AdBlue  - Personal zum Betrieb des BR 1 Zug Verpflegung, 2 Fachgruppen N THW
- [2026-04-17 08:18 Uhr] **#25.3.1** von „AL1: FüAss AL" → „2026-3 - Hackathon: S3 / S6
(AL1: S2 / S5)" [Low/Unopen]
  > Anfrage: Gibt es Informationen zur Begahrbarkeit von Wegen im Waldgebiet?
- [2026-04-17 08:18 Uhr] **#25.3.2** von „AL1: FüAss AL" → „2026-3 - Hackathon: S3 / S6
(Hackathon: S2 / S5)" [Low/Completed]
  > Anfrage: Gibt es Informationen zur Begahrbarkeit von Wegen im Waldgebiet?
- [2026-04-17 08:18 Uhr] **#27.3.1** von „AL1: FüAss AL" → „2026-3 - Hackathon: S2 / S5
(AL1: S2 / S5)" [Low/Unopen]
  > Sonstiges: Wasserentnahmestelle am Hydrantennetz nicht nutzbar. Defekt.
- [2026-04-17 08:18 Uhr] **#28.3.1** von „AL1: FüAss AL" → „2026-3 - Hackathon: S2 / S5
(AL1: S2 / S5)" [Low/Unopen]
  > Anfrage: Übermitteln Sie aktuelle Verfügbarkeit von Wasserentnahmestellen für Einsatzabschnitt 1
- [2026-04-17 08:18 Uhr] **#29.3.1** von „AL1: FüAss AL" → „2026-3 - Hackathon: S2 / S5
(AL1: S2 / S5)" [Low/Unopen]
  > Lagemeldung: Lagemeldung aus Abschnitt 1:  Feuer auf einer Flächen von 1ha.  Feuer nicht unter Kontrolle.   Aktueller Einsatz: Mit Wasserstransportzug Wasser zu einzenen Stelle zu liefern und Schneisen zu schlagen.
- [2026-04-17 08:18 Uhr] **#33.3.1** von „BR : AL" → „2026-3 - Hackathon: S2 / S5
(BR : S2 / S5)" [Low/Unopen]
  > Lagemeldung: Lagemeldung aus BR 1: Bereitstellungsraum wird aufgebaut.  Aktuelle Planungen gegen von 250 Kräften aus.   Für Externe Kräfte aus Norddeutschland werden Sammelräume zum Abruf in der Nähe der Autobahn benötigt.
- [2026-04-17 08:19 Uhr] **#17.2** von „Hackathon: S4" → „Hackathon: Leitung Stab" [Normal/Open]
  > Anforderungen werden zentral über neuen Abschnitt koordiniert. Mit S3 neuen Abschnitt definieren und Kräfte in Abstimmung mit S1 zuweisen.
- [2026-04-17 08:19 Uhr] **#17.2.1** von „Hackathon: S4" → „Hackathon: Leitung Stab
(Hackathon: S2 / S5)" [Normal/Completed]
  > Anforderungen werden zentral über neuen Abschnitt koordiniert. Mit S3 neuen Abschnitt definieren und Kräfte in Abstimmung mit S1 zuweisen.
- [2026-04-17 08:21 Uhr] **#35** von „Hackathon: S4" → „Leitstelle" [Normal/Unopen]
  > Einsatz: Abschnitt hinzufügen Name: Logistik & Versorgung
 Aufbau zentrale Versorgung und Logistik für alle Abschnitte.
- [2026-04-17 08:21 Uhr] **#36** von „Hackathon: S4" → „BR " [Normal/Unopen]
  > Einsatz: Abschnitt hinzufügen Name: Logistik & Versorgung
 Aufbau zentrale Versorgung und Logistik für alle Abschnitte.
- [2026-04-17 08:21 Uhr] **#37** von „Hackathon: S4" → „AL1" [Normal/Unopen]
  > Einsatz: Abschnitt hinzufügen Name: Logistik & Versorgung
 Aufbau zentrale Versorgung und Logistik für alle Abschnitte.
- [2026-04-17 08:21 Uhr] **#38** von „Hackathon: S4" → „16-LZ-1" [Normal/Unopen]
  > Einsatz: Abschnitt hinzufügen Name: Logistik & Versorgung
 Aufbau zentrale Versorgung und Logistik für alle Abschnitte.
- [2026-04-17 08:21 Uhr] **#39** von „Hackathon: S4" → „2-ELW2-1" [Normal/Unopen]
  > Einsatz: Abschnitt hinzufügen Name: Logistik & Versorgung
 Aufbau zentrale Versorgung und Logistik für alle Abschnitte.
- [2026-04-17 08:21 Uhr] **#35.1** von „Hackathon: S4" → „Leitstelle,
BR ,
AL1,
16-LZ-1,
2-ELW2-1
(Hackathon: S2 / S5)" [Normal/Completed]
  > Einsatz: Abschnitt hinzufügen Name: Logistik & Versorgung
 Aufbau zentrale Versorgung und Logistik für alle Abschnitte.
- [2026-04-17 08:22 Uhr] **#17.3** von „Hackathon: S4" → „Hackathon: Leitung Stab" [Normal/Unopen]
  > EA 4 gebildet - Aufbau zentrale Logistik und Versorgung für alle Bereiche.   Anforrderungen aus EA 4 an Stab S4
- [2026-04-17 08:22 Uhr] **#17.3.1** von „Hackathon: S4" → „Hackathon: Leitung Stab
(Hackathon: S2 / S5)" [Normal/Completed]
  > EA 4 gebildet - Aufbau zentrale Logistik und Versorgung für alle Bereiche.   Anforrderungen aus EA 4 an Stab S4
- [2026-04-17 08:27 Uhr] **#41** von „Hackathon: S2 / S5" → „null" [Low/Completed]
  > Nächste Lagebesprechung 12:00
- [2026-04-17 08:27 Uhr] **#42** von „Hackathon: S2 / S5" → „null" [Low/Completed]
  > Außergewöhnliches Ereignis 17.04.2026 10:27:44
- [2026-04-17 08:28 Uhr] **#21.2.2** von „Hackathon: S2 / S5" → „AL1: FüAss AL" [Normal/Open]
  >
- [2026-04-17 08:28 Uhr] **#26.2.1** von „Hackathon: S2 / S5" → „AL1: FüAss AL" [Normal/Open]
  >
- [2026-04-17 08:29 Uhr] **#26.3.2.1** von „Hackathon: S2 / S5" → „AL1: FüAss AL" [Normal/Open]
  >
- [2026-04-17 08:29 Uhr] **#1.1.1** von „Hackathon: S2 / S5" → „Hackathon: S3 / S6" [Normal/Open]
  >
- [2026-04-17 08:29 Uhr] **#2.1.1** von „Hackathon: S2 / S5" → „Hackathon: S3 / S6" [Normal/Open]
  >
- [2026-04-17 08:29 Uhr] **#5.1.1** von „Hackathon: S2 / S5" → „Hackathon: S4" [Normal/Open]
  >
- [2026-04-17 08:29 Uhr] **#6.1.1** von „Hackathon: S2 / S5" → „Hackathon: S4" [Normal/Open]
  >
- [2026-04-17 08:29 Uhr] **#7.1.1** von „Hackathon: S2 / S5" → „Hackathon: S3 / S6" [Normal/Open]
  >
- [2026-04-17 08:29 Uhr] **#8.1.1** von „Hackathon: S2 / S5" → „Hackathon: S3 / S6" [Normal/Open]
  >
- [2026-04-17 08:29 Uhr] **#9.1.1** von „Hackathon: S2 / S5" → „Hackathon: S3 / S6" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#10.1.1** von „Hackathon: S2 / S5" → „Hackathon: S3 / S6" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#14.1.1** von „Hackathon: S2 / S5" → „Hackathon: FüAss AL" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#4.1.2.1** von „Hackathon: S2 / S5" → „AL1: FüAss AL" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#16.1.1** von „Hackathon: S2 / S5" → „Hackathon: S4" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#32.2.1** von „Hackathon: S2 / S5" → „BR : AL" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#32.3.2.1** von „Hackathon: S2 / S5" → „BR : AL" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#17.2.1.1** von „Hackathon: S2 / S5" → „Hackathon: S4" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#35.1.1** von „Hackathon: S2 / S5" → „Hackathon: S4" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#17.3.1.1** von „Hackathon: S2 / S5" → „Hackathon: S4" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#11.1** von „Hackathon: S2 / S5" → „Einsatzabschnitt 1 - Nord" [Low/Unopen]
  > Lagemeldung in Lagebericht übernommen
- [2026-04-17 08:30 Uhr] **#12.1.1** von „Hackathon: S2 / S5" → „Einsatzabschnitt 3 - West" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#15.1.1** von „Hackathon: S2 / S5" → „Hackathon: S3 / S6" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#17.1.1** von „Hackathon: S2 / S5" → „Hackathon: Leitung Stab" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#18.1.1** von „Hackathon: S2 / S5" → „Hackathon: Leitung Stab" [Normal/Open]
  >
- [2026-04-17 08:30 Uhr] **#19.1.1** von „Hackathon: S2 / S5" → „Hackathon: Leitung Stab" [Normal/Open]
  >
- [2026-04-17 08:31 Uhr] **#20.1.1** von „Hackathon: S2 / S5" → „Hackathon: Leitung Stab" [Normal/Open]
  >
- [2026-04-17 08:31 Uhr] **#25.2.1** von „Hackathon: S2 / S5" → „AL1: FüAss AL" [Normal/Open]
  >
- [2026-04-17 08:31 Uhr] **#27.2.1** von „Hackathon: S2 / S5" → „AL1: FüAss AL" [Normal/Open]
  >
- [2026-04-17 08:31 Uhr] **#28.2.1** von „Hackathon: S2 / S5" → „AL1: FüAss AL" [Normal/Open]
  >
- [2026-04-17 08:31 Uhr] **#29.2.1** von „Hackathon: S2 / S5" → „AL1: FüAss AL" [Normal/Open]
  >
- [2026-04-17 08:31 Uhr] **#33.2.1** von „Hackathon: S2 / S5" → „BR : AL" [Normal/Open]
  >
- [2026-04-17 08:31 Uhr] **#25.3.2.1** von „Hackathon: S2 / S5" → „AL1: FüAss AL" [Normal/Open]
  >
- [2026-04-17 08:31 Uhr] **#27.3.2** von „Hackathon: S2 / S5" → „AL1: FüAss AL" [Low/Unopen]
  > Information aufgenommen
- [2026-04-17 08:31 Uhr] **#27.3.2.1** von „Hackathon: S2 / S5" → „AL1: FüAss AL
(AL1: S2 / S5)" [Low/Unopen]
  > Information aufgenommen
- [2026-04-17 08:31 Uhr] **#28.3.2** von „Hackathon: S2 / S5" → „AL1: FüAss AL" [Low/Unknown]
  >
- [2026-04-17 08:31 Uhr] **#29.3.2** von „Hackathon: S2 / S5" → „AL1: FüAss AL" [Low/Unknown]
  >
- [2026-04-17 08:32 Uhr] **#32.3.3** von „Hackathon: S1" → „BR : AL" [Normal/Unknown]
  >
- [2026-04-17 08:33 Uhr] **#32.3.4** von „Hackathon: S1" → „BR : AL" [Normal/Unopen]
  > Keine Fachgruppe N Verfügbar. LOG V dem EA 4 zugewiesen. Weitere Anforderungen über EA 4
- [2026-04-17 08:33 Uhr] **#32.3.4.1** von „Hackathon: S1" → „BR : AL
(Hackathon: S2 / S5)" [Normal/Unopen]
  > Keine Fachgruppe N Verfügbar. LOG V dem EA 4 zugewiesen. Weitere Anforderungen über EA 4
- [2026-04-17 08:33 Uhr] **#32.3.4.2** von „Hackathon: S1" → „BR : AL
(BR : S2 / S5)" [Normal/Unopen]
  > Keine Fachgruppe N Verfügbar. LOG V dem EA 4 zugewiesen. Weitere Anforderungen über EA 4
- [2026-04-17 10:01 Uhr] **#43** von „Hackathon: Leitung Stab" → „Hackathon: S1" [null/Unknown]
  > "Erinnerung CRM Meldung ID 20: Offene Aufgabe mit verstrichener Frist"
- [2026-04-17 10:05 Uhr] **#44** von „Hackathon: Leitung Stab" → „Hackathon: S1" [null/Unopen]
  > Sicherstellung Schichtbetrieb aller Funktionen
- [2026-04-17 10:05 Uhr] **#44.1** von „Hackathon: Leitung Stab" → „Hackathon: S1
(Hackathon: S2 / S5)" [Low/Unopen]
  > Sicherstellung Schichtbetrieb aller Funktionen
- [2026-04-17 10:06 Uhr] **#45** von „Hackathon: Leitung Stab" → „Hackathon: S3 / S6" [null/Unopen]
  > Netzhärtung TETRA für Einsatzgebiet
- [2026-04-17 10:06 Uhr] **#45.1** von „Hackathon: Leitung Stab" → „Hackathon: S3 / S6
(Hackathon: S2 / S5)" [Low/Unopen]
  > Netzhärtung TETRA für Einsatzgebiet
- [2026-04-17 10:06 Uhr] **#46** von „Hackathon: Leitung Stab" → „Hackathon: S3 / S6" [null/Unopen]
  > Beantragung weiterer TMO Rufgruppenblöcke
- [2026-04-17 10:06 Uhr] **#46.1** von „Hackathon: Leitung Stab" → „Hackathon: S3 / S6
(Hackathon: S2 / S5)" [Low/Unopen]
  > Beantragung weiterer TMO Rufgruppenblöcke
- [2026-04-17 10:07 Uhr] **#47** von „Hackathon: Leitung Stab" → „Hackathon: S1" [null/InProgress]
  > Sicherstellung Grunschutz
- [2026-04-17 10:07 Uhr] **#47.1** von „Hackathon: Leitung Stab" → „Hackathon: S1
(Hackathon: S2 / S5)" [Low/InProgress]
  > Sicherstellung Grunschutz
- [2026-04-17 10:10 Uhr] **#49.1** von „UEA 3.1 Bavaria Studios" → „Einsatzleitung
(Hackathon: S2 / S5)" [Normal/Unopen]
  > Nachforderung: Dringend Kräfte zum Schutz der Bavaria Studios benötigt.  Aktuell Werkfeuerwehr mit 1 LZ im Einsatz.   Nachforderung:  2 LZ  Material zur Vegetationsbrandbekämpfung für mind. 2 Gruppen.   Wassertransportzüge und Flatbhälter zur Wasserreserver benötigt.
- [2026-04-17 10:11 Uhr] **#50.1** von „Bereitstellungsraum 1" → „Einsatzleitung
(Hackathon: S2 / S5)" [Low/Unopen]
  > Anfrage: Wann treffen die 8. BSB SH und 1. BSB SH im Bereitstellungsraum an?
- [2026-04-17 10:12 Uhr] **#51.1** von „Bereitstellungsraum 1" → „Einsatzleitung
(Hackathon: S2 / S5)" [Low/Unopen]
  > Anfrage: Wie viele Kräfte befinden sich aktuell auf Anfahrt zum BR?  Gibt es eine aktuelle Übersicht angeforderter Kräfte?
- [2026-04-17 10:13 Uhr] **#52.1** von „Hackathon: S1" → „Bereitstellungsraum 1
(Hackathon: S2 / S5)" [Low/Unopen]
  > Sonstiges: Kräfte aus Schleswig-Holstein treffen am Vormittag des 18. April ein.  Detaillierte Informationen an den Informationen der Ressourcen hinterlegt.
- [2026-04-17 10:13 Uhr] **#52.2** von „Hackathon: S1" → „Bereitstellungsraum 1
(BR : S2 / S5)" [Low/Unopen]
  > Sonstiges: Kräfte aus Schleswig-Holstein treffen am Vormittag des 18. April ein.  Detaillierte Informationen an den Informationen der Ressourcen hinterlegt.
- [2026-04-17 10:13 Uhr] **#18.2** von „Hackathon: S1" → „Hackathon: Leitung Stab" [Normal/Unknown]
  >
- [2026-04-17 11:16 Uhr] **#55** von „Hackathon: Leitung Stab" → „Hackathon: FüAss AL" [null/Unknown]
  > "Erinnerung CRM Meldung ID 19: Offene Aufgabe mit verstrichener Frist"
- [2026-04-17 13:01 Uhr] **#56** von „Hackathon: Leitung Stab" → „Hackathon: S3 / S6" [null/Unknown]
  > "Erinnerung CRM Meldung ID 46: Offene Aufgabe mit verstrichener Frist"
- [2026-04-17 13:31 Uhr] **#57** von „Hackathon: Übungsleitung" → „Hackathon: S2 / S5" [null/Unknown]
  > "Erinnerung CRM Meldung ID 30: Offene Aufgabe mit verstrichener Frist"

**Anfrage** (8)

- [2026-04-17 07:58 Uhr] **#24** von „AL1: FüAss AL" → „Einsatzleitung" [Low/Open]
  > Anfrage Wetterinformationen alle 2 Stunden für die Abschnittsleitung 1.
- [2026-04-17 08:00 Uhr] **#25** von „AL1: FüAss AL" → „Hackathon" [Low/Forwarded]
  > Gibt es Informationen zur Begahrbarkeit von Wegen im Waldgebiet?
- [2026-04-17 08:02 Uhr] **#28** von „AL1: FüAss AL" → „Hackathon" [Low/Forwarded]
  > Übermitteln Sie aktuelle Verfügbarkeit von Wasserentnahmestellen für Einsatzabschnitt 1
- [2026-04-17 08:18 Uhr] **#25.3** von „AL1: FüAss AL" → „2026-3 - Hackathon: S3 / S6" [Low/Unopen]
  > Gibt es Informationen zur Begahrbarkeit von Wegen im Waldgebiet?
- [2026-04-17 08:18 Uhr] **#28.3** von „AL1: FüAss AL" → „2026-3 - Hackathon: S2 / S5" [Low/Completed]
  > Übermitteln Sie aktuelle Verfügbarkeit von Wasserentnahmestellen für Einsatzabschnitt 1
- [2026-04-17 10:11 Uhr] **#50** von „Bereitstellungsraum 1" → „Einsatzleitung" [Low/Unopen]
  > Wann treffen die 8. BSB SH und 1. BSB SH im Bereitstellungsraum an?
- [2026-04-17 10:12 Uhr] **#51** von „Bereitstellungsraum 1" → „Einsatzleitung" [Low/Unopen]
  > Wie viele Kräfte befinden sich aktuell auf Anfahrt zum BR?  Gibt es eine aktuelle Übersicht angeforderter Kräfte?
- [2026-04-17 10:16 Uhr] **#54** von „Hackathon: S2 / S5" → „Leitstelle" [Low/Unopen]
  > Anfrage aktuelle Wetterinformationen und Vorhersage.

**Lagemeldung** (6)

- [2026-04-17 07:43 Uhr] **#11** von „Einsatzabschnitt 1 - Nord" → „Hackathon: S2 / S5" [Low/Completed]
  > Lagemeldung Abschnitt 1 - Ausgedehnter Waldbrand mit Flammenhöhe 10m im Einsatzabschnitt Nord. Fläche aktuell mehr als 500qm. Brandbekämpfung mit einem Wasserstransportzug mit 4 TLF eingeleitet.
- [2026-04-17 07:44 Uhr] **#12** von „Einsatzabschnitt 3 - West" → „Einsatzleitung" [Low/Unopen]
  > Lagemeldung Abschnitt West - Wind treibt Feuer in Richtung der Bavaria Studios - Einsatzabschnitt 3.1 gebildet um Gebit zu schützen. Nachforderungen folgen.
- [2026-04-17 08:03 Uhr] **#29** von „AL1: FüAss AL" → „Hackathon" [Low/Forwarded]
  > Lagemeldung aus Abschnitt 1:  Feuer auf einer Flächen von 1ha.  Feuer nicht unter Kontrolle.   Aktueller Einsatz: Mit Wasserstransportzug Wasser zu einzenen Stelle zu liefern und Schneisen zu schlagen.
- [2026-04-17 08:15 Uhr] **#33** von „BR : AL" → „Einsatzleitung" [Low/Forwarded]
  > Lagemeldung aus BR 1: Bereitstellungsraum wird aufgebaut.  Aktuelle Planungen gegen von 250 Kräften aus.   Für Externe Kräfte aus Norddeutschland werden Sammelräume zum Abruf in der Nähe der Autobahn benötigt.
- [2026-04-17 08:18 Uhr] **#29.3** von „AL1: FüAss AL" → „2026-3 - Hackathon: S2 / S5" [Low/Completed]
  > Lagemeldung aus Abschnitt 1:  Feuer auf einer Flächen von 1ha.  Feuer nicht unter Kontrolle.   Aktueller Einsatz: Mit Wasserstransportzug Wasser zu einzenen Stelle zu liefern und Schneisen zu schlagen.
- [2026-04-17 08:18 Uhr] **#33.3** von „BR : AL" → „2026-3 - Hackathon: S2 / S5" [Low/Unopen]
  > Lagemeldung aus BR 1: Bereitstellungsraum wird aufgebaut.  Aktuelle Planungen gegen von 250 Kräften aus.   Für Externe Kräfte aus Norddeutschland werden Sammelräume zum Abruf in der Nähe der Autobahn benötigt.

**Nachforderung** (6)

- [2026-04-17 07:46 Uhr] **#13** von „Hackathon: S2 / S5" → „Leitstelle" [Normal/Unopen]
  > Weitere Kräfte benötigt: Alarmieren Sie 4 Feuerwehrbereitschaften zur Anfahrt der Bereitstellungsraumes BR1 zur sofortigen Verfügung. Einsatzdauer mind. 24h.
- [2026-04-17 07:48 Uhr] **#16** von „Hackathon: S4" → „Leitstelle" [Normal/Unopen]
  > Anforderung 2 Gruppen Betreuung 2 Fachgruppe N zum BR1 zum Betrieb des BR und Verpflegung der Kräfte - Einsatzdauer vermutlich 48 Stunden.
- [2026-04-17 08:04 Uhr] **#31** von „AL1: FüAss AL" → „Bereitstellungsraum 1" [Normal/Unopen]
  > Anforderung weiterer Kräfte:  5 Tanklöschfahrzeuge für EInsatzabschnitt1 benötigt.
- [2026-04-17 08:07 Uhr] **#32** von „BR : AL" → „Einsatzleitung" [Normal/Forwarded]
  > Anforderungen für BR 1:  - Mobile Tankstelle Diesel 2000l und regelmäßige Befüllung - AdBlue  - Personal zum Betrieb des BR 1 Zug Verpflegung, 2 Fachgruppen N THW
- [2026-04-17 08:18 Uhr] **#32.3** von „BR : AL" → „2026-3 - Hackathon: S1" [Normal/Completed]
  > Anforderungen für BR 1:  - Mobile Tankstelle Diesel 2000l und regelmäßige Befüllung - AdBlue  - Personal zum Betrieb des BR 1 Zug Verpflegung, 2 Fachgruppen N THW
- [2026-04-17 10:10 Uhr] **#49** von „UEA 3.1 Bavaria Studios" → „Einsatzleitung" [Normal/Unopen]
  > Dringend Kräfte zum Schutz der Bavaria Studios benötigt.  Aktuell Werkfeuerwehr mit 1 LZ im Einsatz.   Nachforderung:  2 LZ  Material zur Vegetationsbrandbekämpfung für mind. 2 Gruppen.   Wassertransportzüge und Flatbhälter zur Wasserreserver benötigt.

**Eilmeldung** (5)

- [2026-04-17 07:55 Uhr] **#21** von „Hackathon: S2 / S5" → „An alle: AL1" [High/Completed]
  > Wetterinformationen 17.04.2026 9:50:  Temperatur 13°C  Niederschlag: 0% Luftfeuchte: 63% Wind: 5 km/h  Aussicht:  Wind wird in den nächsten Stunden auffrischen. Wind von Ost nach West.   Lageentwicklung ist abzuwarten und zu bewerten.
- [2026-04-17 07:55 Uhr] **#22** von „Hackathon: S2 / S5" → „An alle: BR " [High/Completed]
  > Wetterinformationen 17.04.2026 9:50:  Temperatur 13°C  Niederschlag: 0% Luftfeuchte: 63% Wind: 5 km/h  Aussicht:  Wind wird in den nächsten Stunden auffrischen. Wind von Ost nach West.   Lageentwicklung ist abzuwarten und zu bewerten.
- [2026-04-17 07:55 Uhr] **#23** von „Hackathon: S2 / S5" → „An alle: Hackathon" [High/Completed]
  > Wetterinformationen 17.04.2026 9:50:  Temperatur 13°C  Niederschlag: 0% Luftfeuchte: 63% Wind: 5 km/h  Aussicht:  Wind wird in den nächsten Stunden auffrischen. Wind von Ost nach West.   Lageentwicklung ist abzuwarten und zu bewerten.
- [2026-04-17 08:01 Uhr] **#26** von „AL1: FüAss AL" → „Hackathon" [High/Forwarded]
  > Kräfte aktuell vom Feuer an angehäängter Position eingeschlossen.
- [2026-04-17 08:17 Uhr] **#26.3** von „AL1: FüAss AL" → „2026-3 - Hackathon: S3 / S6" [High/Unopen]
  > Kräfte aktuell vom Feuer an angehäängter Position eingeschlossen.

**Sonstiges** (3)

- [2026-04-17 08:01 Uhr] **#27** von „AL1: FüAss AL" → „Hackathon" [Low/Forwarded]
  > Wasserentnahmestelle am Hydrantennetz nicht nutzbar. Defekt.
- [2026-04-17 08:18 Uhr] **#27.3** von „AL1: FüAss AL" → „2026-3 - Hackathon: S2 / S5" [Low/Completed]
  > Wasserentnahmestelle am Hydrantennetz nicht nutzbar. Defekt.
- [2026-04-17 10:13 Uhr] **#52** von „Hackathon: S1" → „Bereitstellungsraum 1" [Low/Unopen]
  > Kräfte aus Schleswig-Holstein treffen am Vormittag des 18. April ein.  Detaillierte Informationen an den Informationen der Ressourcen hinterlegt.

**Lagebericht** (3)

- [2026-04-17 08:27 Uhr] **#40** von „Hackathon: S2 / S5" → „Leitstelle" [Low/Unopen]
  > Aktueller Lagebericht 10:25 17.04.2026:   Allgemeine Lage:  Freitagvormitag - meldung über einen Waldbrand im südlichen München, angrenzend Landkreis München.  Waldbrand ausgedehnt pber mehrere ha. Vollfeuer im Wald.   Wetter: Aktuell ca. 13 Grad, ohne Regen, geringe Luftfeuchtigkeit. Aktuell windstill, soll im Verlauf des tages aufdrehen und von Ost nach West verlaufen.  Organisation:  Aktuell 4 Einsatzabschnitte gebildet.  - Nord - Süd - Ost - Logistik  Dazu ein zentraler Bereitstellugsraum.  Einsatzabschnitte arbeiten eigenständig.  Anforerungen über die Einstzleitung/Stab Hackathon.   Kräfte:  Kräfteübersicht aktuell nicht vollständig.  Muss aktalisiert werden.  Anforderungen werden zentral über BR1 und S1 koordiniert.   Externe Kräfte zur Unterstützung angefordert.  Nächste Lagebesprechung: 12 Uhr.
- [2026-04-17 10:08 Uhr] **#48** von „Hackathon: S1" → „Hackathon: S2 / S5" [Low/Unopen]
  > Aktuelle Kräfteübersicht
- [2026-04-17 10:16 Uhr] **#53** von „Hackathon: S2 / S5" → „Leitstelle" [Low/Unopen]
  > Lagebericht 12:15 17.04.2026:   Lageveränderung:  Feuer breitet sich weiter in Richtung Nor-Ost aus.  Feuer weiterhin in keinem  Abschnitt unter Kontrolle. im UEA 3.1 ist das Gebiet der Bavara Studios akut bedroht.   Kräfte:  Vielzahl an Kräften aktuell auf der Anfahrt. Eintreffzeiten verteilt über die Zeit.  Nachforderung:  Hubschrauber mit Außenlastbehälter zur Einsatzstelle. Dafür mit Leitstelle geeignete Landeplätze bestimmen.

**Gesprächsnotiz** (2)

- [2026-04-17 07:47 Uhr] **#15** von „Hackathon: S3 / S6" → „Hackathon: S4" [Low/Completed]
  > Aktuell über 200 Kräfte im Einsatz - Verpflegung wird alle 4 Stunden für alle Kräfte benötigt. Verpflegung muss auf Abschnitte verteilt werden. Zentraler Verpflegungspunkt am BR1 in aufzubauen.
- [2026-04-17 08:16 Uhr] **#34** von „BR : AL" → „null" [Low/Completed]
  > Meldkopf BR ist einzurichen. Es ist ein System einzuführen Kräfte am Meldekopf zu getrieren und dem BR zuzuweisen. Verantwortlich: Meldekopf.

---

## Gesamtübersicht aller Einsatzmittel im System

### Army (1 Einheiten, davon 0 aktiv im FMS)

| Name | Typ | Rufzeichen | FMS-Status |
|------|-----|------------|-----------|
| BWH + Bambi | BWH+Bambi | BWH + Bambi | Status0 |

### EMS (37 Einheiten, davon 0 aktiv im FMS)

| Name | Typ | Rufzeichen | FMS-Status |
|------|-----|------------|-----------|
| 90-PTZ10-1 | PTZ-10 | 90-PTZ10-1 | Status0 |
| 91-PTZ10-1 | PTZ-10 | 91-PTZ10-1 | Status0 |
| 92-BHP15-1 | BHP 15 | 92-BHP15-1 | Status0 |
| 93-BtPl50-1 | BePl 50 | 93-BtPl50-1 | Status0 |
| 94-BtPl500-1 | BePl 500 | 94-BtPl500-1 | Status0 |
| 1-RTW-1 | RTW | 1-RTW-1 | Status0 |
| 1-RTW-2 | RTW | 1-RTW-2 | Status0 |
| 2-RTW-1 | RTW | 2-RTW-1 | Status0 |
| 3-RTW-1 | RTW | 3-RTW-1 | Status0 |
| 4-RTW-1 | RTW | 4-RTW-1 | Status0 |
| 5-RTW-1 | RTW | 5-RTW-1 | Status0 |
| 5-RTW-2 | RTW | 5-RTW-2 | Status0 |
| 6-RTW-1 | RTW | 6-RTW-1 | Status0 |
| 7-RTW-1 | RTW | 7-RTW-1 | Status0 |
| 8-RTW-1 | RTW | 8-RTW-1 | Status0 |
| 9-RTW-1 | RTW | 9-RTW-1 | Status0 |
| 13-KTW-1 | KTW | 13-KTW-1 | Status0 |
| 13-KTW-2 | KTW | 13-KTW-2 | Status0 |
| 13-KTW-3 | KTW | 13-KTW-3 | Status0 |
| 14-KTW-1 | KTW | 14-KTW-1 | Status0 |
| 14-KTW-2 | KTW | 14-KTW-2 | Status0 |
| 1-NEF-1 | NEF | 1-NEF-1 | Status0 |
| 3-NEF-1 | NEF | 3-NEF-1 | Status0 |
| 6-NEF-1 | NEF | 6-NEF-1 | Status0 |
| 7-NEF-1 | NEF | 7-NEF-1 | Status0 |
| EC NEF 1  | NEF | Ret EC 1-82-1 | Status0 |
| EC RTW 1  | RTW | Ret EC 1-83-1 | Status0 |
| EC RTW 2 | RTW | Ret EC 1-83-2 | Status0 |
| EC GW-San 1  | GW-San | Ret EC 1-98-1 | Status0 |
| EC NEF 2 | NEF | Ret EC 2-82-1 | Status0 |
_... und 7 weitere_

### Fire (98 Einheiten, davon 0 aktiv im FMS)

| Name | Typ | Rufzeichen | FMS-Status |
|------|-----|------------|-----------|
| 1-LZ-1 | LZ - FW | 1-LZ-1 | Status0 |
| 1-LZ-2 | LZ - FW | 1-LZ-2 | Status0 |
| 2-LZ-1 | LZ - FW | 2-LZ-1 | Status0 |
| 3-LZ-3 | LZ - FW | 3-LZ-3 | Status0 |
| 4-LZ-1 | LZ - FW | 4-LZ-1 | Status0 |
| 4-LZ-2 | LZ - FW | 4-LZ-2 | Status0 |
| 5-LZ-1 | LZ - FW | 5-LZ-1 | Status0 |
| 6-LZ-1 | LZ - FW | 6-LZ-1 | Status0 |
| 6-LZ-2 | LZ - FW | 6-LZ-2 | Status0 |
| 6-LZ-3 | LZ - FW | 6-LZ-3 | Status0 |
| 9-LZ-2 | LZ - FW | 9-LZ-2 | Status0 |
| 11-LZ-1 | LZ - FW | 11-LZ-1 | Status0 |
| 13-LZ-2 | LZ - FW | 13-LZ-2 | Status0 |
| 16-LZ-1 | LZ - FW | 16-LZ-1 | Status0 |
| 7-RZ-1 | RZ - FW | 7-RZ-1 | Status0 |
| 8-RZ-1 | RZ - FW | 8-RZ-1 | Status0 |
| 12-UMZ-1 | UMZ - FW | 12-UMZ-1 | Status0 |
| 1-ELW2-1 | ELW 2 | 1-ELW2-1 | Status0 |
| 2-ELW2-1 | ELW 2 | 2-ELW2-1 | Status0 |
| 3-ELW2-1 | ELW 2 | 3-ELW2-1 | Status0 |
| 4-ELW2-1 | ELW 2 | 4-ELW2-1 | Status0 |
| 5-WLF-1 | WLF + AB | 5-WLF-1 | Status0 |
| 5-WLF-2 | WLF + AB | 5-WLF-2 | Status0 |
| 10-WLF-1 | WLF + AB | 10-WLF-1 | Status0 |
| 10-WLF-2 | WLF + AB | 10-WLF-2 | Status0 |
| 10-AB-A-1 | WLF + AB | 10-AB-A-1 | Status0 |
| 10-AB-MANV-1 | WLF + AB | 10-AB-MANV-1 | Status0 |
| 10-AB-V-1 | WLF + AB | 10-AB-V-1 | Status0 |
| 10-AB-Log-1 | WLF + AB | 10-AB-Log-1 | Status0 |
| 10-AB-Schaum-1 | WLF + AB | 10-AB-Schaum-1 | Status0 |
_... und 68 weitere_

### Police (3 Einheiten, davon 0 aktiv im FMS)

| Name | Typ | Rufzeichen | FMS-Status |
|------|-----|------------|-----------|
| BPolH + Bambi | BPolH+Bambi | BPolH + Bambi | Status0 |
| Streife 1  | Streife | Peter EC 1  | Status0 |
| Streife 2  | Streife | Peter EC 2 | Status0 |

### Usar (19 Einheiten, davon 0 aktiv im FMS)

| Name | Typ | Rufzeichen | FMS-Status |
|------|-----|------------|-----------|
| 36-FGrB-1 | FGr B | 36-FGrB-1 | Status0 |
| 37-FGrBrB1-1 | FGr BrB | 37-FGrBrB1-1 | Status0 |
| 38-FGrE-1 | FGr E | 38-FGrE-1 | Status0 |
| 39-FGrI-1 | FGr I | 39-FGrI-1 | Status0 |
| 40-FGrN-1 | FGr N | 40-FGrN-1 | Status0 |
| 41-FGrO-B-1 | FGr O-B | 41-FGrO-B-1 | Status0 |
| 42-FGrO-C-1 | FGr O-C | 42-FGrO-C-1 | Status0 |
| 43-FGrSB-B-1 | FGr SB-B | 43-FGrSB-B-1 | Status0 |
| 44-FGrTW-1 | FGr TW | 44-FGrTW-1 | Status0 |
| 45-FGrWP-B-1 | FGr-WP-B | 45-FGrWP-B-1 | Status0 |
| 46-FGrWP-C-1 | FGr-W-C | 46-FGrWP-C-1 | Status0 |
| 47-FGrLogV-1 | FGr-Log-V | 47-FGrLogV-1 | Status0 |
| 48-FGrLogTS-1 | FGr-Log-TS | 48-FGrLogTS-1 | Status0 |
| 49-FGrR-A-1 | FGr-R-A | 49-FGrR-A-1 | Status0 |
| 50-FGrR-B-1 | FGr-R-B | 50-FGrR-B-1 | Status0 |
| 51-FGrR-C-1 | FGr-R-C | 51-FGrR-C-1 | Status0 |
| SysBR500 | SysBR500 | SysBR500 | Status0 |
| EC GKW 1  | GKW | Heros EC 22-51 | Status0 |
| EC GKW 2 | GKW | Heros EC 23-51 | Status0 |

---

## Referenzdaten: Fahrzeug-/Einheitstypen

| Typ | Service | Beschreibung |
|-----|---------|-------------|
| ELW 2 | Fire | Einsatzleitwagen 2 |
| FGr O-C | Usar | Fachgruppe Ortung C |
| FGr-W-C | Usar | Fachgruppe Wasserschaden/Pumpen Typ C |
| FGr-R-C | Usar | Fachgruppe Räumen Typ C |
| FGr-R-B | Usar | Fachgruppe Räumen B |
| LF | Fire | Löschgruppenfahrzeug |
| V1 | Fire | Verband 1 |
| ELW 1 | Fire | Einsatzleitwagen 1 |
| TEL | Fire | Technische Einsatzleitung |
| DL | Fire | Drehleiter |
| FwBer | Fire | Feuerwehrbereitschaft |
| TLF | Fire | Tanklöschfahrzeug |
| LZ - FW | Fire | Löschzug Feuerwehr |
| RZ - FW | Fire | Rüstzug Feuerwehr |
| UMZ - FW | Fire | Umweltschutzzug Feuerwehr |
| WLF + AB | Fire | Wechselladerfahrzeug mit Abrollbehälter |
| GW-L  | Fire | Gerätewagen Logistik |
| SW2000 | Fire | Schlauchwagen 2000 |
| MTF | Fire | Mannschaftstransportfahrzeug |
| RTH | Fire | Rettungshubschrauber |
| ITH | Fire | Intensivtransporthubschrauber |
| BPolH+Bambi | Police | Bundespolizei-Hubschrauber + Bambi Bucket |
| BWH+Bambi | Army | Bundeswehr Hubschrauber + Bambi Bucket |
| RTW | EMS | Rettungswagen |
| KTW | EMS | Krankentransportwagen |
| NEF | EMS | Notarzteinsatzfahrzeug |
| FGr B | Usar | Fachgruppe Bergung |
| FGr BrB | Usar | Fachgruppe Brückenbau |
| FGr E | Usar | Fachgruppe Elektroversorgung |
| FGr I | Usar | Fachgruppe Infrastruktur |
| FGr N | Usar | Fachgruppe Notversorgung |
| FGr TW | Usar | Fachgruppe Trinkwasserversorgung |
| FGr O-B | Usar | Fachgruppe Ortung B |
| FGr-WP-B | Usar | Fachgruppe Wasserschaden/Pumpen Typ B |
| FGr-Log-V | Usar | Fachgruppe Logistik-Versorgung |
| FGr-Log-TS | Usar | Fachgruppe Logistik Transport Schwer |
| FGr SB-B | Usar | Fachgruppe Schwere Bergung Typ B |
| FGr-R-A | Usar | Fachgruppe Räumen Typ A |
| SysBR500 | Usar | System Bereitstellungsraum 500 |
| FD-BS | Fire | Fachdienst Brandschutz |
| FD-ABC | Fire | Fachdienst ABC |
| FD-Log | Fire | Fachdienst Logistik |
| FD-Betr | Fire | Fachdienst Betreuung |
| FD-San | EMS | Fachdienst Sanitätsdienst |
| FD-W | Fire | Fachdienst Wasserrettung |
| PTZ-10 | EMS | Patiententransportzug 10 |
| BHP 15 | EMS | Behandlungsplatz 15 |
| BePl 50 | EMS | Betreuungsplatz 50 |
| BePl 500 | EMS | Betreuungsplatz 500 |
| LZ | Fire | Löschzug |
| Police unit UAE | Police | – |
| HLF 20 | Fire | Hilfeleistungslöschgruppenfahrzeug |
| Streife | Police | Streifenwagen |
| GKW | Usar | Gerätekraftwagen |
| GW-San | EMS | Gerätewagen Sanität |
| UAV | Fire | Drohne |
| GW-W | Fire | Gerätewagen Wasser |
| RW 2 | Fire | Rüstwagen 2 |
| GW-L2 | Fire | Gerätewagen-Logistik |
| DLK | Fire | Drehleiter |
| DLAK | Fire | Drehleiter |
| LF 20/16 | Fire | Löschgruppenfahrzeug |
| LF 16/12 | Fire | Löschgruppenfahrzeug |
| MTW | Fire | Mannschaftstransportwagen |
| PKW | Fire | Personenkraftwagen |
| RTB2 | Fire | Rettungsboot 2 |
| ELW | Fire | FF Halstenbek ELW1 |
| FFG ELW | Fire | FF Geesthacht ELW |
| DLAK 23/12 | Fire | Drehleiter 23/12 DLAK |
| LF 20 | Fire | Löschgruppenfahrzeug 20 |
