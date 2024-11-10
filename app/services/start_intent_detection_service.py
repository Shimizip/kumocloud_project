import asyncio
from transformers import pipeline
from fastapi import BackgroundTasks, HTTPException
import pandas as pd
from app.services.csv_upload_service import uploaded_csv_data
from app.services.job_status_service import job_status
import time

# Pipeline für Zero-Shot Klassifikation
intent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

class IntentService:

    @staticmethod
    async def detect_intents(background_tasks: BackgroundTasks, max_intentions: int = 5):
        if "data" not in uploaded_csv_data:
            raise HTTPException(status_code=400, detail="Keine hochgeladene CSV-Datei gefunden.")
        
        # Starte den Job im Hintergrund
        background_tasks.add_task(IntentService._run_intent_detection, max_intentions)
        return {"message": "Intent-Erkennung im Hintergrund gestartet."}

    @staticmethod
    async def _run_intent_detection(max_intentions: int):
        start_time = time.time()

        df = uploaded_csv_data["data"]
        
        # Setze den Job-Status auf 'in progress'
        job_status["status"] = "in progress"
        job_status["progress"] = 0
        job_status["is_canceled"] = False

        # Führe die Intentionserkennung auf dem gesamten DataFrame aus
        try:
            intent_counts = await IntentService._perform_intent_detection(df, max_intentions)

            # Sortiere die Ergebnisse nach Häufigkeit und füge ggf. Fallback hinzu
            sorted_intents = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)
            if len(sorted_intents) > max_intentions:
                selected_intents = sorted_intents[:max_intentions]
                fallback_intent_count = sum(count for _, count in sorted_intents[max_intentions:])
                selected_intents.append(("Fallback", fallback_intent_count))
            else:
                selected_intents = sorted_intents

            # Endzeit erfassen und Dauer berechnen
            end_time = time.time()
            duration = end_time - start_time
            print(f"Gesamte Verarbeitungszeit: {duration:.2f} Sekunden")

            # Setze den Job-Status auf 'completed' und den Fortschritt auf 100
            if job_status["progress"] == 100 :
                job_status["status"] = "completed"
            return dict(selected_intents)
        
        except Exception as e:
            # Bei Fehlern setze den Status auf 'failed'
            job_status["status"] = "failed"
            job_status["progress"] = 0
            print(f"Fehler während der Verarbeitung: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def _perform_intent_detection(df: pd.DataFrame, max_intentions: int):
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
            if job_status["is_canceled"]:  # Job-Abbruch nach jedem Schritt
                job_status["status"] = "canceled"
                return intents  
            
            # Klassifiziere die Nachricht basierend auf den spezifischen Intentionen
            result = intent_classifier(message, candidate_labels=intent_labels)

            # Fortschritt aktualisieren
            job_status["progress"] = int(((idx + 1) / total_messages) * 100)

            # Wähle die Intention mit der höchsten Wahrscheinlichkeit
            intent = result["labels"][0]

            # Erhöhe die Häufigkeit für die erkannte Intention
            intents[intent] = intents.get(intent, 0) + 1

            # Asynchroner Sleep, um den Thread nicht zu blockieren
            await asyncio.sleep(0)  # Gib anderen Tasks die Möglichkeit, ausgeführt zu werden

        return intents
