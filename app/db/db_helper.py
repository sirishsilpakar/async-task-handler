import functools

from db.models import LogStatus, TaskLog
from logs.get_logger import logger


def add_log(session, task_id: str, request_data: str):
    """Adds a new record to the task log table.

    Args:
        session (sqlalchemy.orm.Session): The SQLAlchemy database session
        task_id (str): The identifier of the task
        request_data (str): The request data associated with the task

    Returns
        int: ID of the newly added task log record
    """
    logger.info("Adding new record to the table...")

    task_log = TaskLog(task_id=task_id, request_data=request_data)
    session.add(task_log)
    session.commit()

    logger.info(f"New record added to the table {TaskLog.__tablename__} ")
    return task_log.id


def update_log(
    session,
    task_log_id: int,
    status: str,
    completed: bool = False,
    retry: bool = False,
    remarks: str = "",
):
    """Updates the status and details of a task log record

    Args:
        session (sqlalchemy.orm.Session): The SQLAlchemy database session
        task_log_id (int): The ID of the task log record to be updated
        status (str): The new status of the task log (e.g., 'SUCCESS', 'FAILURE', 'RETRY', 'PENDING')
        completed (bool, optional): Indicates whether the task is completed (default is False)
        retry (bool, optional): Indicates whether the task is a retry attempt (default is False)
        remarks (str, optional): Additional remarks or comments about the task (default is an empty string)

    Returns:
        TaskLog or None: The updated TaskLog record if successful, None if the record with the given ID is not found
    """
    task_log = session.query(TaskLog).get(task_log_id)

    if task_log:
        task_log.status = status
        task_log.remarks = remarks
        task_log.completed = completed
        task_log.retry = retry

        session.commit()
        return task_log
    return None


# Create functions with predefined arguments
# to log success condition and failure condition
update_log_success = functools.partial(
    update_log, status=LogStatus.COMPLETED, completed=True
)

update_log_failure = functools.partial(update_log, status=LogStatus.FAILED)
