# app/routers/intent_router.py
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from app.services.start_intent_detection_service import IntentService

router = APIRouter()

@router.post("/start-intent-detection")
async def start_intent_detection(background_tasks: BackgroundTasks, max_intentions: int = Query(5, ge=1, le=10, description="Maximale Anzahl von Intentionen (1-10)")):
    """
    Endpoint zur Ausführung der Intent-Erkennung auf hochgeladenen Daten.
    
    Args:
        max_intentions (int): Maximale Anzahl der zurückzugebenden Intentionen (Standard: 5)
    
    Returns:
        dict: Ergebnisse der Intent-Erkennung mit den häufigsten Intentionen und ggf. Fallback.
    """
    try:
        # Übergabe des dynamisch festgelegten Wertes für max_intentions an den Hintergrundjob
        return await IntentService.detect_intents(background_tasks, max_intentions=max_intentions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
