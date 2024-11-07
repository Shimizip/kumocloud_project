# create_tables.py
from app.database import Base, engine
from app.models import CustomerQuery

Base.metadata.create_all(bind=engine)
