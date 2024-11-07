# app/models.py
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class CustomerQuery(Base):
    __tablename__ = "customer_queries"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
