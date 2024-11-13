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

    Args:
        file_name (str): Name der CSV-Datei, für die die Job-IDs abgerufen werden sollen.
    
    Returns:
        list: Liste der Job-IDs, die mit der angegebenen CSV-Datei verknüpft sind.
    """
    try:
        job_ids = JobService.get_job_ids_by_csv(db, file_name)
        if not job_ids:
            raise HTTPException(status_code=404, detail="Keine Jobs gefunden, die mit der angegebenen CSV-Datei verknüpft sind.")
        return {"job_ids": job_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
