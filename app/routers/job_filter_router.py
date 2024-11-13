# app/routers/intent_router.py
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, Depends
from app.services.start_intent_detection_service import IntentService
from app.database.database_service import get_db
from app.services.job_filter_service import JobFilter, Order
from sqlalchemy.orm import Session
from typing import Optional
from app.services.csv_upload_service import all_uploaded_csvs
from datetime import datetime



router = APIRouter()

@router.get("/filter-results")
async def job_filter(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None, description="Startdatum (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="Enddatum (YYYY-MM-DD)"),
    file_name: Optional[str] = Query(None, title="Dateiname", description="Gib den Namen der Datei an, für die gefiltert werden soll"),
    job_id: Optional[str] = Query(None, title="Job ID", description="Gib die Job-ID ein, für dessen die Ergebnisse der Intent Detetion zurück gegebn werden sollen"),
    order: Order = Query(Order.desc, description="Sortierreihenfolge: 'desc' für häufigste zuerst, 'asc' für am wenigsten häufige zuerst")
):
    """
    Endpoint zur Ausführung der Intent-Erkennung auf hochgeladenen Daten.
    
    Args:
        max_intentions (int): Maximale Anzahl der zurückzugebenden Intentionen (Standard: 5)
    
    Returns:
        dict: Ergebnisse der Intent-Erkennung mit den häufigsten Intentionen und ggf. Fallback.
    
    """
    file_data = next((item["data"] for item in all_uploaded_csvs if item["file_name"] == file_name), None)

    if file_data is None:
        raise HTTPException(status_code=404, detail="Die angegebene Datei wurde nicht gefunden.")
    if start_date and end_date and end_date < start_date:
            raise HTTPException(status_code=400, detail="Das Enddatum darf nicht vor dem Startdatum liegen.")

    try:
        # Ausführen der Filterung in JobFilter
        filtered_results = await JobFilter.filter_jobs(db, start_date, end_date, file_name, job_id, order.value)
        return {"filtered_results": filtered_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
