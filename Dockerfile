# Verwende das offizielle Python 3.11 Image als Basis
FROM python:3.11-slim

# Setze den Arbeitsordner
WORKDIR /app

# Kopiere die Anforderungen in das Image
COPY requirements.txt .

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten App-Code in das Arbeitsverzeichnis
COPY . .

# Exponiere Port 8000 für die Anwendung
EXPOSE 8000

# Starte die Anwendung mit uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
