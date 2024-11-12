# app/routers/intent_router.py
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, Depends
from app.services.start_intent_detection_service import IntentService
from app.database.database_service import get_db
from sqlalchemy.orm import Session
from typing import Optional
from app.services.csv_upload_service import all_uploaded_csvs


router = APIRouter()

@router.post("/start-intent-detection")
async def start_intent_detection(background_tasks: BackgroundTasks, 
                                 db: Session = Depends(get_db), 
                                 max_intentions: int = Query(5, 
                                                             ge=1, 
                                                             le=10, 
                                                             description="Maximale Anzahl von Intentionen (1-10)"),
                                 file_name: Optional[str] = Query(
                                    None,
                                    title="Dateiname",
                                    description="Gib den Namen der hochgeladenen Datei ein, bei der eine Intent Detection statt finden soll",
                                ),):
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
    
    try:
        # Übergabe des dynamisch festgelegten Wertes für max_intentions an den Hintergrundjob
        return await IntentService.detect_intents(background_tasks, db,  max_intentions=max_intentions, file_name=file_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
