import os
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Initialisiere das Datenbankmodell
Base = declarative_base()

class Job(Base):
    __tablename__ = "all_jobs"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, index=True)
    progress = Column(Integer)
    result = Column(JSON)  # Speichert die Intentionsergebnisse als JSON
    csv_name = Column(String, index=True)
    limit = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Erstelle den Pfad für die Datenbankdatei
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "all_jobs.db")

# Erstelle die SQLite-Engine
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialisiere die Tabellen, wenn die Datenbankdatei noch nicht existiert
if not os.path.exists(db_path):
    Base.metadata.create_all(bind=engine)
