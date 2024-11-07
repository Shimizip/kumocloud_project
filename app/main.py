from fastapi import FastAPI
from app.routers import (
    csv_upload_router,
    csv_upload_check_router,
    start_intent_detection_router,
    job_status_router,
    job_cancel_router,
    job_filter_router
)

app = FastAPI()

# Registriere die Routen
app.include_router(csv_upload_router.router, prefix="/upload", tags=["Upload CSV"])
app.include_router(csv_upload_check_router.router, prefix="/check-upload", tags=["Check Upload"])
app.include_router(start_intent_detection_router.router, prefix="/intent-detection", tags=["Intent Detection"])
#app.include_router(job_status_router.router, prefix="/job-status", tags=["Job Status"])
#app.include_router(job_cancel_router.router, prefix="/cancel-job", tags=["Cancel Job"])
#app.include_router(job_filter_router.router, prefix="/filter-results", tags=["Filter Results"])

# Optional: Root-Route für einen einfachen Begrüßungstext
@app.get("/")
async def root():
    return {"message": "Willkommen zur Intent Detection API"}
