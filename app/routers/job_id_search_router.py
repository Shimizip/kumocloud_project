# app/routers/intent_router.py
from fastapi import APIRouter, HTTPException, Query, Depends
from app.database.database_service import get_db
from sqlalchemy.orm import Session
from typing import List
from app.services.job_id_search_service import JobService  # Importiere die JobService-Klasse

router = APIRouter()

@router.get("/jobs-by-csv")
async def get_jobs_by_csv(
    file_name: str = Query(..., title="Dateiname", description="Gib den Namen der CSV-Datei an, für die die Job-IDs abgerufen werden sollen"),
    db: Session = Depends(get_db)
) -> List[str]:
    """
    Endpoint zur Suche nach allen Job-IDs, die zu einer bestimmten CSV-Datei gehören.

    Dieser Endpoint ermöglicht die Abfrage von Job-IDs, die mit einer bestimmten CSV-Datei verknüpft sind.
    Die Job-IDs werden mithilfe des JobService aus der Datenbank abgerufen, um sicherzustellen, dass alle
    relevanten Jobs für eine angegebene Datei zurückgegeben werden.

    Args:
        file_name (str): Der Name der CSV-Datei, für die die Job-IDs abgerufen werden sollen.

    Returns:
        dict: Ein Dictionary, das eine Liste von Job-IDs enthält, die mit der angegebenen CSV-Datei verknüpft sind.
        
    Raises:
        HTTPException:
            - 404: Wenn keine Job-IDs für die angegebene CSV-Datei gefunden werden.
            - 500: Bei einem internen Fehler während der Abfrage.
    """
    try:
        job_ids = JobService.get_job_ids_by_csv(db, file_name)
        if not job_ids:
            raise HTTPException(status_code=404, detail="Keine Jobs gefunden, die mit der angegebenen CSV-Datei verknüpft sind.")
        return {"job_ids": job_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
