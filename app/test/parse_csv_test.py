import pandas as pd

import os
import sys

# Füge den Hauptprojektordner zum Modulpfad hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.utils.csv_handler import parse_csv  # Importiere die parse_csv-Funktion

def test_parse_csv_with_real_file(input_file_path, output_file_path):
    # Öffne die echte CSV-Datei und verwende parse_csv darauf
    with open(input_file_path, 'rb') as f:
        class MockUploadFile:
            def __init__(self, file):
                self.file = file

        # Erstelle ein MockUploadFile-Objekt für parse_csv
        mock_file = MockUploadFile(f)
        
        # Verwende parse_csv, um die Daten zu bereinigen und zu formatieren
        df = parse_csv(mock_file)
    
    # Speichere das bereinigte DataFrame in eine neue CSV-Datei
    df.to_csv(output_file_path, index=False, encoding='utf-8')
    
    print(f"Geparste und bereinigte Daten wurden erfolgreich in {output_file_path} gespeichert.")

# Beispielverwendung
input_file_path = 'app/random_data_szymon.csv'  # Pfad zur Originaldatei
output_file_path = '/home/shimi/Documents/kumocloud_project/app/parse_random_data_szymon.csv'  # Pfad zur Ausgabe, z.B. "parsed_output.csv"
test_parse_csv_with_real_file(input_file_path, output_file_path)
