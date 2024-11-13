# app/services/job_filter_service.py
from sqlalchemy.orm import Session
from app.database.database_service import get_job_by_id
from app.database.database_config import Job
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from app.services.csv_upload_service import all_uploaded_csvs
import pandas as pd

# Enum zur Definition der Sortierreihenfolge
class Order(str, Enum):
    asc = "asc"
    desc = "desc"

class JobFilter:
    @staticmethod 
    async def filter_jobs(
        db: Session, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None, 
        file_name: Optional[str] = None,
        job_id: Optional[str] = None, 
        order: str = "desc"
    ) -> Dict[str, Any]:  # Angepasst auf Dict-Rückgabewert
        # Filtere die CSV-Daten basierend auf dem Start- und Enddatum
        filtered_questions = await JobFilter._filter_csv_data(start_date, end_date, file_name)
        
        # Hole den Job aus der Datenbank
        job_from_db = get_job_by_id(db, job_id)
        if job_from_db is None:
            raise ValueError("Job nicht gefunden oder keine Ergebnisse verfügbar.")

        # Sortiere die Intent-Ergebnisse basierend auf `job_id` und `order`
        order_enum = Order.desc if order == "desc" else Order.asc  # Konvertiere `order` in `Order` Enum
        sorted_intent_results = await JobFilter._filter_intent_results(job_from_db, order_enum)

        # Hole das Limit (falls im Job definiert)
        limit = getattr(job_from_db, "limit", None)  # Verwende getattr, falls limit nicht existiert
        
        # Rückgabe der gefilterten Fragen und Intent-Ergebnisse
        return {
            "filtered_questions": filtered_questions.to_dict(orient="records"),
            "intent_results": sorted_intent_results,
            "limit_der_intents": limit  # Behebt den Syntaxfehler
        }
        
    @staticmethod
    async def _filter_csv_data(start_date: Optional[datetime], end_date: Optional[datetime], file_name: str) -> pd.DataFrame:
        file_data = next((item["data"] for item in all_uploaded_csvs if item["file_name"] == file_name), None)
        print(f"Filename: {file_name}")
        
        if file_data is None:
            raise ValueError("Keine hochgeladene CSV-Datei gefunden.")
        
        # Überprüfe, ob die DataFrame die notwendigen Spalten hat
        required_columns = {"question", "created_at"}
        if not required_columns.issubset(file_data.columns):
            raise ValueError("Die hochgeladene CSV-Datei hat nicht die erforderlichen Spalten.")
        
        # Konvertiere die `created_at`-Spalte in datetime-Format, falls noch nicht geschehen
        file_data["created_at"] = pd.to_datetime(file_data["created_at"])

        # Filtern der Zeilen basierend auf dem Start- und Enddatum
        if start_date and end_date:
            filtered_data = file_data[(file_data["created_at"] >= start_date) & (file_data["created_at"] <= end_date)]
        elif start_date:
            filtered_data = file_data[file_data["created_at"] >= start_date]
        elif end_date:
            filtered_data = file_data[file_data["created_at"] <= end_date]
        else:
            # Wenn kein Start- und Enddatum angegeben ist, gib die gesamte DataFrame zurück
            filtered_data = file_data

        # Gib die gefilterten Fragen und das Erstellungsdatum zurück
        return filtered_data[["question", "created_at"]]
    
    @staticmethod
    async def _filter_intent_results(job_from_db: Job, order: Order) -> Optional[Dict[str, int]]:
        """
        Holt und sortiert die Intent-Ergebnisse eines Jobs basierend auf der Job-Instanz und der angegebenen Sortierreihenfolge.
        
        Args:
            job_from_db (Job): Die Job-Instanz mit den Intent-Ergebnissen.
            order (Order): Sortierreihenfolge der Ergebnisse - "desc" für absteigend, "asc" für aufsteigend.
        
        Returns:
            Optional[Dict[str, int]]: Sortierte Intent-Ergebnisse als Dictionary.
        """
        # Ergebnis der Intent-Erkennung
        intent_results = job_from_db.result

        # Sortiere das Ergebnis basierend auf `order`
        sorted_intents = sorted(intent_results.items(), key=lambda x: x[1], reverse=(order == Order.desc))

        # Konvertiere die sortierte Liste zurück in ein Dictionary
        sorted_intent_results = dict(sorted_intents)
        
        return sorted_intent_results
