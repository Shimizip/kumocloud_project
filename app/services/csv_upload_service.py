# app/services/csv_upload_service.py
import pandas as pd
from io import BytesIO
from fastapi import UploadFile

# Speicher für die hochgeladene CSV-Datei
uploaded_csv_data = {}

class CSVUploadService:
    @staticmethod
    def process_csv(file: UploadFile):
        content = BytesIO(file.file.read())
        df = pd.read_csv(content)
        
        # Speichere die Daten in der globalen Variable
        uploaded_csv_data["data"] = df
