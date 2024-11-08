# app/services/csv_upload_check_service.py
from app.services.csv_upload_service import uploaded_csv_data

class DataCheckService:
    @staticmethod
    def check_uploaded_data(num_rows: int = 5):
        if "data" not in uploaded_csv_data:
            raise ValueError("Keine hochgeladene CSV-Datei gefunden.")
        
        # Hier kannst du die Überprüfung der Daten durchführen
        df = uploaded_csv_data["data"]
        
        # Überprüfe, ob die DataFrame die notwendigen Spalten hat
        required_columns = {"question", "created_at"}
        if not required_columns.issubset(df.columns):
            raise ValueError("Die hochgeladene CSV-Datei hat nicht die erforderlichen Spalten.")
        
        # Gib die gewünschten Zeilen zurück
        return df.head(num_rows)  # Beispiel: Gib die ersten num_rows zurück
