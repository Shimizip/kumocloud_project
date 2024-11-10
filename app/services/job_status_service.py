# Globale Variable für den Job-Status und Fortschritt
job_status = {"status": "not started", "progress": 0, "is_canceled": False}

class JobStatusService:
    @staticmethod
    def set_job_status(status: str, progress: int):
        job_status["status"] = status
        job_status["progress"] = progress

    @staticmethod
    def get_job_status():
        return job_status
    
    @staticmethod
    def cancel_job():
        job_status["status"] = "canceled"
        job_status["is_canceled"] = True
    

