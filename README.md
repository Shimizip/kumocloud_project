# Intentionserkennung von Kundennachrichten

Dieses Projekt implementiert ein Backend zur Analyse und Intentionserkennung von Kundennachrichten. Mit FastAPI und Python werden RESTful-Services bereitgestellt, um Nachrichten nach gemeinsamen Intentionen zu analysieren und die Ergebnisse flexibel zu filtern.

---

## Features

### Hauptendpunkte
1. **CSV hochladen**  
   Lädt Datensätze (Kundennachrichten und Sendezeitpunkt) im CSV-Format hoch.
   
2. **Intent-Erkennung starten**  
   Führt die Intentionserkennung auf den hochgeladenen Daten durch. Der Benutzer kann die maximale Anzahl von Intentionen festlegen. Nachrichten ohne erkennbare Intentionen werden einer Fallback-Intention zugeordnet.
   
3. **Jobstatus anzeigen**  
   Zeigt den Status eines laufenden oder abgeschlossenen Intent-Erkennungs-Jobs an. Enthält Informationen wie Fortschritt (Prozent), Status (`completed`, `canceled`, `failed`) und das definierte Intent-Limit.

4. **Job abbrechen**  
   Bricht einen laufenden Intent-Erkennungs-Job ab.

5. **Filterung der Ergebnisse**  
   Filtert die Ergebnisse eines abgeschlossenen Jobs anhand folgender Kriterien:
   - **Sendezeitpunkt:** Filterung der Nachrichten nach Datum/Zeit.
   - **Anzahl der Intentionen:** Begrenzung der zurückgegebenen Intentionen.
   - **Sortierung:** Ergebnisse sortiert nach häufigsten oder seltensten Intentionen.

### Zusätzliche Endpunkte
1. **CSV-Überprüfung**  
   Überprüft, ob eine CSV-Datei erfolgreich hochgeladen wurde, basierend auf ihrem Namen.

2. **Job-IDs abrufen**  
   Gibt alle zu einer bestimmten CSV-Datei gehörigen Job-IDs zurück. Diese IDs können zur weiteren Verarbeitung (z. B. Statusabfrage) verwendet werden.

---

## Setup-Anleitung

### Voraussetzungen
1. **Docker installieren:**  
   Lade die neueste Version von Docker herunter und installiere sie.  
   Überprüfe die Installation mit:  
   ```bash
   docker --version
   
