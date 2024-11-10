# app/routers/job_cancel_router.py
from fastapi import APIRouter, HTTPException
from app.services.job_status_service import JobStatusService

router = APIRouter()

@router.post("/cancel-job")
async def cancel_job():
    try:
        # Job als abgebrochen markieren
        JobStatusService.cancel_job()
        return {"message": "Job wurde erfolgreich abgebrochen."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
