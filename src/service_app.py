import os

from fastapi import FastAPI
from route.router import api_router
from redis_server import run_redis_server

run_redis_server()
print("Running on port service_app.py")
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True})
app.include_router(api_router, prefix="/api", tags=["api"])
