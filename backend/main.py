import backend.path_fix
from fastapi import FastAPI
from backend.api.v1.api import api_router
from backend.core.config import settings
import backend.logs

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(api_router, prefix="/api/v1")
