# app/routers/job_cancel_router.py
from fastapi import APIRouter, HTTPException
from app.services.job_status_service import JobStatusService
from app.services.job_status_service import jobStatus

router = APIRouter()

@router.post("/cancel-job")
async def cancel_job():
    try:
        # Job als abgebrochen markieren
        if jobStatus["status"] == "in progress" :     
            JobStatusService.cancel_job()
            return {"message": "Job wurde erfolgreich abgebrochen."}
        else : 
            return {"message": "Noch kein Job gestartet. "}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
