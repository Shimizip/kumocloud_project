# Globale Variable für den Job-Status und Fortschritt
jobStatus = {"status": "not started", "progress": 0, "is_canceled": False, "job_id": None, "csv_name": None}

class JobStatusService:
    @staticmethod
    def set_job_status(status: str, progress: int):
        # Setzt den Job-Status und Fortschritt
        jobStatus["status"] = status
        jobStatus["progress"] = progress

    @staticmethod
    def get_job_status():
        # Gibt den aktuellen Status des Jobs zurück
        return jobStatus
    
    @staticmethod
    def cancel_job():
        # Setzt den Job-Status auf 'canceled' und markiert ihn als abgebrochen
        jobStatus["status"] = "canceled"
        jobStatus["is_canceled"] = True

    @staticmethod
    def clear_job():
        # Setzt alle Job-Status-Informationen auf die Initialwerte zurück
        jobStatus["status"] = "not started"
        jobStatus["progress"] = 0
        jobStatus["is_canceled"] = False
        jobStatus["job_id"] = None
    
    @staticmethod
    def check_if_job_in_progress() -> bool:
        # Überprüft, ob der Job im Status 'in progress' ist
        return jobStatus["status"] == "in progress"
