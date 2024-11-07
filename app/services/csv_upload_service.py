# app/services/csv_upload_service.py
import pandas as pd
from io import BytesIO
from fastapi import UploadFile

# Speicher für die hochgeladene CSV-Datei
uploaded_csv_data = {}

class CSVUploadService:
    @staticmethod
    def process_csv(file: UploadFile):
        """
        Liest die hochgeladene CSV-Datei ein und speichert die Daten für die spätere Verwendung.

        Args:
            file (UploadFile): Die hochgeladene CSV-Datei.

        Returns:
            None: Die Daten werden in der globalen Variable gespeichert.
        """
        content = BytesIO(file.file.read())
        
        # Hier kannst du das Trennzeichen anpassen, falls nötig
        df = pd.read_csv(content, sep=';')  # Angenommen, die CSV ist durch Semikolon getrennt
        
        # Speichere die Daten in der globalen Variable
        uploaded_csv_data["data"] = df
