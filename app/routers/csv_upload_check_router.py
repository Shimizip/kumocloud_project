# app/routers/csv_upload_check_router.py
from fastapi import APIRouter, HTTPException
from app.services.csv_upload_check_service import DataCheckService

router = APIRouter()

@router.get("/check-uploaded-data")
async def check_uploaded_data(num_rows: int = 5):  # Parameter für die Anzahl der Zeilen hinzufügen
    try:
        data_preview = DataCheckService.check_uploaded_data(num_rows=num_rows)  # Parameter weitergeben
        return {"message": "Datenüberprüfung erfolgreich", "data_preview": data_preview}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
