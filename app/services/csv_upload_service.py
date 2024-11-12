import pandas as pd
from io import BytesIO
from fastapi import UploadFile, HTTPException, File
from typing import List

# Speicher für alle hochgeladenen CSV-Dateien
uploaded_csv_data = {
    "data": None,  # Hier wird der DataFrame gespeichert
    "file_name": None,
    "job_id": None
}
all_uploaded_csvs = []  # Hier speichern wir alle DataFrames der CSV-Dateien

class CSVUploadService:
    @staticmethod
    async def upload_csv(files: List[UploadFile] = File(...)):
        """
        Liest die hochgeladene(n) CSV-Datei(en) ein und speichert die Daten in einer Liste.

        Args:
            files (List[UploadFile]): Liste der hochgeladenen CSV-Dateien.
        
        Returns:
            dict: Bestätigung, dass die Dateien erfolgreich verarbeitet wurden.
        """
        for file in files:
            try:
                content = BytesIO(file.file.read())
                # Hier kannst du das Trennzeichen anpassen, falls nötig
                df = pd.read_csv(content, sep=';')  # Angenommen, die CSV ist durch Semikolon getrennt
                uploaded_csv_data = {
                    "data": df,
                    "file_name": file.filename,
                    "job_id": None  # Optional: Falls du einen Job-Id benötigst
                }
                # Speichere die CSV-Daten in der Liste
                all_uploaded_csvs.append(uploaded_csv_data)
                file_names = [item["file_name"] for item in all_uploaded_csvs]
                print(file_names)
                print(len(file_names))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Fehler beim Verarbeiten der Datei {file.filename}: {str(e)}")
        
        return {"message": "CSV-Dateien erfolgreich hochgeladen und im Speicher verarbeitet!"}

    @staticmethod
    def get_all_csv_data():
        """
        Gibt alle hochgeladenen CSV-Daten zurück.
        
        Returns:
            list: Liste der DataFrames, die für alle hochgeladenen CSV-Dateien gespeichert wurden.
        """
        return all_uploaded_csvs
    @staticmethod
    def is_file_already_uploaded(file_name: str) -> bool:
    #Prüft, ob eine Datei mit dem gegebenen Dateinamen bereits hochgeladen wurde."""
        for uploaded_csv_data in all_uploaded_csvs:
            if uploaded_csv_data["file_name"] == file_name:
                return True
        return False
