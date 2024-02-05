import random
import time

from celery.utils.log import get_logger
from worker.worker import celery

logger = get_logger(__name__)


@celery.task(bind=True, max_retries=3, retry_backoff=True)
def process_async_task(self, data):
    """An asynchronous task to process data with retry mechanism

    Args:
        self: The Celery task instance
        data (str): The data to be processed

    Returns:
        bool: True if the task is completed successfully
    """
    task_id = self.request.id

    try:
        # Simulate some asynchronous task
        logger.info(f"Task id: {task_id}")
        logger.info(f"Processing data: {data}")

        time.sleep(5)

        if data == "error":
            raise ValueError("Test error")

        logger.info(f"Task completed: {data}")
        return True
    except Exception as e:
        logger.exception(e)
        self.retry()

