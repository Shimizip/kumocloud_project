from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.csv_upload_service import all_uploaded_csvs

router = APIRouter()

@router.get("/check-uploaded-data")
async def check_uploaded_data(
    num_rows: int = 5,
    file_name: Optional[str] = Query(
        None,
        title="Dateiname",
        description="Gib den Namen der hochgeladenen Datei ein, die du überprüfen möchtest",
    ),
):
    # Überprüfung, ob der Dateiname in all_uploaded_csvs existiert
    file_data = next((item["data"] for item in all_uploaded_csvs if item["file_name"] == file_name), None)
    
    if file_data is None:
        raise HTTPException(status_code=404, detail="Die angegebene Datei wurde nicht gefunden.")
    
    # Gib die gewünschten Zeilen zurück
    data_preview = file_data.head(num_rows)
    return {"message": "Datenüberprüfung erfolgreich", "data_preview": data_preview.to_dict()}
