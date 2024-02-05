from celery import Celery

# Create the celery object, and set using config from file
celery = Celery(__name__)
celery.config_from_object("celeryconfig")
