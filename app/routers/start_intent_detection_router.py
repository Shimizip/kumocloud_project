# app/routers/intent_router.py
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, Depends
from app.services.start_intent_detection_service import IntentService
from app.database.database_service import get_db
from app.services.job_status_service import JobStatusService
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

    Dieser Endpoint führt eine Intent-Erkennung auf den hochgeladenen CSV-Daten durch. Die Anzahl der maximal
    zurückzugebenden Intentionen kann durch den Parameter `max_intentions` (1-10) angepasst werden.
    Der Datei-Name, für die die Intent-Erkennung durchgeführt wird, wird ebenfalls als Eingabeparameter erwartet.
    Es wird immer nur ein Job gestartet.

    Args:
        max_intentions (int): Maximale Anzahl der zurückzugebenden Intentionen (Standard: 5).
            Die Zahl muss zwischen 1 und 10 liegen.
        file_name (str, optional): Der Name der Datei, für die die Intent-Erkennung durchgeführt werden soll.

    Returns:
        dict: Ein Dictionary, das die Ergebnisse der Intent-Erkennung enthält, einschließlich der häufigsten Intentionen 
              und ggf. einem Fallback für Nachrichten ohne erkannte Intentionen.

    Raises:
        HTTPException:
            - 404: Wenn die angegebene Datei nicht gefunden wird.
            - 500: Bei einem Fehler während der Durchführung der Intent-Erkennung.
    """
    file_data = next((item["data"] for item in all_uploaded_csvs if item["file_name"] == file_name), None)

    if file_data is None:
        raise HTTPException(status_code=404, detail="Die angegebene Datei wurde nicht gefunden.")
    
            # Überprüfen, ob bereits ein Job läuft
    if JobStatusService.check_if_job_in_progress() :
        raise HTTPException(status_code=400, detail="Es läuft bereits ein Job. Bitte warten Sie, bis der aktuelle Job abgeschlossen ist.")
    
    try:
        # Übergabe des dynamisch festgelegten Wertes für max_intentions an den Hintergrundjob
        return await IntentService.detect_intents(background_tasks, db,  max_intentions=max_intentions, file_name=file_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
