import inspect
import json
from functools import wraps

from celery.exceptions import MaxRetriesExceededError
from db.db_connection import Session
from db.db_helper import add_log, update_log_failure, update_log_success
from kombu.exceptions import OperationalError
from logs.get_logger import logger

session = Session()


def is_serializable(obj):
    """Checks if an object is serializable to JSON

    Args:
        obj: The object to check for serializability

    Returns:
        bool: True if the object is serializable, False otherwise
    """
    try:
        json.dumps(obj)
        return True
    except (TypeError, ValueError):
        return False


def serialize_arg(arg):
    """Serialize an argument to JSON if possible; otherwise, convert to string

    Args:
        arg: The argument to be serialized

    Returns:
        str: The serialized or string representation of the argument
    """
    if is_serializable(arg):
        return arg
    return str(arg)


def get_function_arguments_as_string(func, *args, **kwargs):
    """Get the string representation of function arguments

    Args:
        func: The function whose arguments are to be serialized
        args: Positional arguments for the function
        kwargs: Keyword arguments for the function

    Returns:
        str: The string representation of function arguments
    """
    sig = inspect.signature(func)

    # Create a dictionary of positional arguments and keyword arguments
    args_dict = {name: serialize_arg(arg) for name, arg in zip(sig.parameters, args)}
    kwargs_dict = {
        name: serialize_arg(arg)
        for name, arg in kwargs.items()
        if name in sig.parameters
    }

    all_args = {**args_dict, **kwargs_dict}
    args_str = json.dumps(all_args)

    return args_str


def log_to_database(func):
    """Decorator to log task execution details to the database"""

    @wraps(func)
    def wrapper(*args, **kwargs):

        # Get the task id from the task function
        task_id = kwargs.get("self", args[0]).request.id
        try:
            # Add a new log record with the request data for the function call
            log_id = add_log(
                session,
                task_id,
                request_data=get_function_arguments_as_string(func, *args, **kwargs),
            )
            result = func(*args, **kwargs)
            logger.info("Task completed")

            # Log task completion to the database
            task_log = update_log_success(session, log_id)
            logger.info(f"Task log updated: {task_log.id=}")

            return result

        except (
            MaxRetriesExceededError,
            OperationalError,
        ) as exc:
            # Incase of max memory or other process fault error
            # and retry case exceeded error, update the corresponding log with retry metadata
            # so that it can be run again later using the database record
            logger.exception(exc)
            task_log = update_log_failure(session, log_id, remarks=str(exc), retry=True)
            logger.info(f"Task log updated: {task_log.id=}")

        except Exception as exc:
            # Incase of any other errors, just log the task failure
            logger.exception(f"Task failed. Reason: {exc}")
            task_log = update_log_failure(session, log_id, remarks=str(exc))
            logger.info(f"Task log updated: {task_log.id=}")

    return wrapper
