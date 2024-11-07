from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Schema für den CSV-Upload (z. B., wenn zusätzliche Parameter benötigt werden)
class UploadSchema(BaseModel):
    filename: str
    upload_date: datetime

# Schema für das Erstellen eines Intent-Erkennungsjobs
class CreateIntentJobSchema(BaseModel):
    max_intentions: Optional[int] = 5  # Standardmäßig 5, kann optional sein

# Schema für die Rückgabe eines Jobs
class JobResponseSchema(BaseModel):
    job_id: str
    status: str  # z.B., "in_progress", "completed", "failed"
    created_at: datetime
    completed_at: Optional[datetime]

# Schema für das Abbrechen eines Jobs
class CancelJobSchema(BaseModel):
    job_id: str
    success: bool

# Schema für das Filtern der Ergebnisse eines Jobs
class FilterResultsSchema(BaseModel):
    job_id: str
    limit: Optional[int] = 10
    order: Optional[str] = "most_common"  # "most_common" oder "least_common"

# Schema für die Struktur der Intent-Erkennungsergebnisse
class IntentResultSchema(BaseModel):
    intention: str
    count: int

# Schema für die Rückgabe der gefilterten Job-Ergebnisse
class FilteredJobResultsResponse(BaseModel):
    job_id: str
    results: List[IntentResultSchema]

# Neues Schema für die Antwort des CSV-Uploads
class CSVUploadResponse(BaseModel):
    message: str
    upload_date: datetime
    data_preview: Optional[List[dict]] = None  # Vorschau der ersten Zeilen (optional)
