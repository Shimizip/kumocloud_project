# app/routers/csv_upload_router.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.csv_upload_service import CSVUploadService

router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=415, detail="Datei muss im CSV-Format sein.")
    
    # Übergabe der Datei an den Service zur Verarbeitung
    try:
        CSVUploadService.process_csv(file)
        return {"message": "CSV-Datei erfolgreich hochgeladen und im Speicher gespeichert"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
