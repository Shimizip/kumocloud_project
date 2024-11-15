# app/routers/job_cancel_router.py
from fastapi import APIRouter, HTTPException
from app.services.job_status_service import JobStatusService
from app.services.job_status_service import jobStatus

router = APIRouter()

@router.post("/cancel-job")
async def cancel_job():
    """
    Endpoint zum Abbrechen eines laufenden Intent-Erkennungs-Jobs.

    Dieser Endpoint überprüft, ob ein Job aktuell im Status "in progress" ist. Falls ja, 
    wird der Job abgebrochen und der Status auf "canceled" gesetzt. Wenn kein Job 
    gestartet wurde, gibt der Endpoint eine Nachricht zurück, dass kein Job zum Abbrechen existiert.

    Args:
        Keine Eingabeparameter erforderlich.

    Returns:
        dict: Ein Dictionary mit einer Bestätigungsmeldung:
            - Wenn der Job abgebrochen wurde: {"message": "Job wurde erfolgreich abgebrochen."}
            - Wenn kein Job gestartet wurde: {"message": "Noch kein Job gestartet."}
        
    Raises:
        HTTPException: Bei Fehlern wird eine HTTPException mit Statuscode 400 zurückgegeben.
    """
    try:
        # Job als abgebrochen markieren
        if jobStatus["status"] == "in progress" :     
            JobStatusService.cancel_job()
            return {"message": "Job wurde erfolgreich abgebrochen."}
        else : 
            return {"message": "Noch kein Job gestartet. "}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
