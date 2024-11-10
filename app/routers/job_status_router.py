from fastapi import APIRouter, HTTPException
from app.services.job_status_service import JobStatusService

router = APIRouter()

@router.get("/job-status")
async def get_job_status():
    try:
        status = JobStatusService.get_job_status()
        status['progress'] = f"{status['progress']}%"  # Formatierung: 100 -> '100%'
        return status
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
