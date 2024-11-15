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
    """
    Endpoint zur Überprüfung der hochgeladenen Daten.

    Dieser Endpoint ermöglicht es, die hochgeladenen CSV-Daten zu überprüfen, indem eine Vorschau der ersten
    `num_rows` Zeilen der angegebenen Datei zurückgegeben wird. Der Dateiname muss als Eingabeparameter übergeben werden.

    Args:
        num_rows (int): Die Anzahl der Zeilen, die aus der hochgeladenen Datei zurückgegeben werden sollen. (Standard: 5)
        file_name (str, optional): Der Name der Datei, deren Daten überprüft werden sollen.

    Returns:
        dict: Ein Dictionary mit einer Erfolgsmeldung und einer Vorschau der angeforderten Zeilen der hochgeladenen Datei.
        
    Raises:
        HTTPException:
            - 404: Wenn die angegebene Datei nicht gefunden wird.
    """
    
    # Überprüfung, ob der Dateiname in all_uploaded_csvs existiert
    file_data = next((item["data"] for item in all_uploaded_csvs if item["file_name"] == file_name), None)
    
    if file_data is None:
        raise HTTPException(status_code=404, detail="Die angegebene Datei wurde nicht gefunden.")
    
    # Gib die gewünschten Zeilen zurück
    data_preview = file_data.head(num_rows)
    return {"message": "Datenüberprüfung erfolgreich", "data_preview": data_preview.to_dict()}
