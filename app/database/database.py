from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Konfiguration der Datenbank-URL (z.B. SQLite)
DATABASE_URL = "sqlite:///./kumocloud.db"  # SQLite-Datenbank

# Erstellen des Datenbank-Engines
engine = create_engine(DATABASE_URL)

# Erstellen der SessionLocal-Klasse
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Diese Funktion wird verwendet, um eine neue Session zu erhalten
def get_db():
    db = SessionLocal()  # Neue Session wird erstellt
    try:
        yield db
    finally:
        db.close()  # Schließe die Session nach der Nutzung
