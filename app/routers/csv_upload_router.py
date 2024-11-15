from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.csv_upload_service import CSVUploadService
from typing import List


router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(files: List[UploadFile] = File(...)):
    """
    Endpoint zum Hochladen von CSV-Dateien.

    Dieser Endpoint ermöglicht das Hochladen von mehreren CSV-Dateien. Jede Datei wird überprüft,
    um sicherzustellen, dass sie im CSV-Format vorliegt und nicht bereits zuvor hochgeladen wurde.
    Nach der Überprüfung werden die Dateien an einen Service zur weiteren Verarbeitung übergeben.
    Benutzer können durch Klicken auf die Schaltfläche "Add String Item" zusätzliche Dateien auswählen 
    und hinzufügen, die dann ebenfalls hochgeladen werden können.

    Args:
        files (List[UploadFile]): Eine Liste von Dateien, die als CSV-Dateien hochgeladen werden sollen.

    Returns:
        dict: Ein Dictionary mit einer Bestätigungsmeldung:
            - Wenn der Upload erfolgreich war: {"message": "X CSV-Dateien erfolgreich hochgeladen und im Speicher gespeichert"}

    Raises:
        HTTPException:
            - 415: Wenn eine Datei nicht im CSV-Format ist.
            - 409: Wenn die Datei bereits hochgeladen wurde.
            - 500: Bei einem internen Fehler während des Uploads.
    """

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
