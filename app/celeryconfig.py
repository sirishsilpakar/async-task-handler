import os

# Config file for celery

broker_url = os.environ.get("CELERY_BROKER_URL")
result_backend = os.environ.get("CELERY_RESULT_BACKEND")
imports = ["usecase.task"]
