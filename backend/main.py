# TODO: The server is currently crashing with an "Internal Server Error" when running with the full authentication code.
# The issue seems to be related to the application startup, as no logs are being generated.
# This needs to be investigated and fixed.

from fastapi import FastAPI
from backend.api.v1.api import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")
