import types
from datetime import datetime

import requestvars
from fastapi import Request
from logs.get_logger import logger
from uuid6 import uuid7


async def log_request(request: Request, call_next):
    """Middleware to log each request's successful execution

    Args:
        request (Request): A FastAPI request object
        call_next (function): Next func to execute

    Returns:
        Response: A FastAPI response object
    """
    start_time = datetime.utcnow()

    request_data = types.SimpleNamespace(id=str(uuid7()))
    requestvars.request_global.set(request_data)

    logger.info(f"Endpoint {request.url.path} called!")

    response = await call_next(request)

    elapsed_time = datetime.utcnow() - start_time

    logger.info(
        f"Endpoint {request.url.path} completed successfully in {elapsed_time.total_seconds():.5f} seconds"
    )

    return response
