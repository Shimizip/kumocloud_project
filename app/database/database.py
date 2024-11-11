# app/database/db_service.py
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True, index=True)
    status = Column(String, index=True)
    progress = Column(Integer)
    result = Column(JSON)  # Speichert die Intentionsergebnisse als JSON
    csv_file = Column(LargeBinary)  # Speichert die CSV-Datei als BLOB
    csv_filename = Column(String)  # Speichert den Dateinamen der CSV
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Erstelle die Engine und Session
engine = create_engine("sqlite:///./jobs.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
