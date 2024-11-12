# app/database/database_config.py
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, index=True)
    progress = Column(Integer)
    result = Column(JSON)  # Speichert die Intentionsergebnisse als JSON
    csv_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Erstelle die Engine und Session
engine = create_engine("sqlite:///./jobs.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
