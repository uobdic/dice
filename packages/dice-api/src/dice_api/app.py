from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .host import router as host_router
from .storage import hdfs_router

app = FastAPI()
app.include_router(host_router)
app.include_router(hdfs_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to the Dice APIs!"}


@app.get("/health")
async def health_check() -> JSONResponse:
    """
    Health check endpoint.
    Returns a JSON response with a status indicating the app is up and running.
    """
    return JSONResponse(content={"status": "healthy"}, status_code=200)
