# app/services/job_service.py
from sqlalchemy.orm import Session
from app.database.database_config import Job  # Importiere das Job-Modell
from typing import List

class JobService:
    @staticmethod
    def get_job_ids_by_csv(db: Session, file_name: str) -> List[str]:
        # Abfrage der Job-IDs, die mit der CSV-Datei verknüpft sind
        jobs = db.query(Job.id).filter(Job.csv_name == file_name).all()
        return [job.id for job in jobs]  # Extrahiere nur die Job-IDs aus dem Ergebnis
