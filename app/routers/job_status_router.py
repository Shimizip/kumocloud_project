from fastapi import APIRouter, HTTPException
from app.services.job_status_service import JobStatusService

router = APIRouter()

@router.get("/job-status")
async def get_job_status():
    """
    Endpoint zur Abfrage des aktuellen Status eines Jobs.

    Dieser Endpoint ruft den aktuellen Status eines laufenden oder abgeschlossenen Jobs ab,
    einschließlich des Fortschritts in Prozent. Falls ein Fehler auftritt, wird eine detaillierte Fehlermeldung zurückgegeben.

    Returns:
        dict: Ein Dictionary mit dem aktuellen Job-Status, einschließlich des Fortschritts in Prozent.
        
    Raises:
        HTTPException:
            - 400: Bei einem Fehler während der Abfrage des Job-Status.
    """
    try:
        status = JobStatusService.get_job_status()
        status['progress'] = f"{status['progress']}%"  # Formatierung: 100 -> '100%'
        return status
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
