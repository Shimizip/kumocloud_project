import asyncio
from uuid import uuid4  # uuid4 aus dem uuid-Modul importieren
from transformers import pipeline
from fastapi import BackgroundTasks, HTTPException
from app.database.database_service import create_job, get_job_by_id
from sqlalchemy.orm import Session
import pandas as pd
from app.services.csv_upload_service import  all_uploaded_csvs
from app.services.job_status_service import jobStatus, JobStatusService

import json


# Pipeline für Zero-Shot Klassifikation
intent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

class IntentService:

    @staticmethod
    async def detect_intents(background_tasks: BackgroundTasks, db: Session, max_intentions: int = 5, file_name: str = None):
        # Generiere eine UUID für den Job
        job_id = str(uuid4())
        # Starte den Job im Hintergrund
        background_tasks.add_task(IntentService._run_intent_detection, db, job_id, max_intentions, file_name)
        return {"message": "Intent-Erkennung im Hintergrund gestartet.", "job_id": job_id}
    
    @staticmethod
    async def _run_intent_detection(db: Session, job_id: str, max_intentions: int, file_name: str):
        print(f"Filename: {file_name}")
        #Holen der csv aus all_uploaded_csvs anhand des angegebenen Names
        uploaded_csv_data = next((item for item in all_uploaded_csvs if item["file_name"] == file_name), None) 
        #Uenberpruefung ob die uploaded_csv_data valide ist
        if uploaded_csv_data is None:
            print("Kein CSV mit dem angegebenen Dateinamen gefunden.")
            return None

        uploaded_csv_data["job_id"]=job_id

        df = uploaded_csv_data["data"]
        
        # Setze den Job-Status auf 'in progress'
        jobStatus["status"] = "in progress"
        jobStatus["progress"] = 0
        jobStatus["is_canceled"] = False
        jobStatus["job_id"] = job_id
        jobStatus["csv_name"] = file_name

        # Führe die Intentionserkennung auf dem gesamten DataFrame aus
        try:
            print("Intent Detection gestartet")
            intent_counts = await IntentService._perform_intent_detection(df)

            # Sortiere die Ergebnisse nach Häufigkeit und füge ggf. Fallback hinzu
            sorted_intents = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)
            if len(sorted_intents) > max_intentions:
                selected_intents = sorted_intents[:max_intentions]
                fallback_intent_count = sum(count for _, count in sorted_intents[max_intentions:])
                selected_intents.append(("Fallback", fallback_intent_count))
            else:
                selected_intents = sorted_intents

            print("Intents selected")
            # Verwende json.dumps() um es in ein gut formatiertes JSON zu konvertieren
            selected_intents_json = json.dumps(selected_intents, indent=4)

            # Ausgabe im Terminal
            print("Ergebnisse der Intentionserkennung:")
            print(selected_intents_json)

            # Setze den Job-Status auf 'completed' und den Fortschritt auf 100
            if jobStatus["progress"] == 100 :
                jobStatus["status"] = "completed"
                    # Speichern der CSV-Datei aus uploaded_csv_data in die Datenbank

            #Erstelle einen Eintrag des Jobs in der Datenbank
            create_job(db, 
                       job_id,
                       jobStatus["status"],
                       jobStatus["progress"], 
                       dict(selected_intents),
                       jobStatus["csv_name"],
                       max_intentions
                       )
            JobStatusService.clear_job()
            #DEBUG
            job_from_db = get_job_by_id(db, job_id)
            if job_from_db:
                print("Job-ID:", job_from_db.id)
                print("Status:", job_from_db.status)
                print("Progress:", job_from_db.progress)
                print("Ergebnis:", job_from_db.result)
            else:
                print("Job nicht gefunden.")
                return dict(selected_intents)


        
        except Exception as e:
            # Bei Fehlern setze den Status auf 'failed'
            jobStatus["status"] = "failed"
            jobStatus["progress"] = 0
            print(f"Fehler während der Verarbeitung: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def _perform_intent_detection(df: pd.DataFrame):
        intents = {}

        intent_labels = [
            "Vertrag Kündigen",
            "Rechnung Klären",
            "Abschlagszahlung Anpassen",
            "Umzug Melden",
            "Tarif Wechseln",
            "Zählerstand Übermitteln",
            "Technische Störung",
            "Zahlungsart Ändern",
            "Förderung und Rabatt Anfragen",
            "Kundensupport Allgemein"
        ]
        
        total_messages = len(df['question'])
        for idx, message in enumerate(df['question']):
            if jobStatus["is_canceled"]:  # Job-Abbruch nach jedem Schritt
                jobStatus["status"] = "canceled"
                return intents  
            
            # Klassifiziere die Nachricht basierend auf den spezifischen Intentionen
            result = intent_classifier(message, candidate_labels=intent_labels)

            # Fortschritt aktualisieren
            jobStatus["progress"] = int(((idx + 1) / total_messages) * 100)
            print(f"Nachricht {idx} versendet. Progress liegt bei: {jobStatus['progress']} %")
            # Wähle die Intention mit der höchsten Wahrscheinlichkeit
            intent = result["labels"][0]

            # Erhöhe die Häufigkeit für die erkannte Intention
            intents[intent] = intents.get(intent, 0) + 1

            # Asynchroner Sleep, um den Thread nicht zu blockieren
            await asyncio.sleep(0)  # Gib anderen Tasks die Möglichkeit, ausgeführt zu werden

        return intents
