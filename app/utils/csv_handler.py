import pandas as pd
from io import BytesIO

def parse_csv(file):
    """
    Funktion, um eine CSV-Datei zu parsen, die Nachrichten in mehreren Spalten enthält.
    Fügt die Nachrichtenspalten zusammen und extrahiert das Datum in eine separate Spalte.
    
    Args:
    - file: Ein UploadFile-Objekt von FastAPI (CSV-Datei)
    
    Returns:
    - pd.DataFrame: DataFrame mit zwei Spalten: 'question' und 'created_at'
    """
    # Dateiinhalt lesen
    content = BytesIO(file.file.read())
    
    # CSV-Datei ohne Header laden, da die Spalten dynamisch zusammengeführt werden
    df = pd.read_csv(content, header=0, sep=';', engine='python')  # Lese die Datei mit Header
    
    # Bestimme die letzte Spalte als `created_at` und den Rest als `question`
    df['created_at'] = df.iloc[:, -1]  # Letzte Spalte als Datum/Uhrzeit
    df['question'] = df.iloc[:, :-1].fillna('').apply(lambda row: ' '.join(map(str, row)).strip(), axis=1)
    
    # Behalte nur die Spalten `question` und `created_at`
    df = df[['question', 'created_at']]
    
    # Überprüfen, ob die Daten korrekt geladen wurden
    if df['question'].isnull().any() or df['created_at'].isnull().any():
        raise ValueError("Fehler beim Einlesen der CSV: Die Spalten 'question' und 'created_at' sind nicht korrekt formatiert.")
    
    return df
