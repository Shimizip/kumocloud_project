# app/services/job_service.py
from sqlalchemy.orm import Session
from app.database.database_config import Job  # Importiere das Job-Modell
from typing import List

class JobService:
    @staticmethod
    def get_job_ids_by_csv(db: Session, file_name: str) -> List[str]:
        """
        Holt alle Job-IDs, die zu einer bestimmten CSV-Datei gehören.

        Args:
            db (Session): Datenbank-Session.
            file_name (str): Name der CSV-Datei, für die die Job-IDs abgerufen werden sollen.

        Returns:
            list: Liste der Job-IDs, die mit der angegebenen CSV-Datei verknüpft sind.
        """
        # Abfrage der Job-IDs, die mit der CSV-Datei verknüpft sind
        jobs = db.query(Job.id).filter(Job.csv_name == file_name).all()
        return [job.id for job in jobs]  # Extrahiere nur die Job-IDs aus dem Ergebnis
