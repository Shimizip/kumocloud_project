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

#### In den Root-Ordner navigieren
   Navigiere mit einer Kommandozeile (CMD/Bash) in den Root-Ordner des Projekts kumocloud_projekt.

2. **Docker-Befehle ausführen**

    Für Linux:
        ```bash
        sudo docker build -t        kumocloud_app .
        sudo docker run -p 8000:8000 kumocloud_app

    Für Windows:
        ```bash
        docker build -t kumocloud_app .
        docker run -p 8000:8000 kumocloud_app

3. **Backend prüfen**
    Nach dem Start ist das Backend unter http://127.0.0.1:8000 erreichbar.
    Die Swagger UI kann unter http://127.0.0.1:8000/docs aufgerufen werden.

## API Endpunkte

### 1. CSV hochladen
- **Methode:** `POST`
- **Pfad:** `/upload/upload-csv`
- **Beschreibung:** 
  - Lädt eine CSV-Datei mit Kundennachrichten und Sendezeitpunkten hoch.


### 2. CSV-Überprüfung
- **Methode:** `GET`
- **Pfad:** `/check-upload/check-uploaded-data`
- **Beschreibung:** 
  - Überprüft, ob eine CSV-Datei erfolgreich hochgeladen wurde. 
  - **Wichtig:** Geben Sie den **vollständigen Dateinamen** der hochgeladenen Datei an, um zu überprüfen, ob sie korrekt verarbeitet wurde.
  - Dieser Endpoint stellt sicher, dass die angegebene Datei erfolgreich hochgeladen wurde und erlaubt es, eine Vorschau der Daten zu erhalten, um ihre Richtigkeit zu bestätigen.


### 3. Intent-Erkennung starten
- **Methode:** `POST`
- **Pfad:** `/intent-detection/start-intent-detection`
- **Beschreibung:** 
  - Startet einen Intent-Erkennungs-Job für die hochgeladene CSV-Datei. 
  - **Wichtig:** Geben Sie den **vollständigen Dateinamen** der hochgeladenen Datei an, bei der die Intent-Erkennung durchgeführt werden soll.
  - Optional kann ein **Limit** für die maximale Anzahl der zu erkennenden Intentionen angegeben werden. Der Standardwert ist 5.
  - Die Anzahl der Intentionen muss zwischen 1 und 10 liegen.

### 4. Job abbrechen
- **Methode:** `POST`
- **Pfad:** `/cancel-job/cancel-job`
- **Beschreibung:** 
  - Dieser Endpoint dient dazu, einen laufenden Intent-Erkennungs-Job abzubrechen. Der Job wird nur abgebrochen, wenn er sich im Status **"in progress"** befindet. Falls kein Job gestartet wurde, gibt der Endpoint eine Nachricht zurück, dass kein Job zum Abbrechen existiert.
  - Es wird überprüft, ob ein Job derzeit läuft, und je nach Status wird der Job entweder abgebrochen oder eine entsprechende Nachricht zurückgegeben.


### 5. Jobstatus anzeigen
- **Methode:** `GET`
- **Pfad:** `/job-status/job-status`
- **Beschreibung:** 
  - Zeigt den aktuellen Status eines laufenden Intent-Erkennungs-Jobs an.
  - **Es läuft immer nur ein Job** gleichzeitig. Wenn ein Job abgeschlossen oder abgebrochen wurde, kann ein neuer gestartet werden.
  - Der Jobstatus umfasst Informationen wie den aktuellen **Fortschritt**, ob der Job abgebrochen wurde, die **Job-ID** und den **Dateinamen** der CSV-Datei, die verarbeitet wird.

- **Beispielantwort:**
  ```json
  {
    "status": "in progress",
    "progress": "34%",
    "is_canceled": false,
    "job_id": "98594907-3698-4d0a-9557-49c48414bf5b",
    "csv_name": "test_long.csv"
  }

### 6. Jobs-IDs nach CSV-Datei abrufen
- **Methode:** `GET`
- **Pfad:** `/filter-id/jobs-by-csv`
- **Beschreibung:** 
  - Gibt alle Job-IDs zurück, die zu einer bestimmten CSV-Datei gehören. Der Dateiname muss als Query-Parameter angegeben werden.
- **Query-Parameter:**
  - `file_name` (str): Der Name der CSV-Datei, für die die Job-IDs abgerufen werden sollen.

### 7. Ergebnisse filtern
- **Methode:** `GET`
- **Pfad:** `/filter/filter-results`
- **Beschreibung:** 
  - Filtert die Ergebnisse eines Intent-Erkennungs-Jobs basierend auf verschiedenen Kriterien wie Zeiträumen, Dateinamen, Job-IDs und Sortierreihenfolgen.
  - **Beispielantwort**: Die Antwort enthält eine Liste der gefilterten Fragen und deren zugehörigen Intentionen. Optional kann die Anzahl der zurückgegebenen Fragen auf eine bestimmte Anzahl begrenzt werden.
  
- **Query-Parameter:**
  - `start_date` (datetime, optional): Startdatum und Uhrzeit im Format `YYYY-MM-DD HH:MM`, ab dem gefiltert werden soll. Beispiel: `2023-10-05 09:00`.
  - `end_date` (datetime, optional): Enddatum und Uhrzeit im Format `YYYY-MM-DD HH:MM`, bis zu dem gefiltert werden soll. Beispiel: `2023-10-05 18:00`.
  - `file_name` (str, optional): Name der CSV-Datei, für die die Ergebnisse gefiltert werden sollen.
  - `job_id` (str, optional): Job-ID, deren Ergebnisse zurückgegeben werden sollen.
  - `order` (str, optional): Sortierreihenfolge der Intentionen. Akzeptiert:
    - `desc`: Häufigste Intentionen zuerst.
    - `asc`: Am wenigsten häufige Intentionen zuerst.

- **Beispielantwort:**
  ```json
  {
    "filtered_results": {
      "filtered_questions": [
        {
          "question": "Hi! Könnt ihr bitte mal die Rechnung checken? Kommt mir bisschen hoch vor…",
          "created_at": "2023-10-05T15:45:00"
        },
        {
          "question": "Könnt ihr endlich meinen Vertrag kündigen? Hab’s jetzt schon dreimal geschrieben!",
          "created_at": "2023-10-01T09:12:00"
        }
      ],
      "intent_results": {
        "Umzug Melden": 13,
        "Zahlungsart Ändern": 10,
        "Zählerstand Übermitteln": 9,
        "Vertrag Kündigen": 8,
        "Fallback": 6,
        "Abschlagszahlung Anpassen": 3
      },
      "limit_der_intents": 5
    }
  }
