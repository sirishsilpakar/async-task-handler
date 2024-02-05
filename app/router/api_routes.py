import json

import redis
from celery.exceptions import MaxRetriesExceededError, SoftTimeLimitExceeded
from celery.result import AsyncResult
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from logs.get_logger import logger
from usecase.task import process_async_task

router = APIRouter()


@router.post("/tasks", status_code=201)
async def process_request(payload=Body(...)):
    """Endpoint to initiate a background task for processing async data

    Args:
        payload (dict): A dictionary containing the data for the async task

    Returns:
        JSONResponse: A JSON response indicating the successful initiation of the background task
    """
    data = payload["data"]
    try:
        task = process_async_task.apply_async(args=(data,))
        return JSONResponse(
            {
                "message": f"Request received. Background task will be processed with task_id: {task.id}"
            }
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"msg": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@router.get("/tasks/{task_id}")
def get_task_status(task_id):
    """Endpoint to get the status of a specific task

    Args:
        task_id (str): The ID of the task

    Returns:
        dict: A dictionary containing the task_id, task_status, and task_result
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return result

