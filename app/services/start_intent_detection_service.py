from transformers import pipeline
from app.services.csv_upload_service import uploaded_csv_data
import pandas as pd

class IntentService:
    # Lade das Modell einmalig in einer Pipeline für Textklassifikation
    intent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    @staticmethod
    def detect_intents(max_intentions: int = 5):
        if "data" not in uploaded_csv_data:
            raise ValueError("Keine hochgeladene CSV-Datei gefunden. Bitte zuerst eine Datei hochladen.")
        
        df = uploaded_csv_data["data"]
        intent_counts = IntentService._perform_intent_detection(df)
        
        sorted_intents = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_intents) > max_intentions:
            selected_intents = sorted_intents[:max_intentions]
            fallback_intent_count = sum([count for _, count in sorted_intents[max_intentions:]])
            selected_intents.append(("Fallback", fallback_intent_count))
        else:
            selected_intents = sorted_intents
        
        return dict(selected_intents)

    @staticmethod
    def _perform_intent_detection(df: pd.DataFrame):
        intents = {}
        
        # Spezifische Intentionen (Labels), die für einen Stadtwerke-Kundendienst relevant sind
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

        for message in df['question']:
            # Klassifiziere die Nachricht basierend auf den spezifischen Intentionen
            result = IntentService.intent_classifier(message, candidate_labels=intent_labels)
            
            # Wähle die Intention mit der höchsten Wahrscheinlichkeit
            intent = result["labels"][0]
            
            # Erhöhe die Häufigkeit für die erkannte Intention
            intents[intent] = intents.get(intent, 0) + 1
        
        return intents
