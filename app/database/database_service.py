# Funktion zum Speichern eines Jobs
# app/services/database_service.py
from sqlalchemy.orm import Session
from app.database.database_config import Job, SessionLocal

def create_job(db: Session, job_id: str, status: str, progress: int, result: dict, csv_name: str, limit: int):
    db_job = Job(
        id=job_id,
        status=status,
        progress=progress,
        result=result,
        csv_name=csv_name,
        limit=limit
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job



# Funktion zum Abrufen eines Jobs anhand der ID
def get_job_by_id(db: Session, job_id: str):
    return db.query(Job).filter(Job.id == job_id).first()

def get_db():
    db = SessionLocal()  # Neue Session wird erstellt
    try:
        yield db
    finally:
        db.close()  # Schließe die Session nach der Nutzung

def get_job_by_id(db: Session, job_id: str):
    return db.query(Job).filter(Job.id == job_id).first()

