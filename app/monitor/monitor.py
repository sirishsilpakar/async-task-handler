from datetime import datetime, timedelta

from celery.result import AsyncResult
from db.db_connection import Session
from db.db_helper import update_log
from db.models import LogStatus, TaskLog
from logs.get_logger import logger
from worker.worker import celery

session = Session()


TIMEOUT_LIMIT_IN_MINS = 30


@celery.task
def monitor_pending_tasks(timeout_minutes=TIMEOUT_LIMIT_IN_MINS):
    """Monitors pending and failed tasks in the task log table.
        This task will be scheduled to run periodically to handle silent failure cases

    Args:
        timeout_minutes (int, optional): The duration after which tasks are considered pending for too long (default is 30)
    """
    # Get all tasks that are still pending after a certain timeout
    pending_tasks = (
        session.query(TaskLog)
        .filter(
            (
                (TaskLog.status == LogStatus.PENDING)
                | (TaskLog.status == LogStatus.FAILED)
            )
            & (
                TaskLog.timestamp
                < datetime.utcnow() - timedelta(minutes=timeout_minutes)
            )
        )
        .all()
    )

    # For each task, attemp to run it again
    for task in pending_tasks:
        task_id = task.task_id
        task_log_id = task.id

        result = AsyncResult(task_id, app=celery)
        if result.state == "PENDING":
            logger.info(f"Task {task_id} is still pending. Logging and retrying...")
            update_log(session, task_log_id, LogStatus.PENDING)
            celery.tasks[task_id].retry()
