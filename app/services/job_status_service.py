# Globale Variable für den Job-Status und Fortschritt
jobStatus = {"status": "not started", "progress": 0, "is_canceled": False, "job_id": None, "csv_name": None}

class JobStatusService:
    @staticmethod
    def set_job_status(status: str, progress: int):
        jobStatus["status"] = status
        jobStatus["progress"] = progress

    @staticmethod
    def get_job_status():
        return jobStatus
    
    @staticmethod
    def cancel_job():
        jobStatus["status"] = "canceled"
        jobStatus["is_canceled"] = True

    @staticmethod
    def clear_job():
        jobStatus["status"] = "not started"
        jobStatus["progress"] = 0
        jobStatus["is_canceled"] = False
        jobStatus["job_id"] = None
    
    @staticmethod
    def check_if_job_in_progress() -> bool:
        return jobStatus["status"] == "in progress"

    

