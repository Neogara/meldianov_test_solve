import os

from fastapi import FastAPI
from route.router import api_router

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True})

app.include_router(api_router, prefix="/api", tags=["api"])



