from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.csv_upload_service import CSVUploadService
from typing import List


router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(files: List[UploadFile] = File(...)):
    # Überprüfen, ob jede Datei im CSV-Format ist
    for file in files:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=415, detail=f"Die Datei {file.filename} muss im CSV-Format sein.")
        file_name = file.filename
        if CSVUploadService.is_file_already_uploaded(file_name):
            raise HTTPException(status_code=409, detail=f"Die Datei {file.filename} ist bereits hochgeladen")
    
    # Übergabe der Dateien an den Service zur Verarbeitung
    try:
        # Verarbeite alle CSV-Dateien
        await CSVUploadService.upload_csv(files)
        return {"message": f"{len(files)} CSV-Dateien erfolgreich hochgeladen und im Speicher gespeichert"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
