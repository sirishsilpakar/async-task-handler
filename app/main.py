import os

import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from logs.get_logger import logger
from middleware.logger import log_request
from router import api_routes

app = FastAPI(title="background_tasks")

app.include_router(api_routes.router)
app.middleware("http")(log_request)


@app.get("/health")
async def check_health():
    """API health check endpoint

    Returns:
        json_object (JSONResponse): a JSONResponse object
    """
    return JSONResponse(
        content={"msg": "App is Running"}, status_code=status.HTTP_200_OK
    )


if __name__ == "__main__":
    logger.info("Uvicorn server started")

    uvicorn.run(
        "__main__:app",
        host=os.getenv("SERVER_HOST"),
        port=int(os.getenv("SERVER_PORT")),
        reload=False,
    )
