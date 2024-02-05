import os

# Config file for celery

broker_url = os.environ.get("CELERY_BROKER_URL")
result_backend = os.environ.get("CELERY_RESULT_BACKEND")
imports = ["usecase.task", "monitor.monitor"]
beat_schedule = {
    "run-every-thirty-minutes": {
        "task": "monitor.monitor.monitor_pending_tasks",
        "schedule": 1800,  # 30 minutes in seconds
    }
}
