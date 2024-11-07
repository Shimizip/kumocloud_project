# app/services/csv_upload_check_service.py
from app.services.csv_upload_service import uploaded_csv_data

class DataCheckService:
    @staticmethod
    def check_uploaded_data():
        if "data" not in uploaded_csv_data:
            raise ValueError("Keine hochgeladene CSV-Datei gefunden.")
        
        # Hier kannst du die Überprüfung der Daten durchführen
        df = uploaded_csv_data["data"]
        
        # Überprüfe, ob die DataFrame die notwendigen Spalten hat
        required_columns = {"question", "created_at"}
        if not required_columns.issubset(df.columns):
            raise ValueError("Die hochgeladene CSV-Datei hat nicht die erforderlichen Spalten.")
        
        # Weitere Prüfungen können hier durchgeführt werden

        return df.head()  # Beispiel: Gib die ersten 5 Zeilen zurück
