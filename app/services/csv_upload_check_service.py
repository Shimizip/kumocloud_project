# app/services/csv_upload_check_service.py
from app.services.csv_upload_service import all_uploaded_csvs
from typing import List

class DataCheckService:
    @staticmethod
    def check_uploaded_data(file_name: str, num_rows: int = 5):
        # Suche die gewünschte Datei basierend auf dem Dateinamen
        file_data = next((item["data"] for item in all_uploaded_csvs if item["file_name"] == file_name), None)
        #DEBUG
        print(f"Filename: {file_name}")
        if file_data is None:
            raise ValueError("Keine hochgeladene CSV-Datei gefunden.")
        
        # Überprüfe, ob die DataFrame die notwendigen Spalten hat
        required_columns = {"question", "created_at"}
        if not required_columns.issubset(file_data.columns):
            raise ValueError("Die hochgeladene CSV-Datei hat nicht die erforderlichen Spalten.")
        
        # Gib die gewünschten Zeilen zurück
        return file_data.head(num_rows)

    @staticmethod
    def get_file_choices() -> List[str]:
        """Liefert eine Liste der Dateinamen für das Dropdown-Menü."""
        return [item["file_name"] for item in all_uploaded_csvs]
