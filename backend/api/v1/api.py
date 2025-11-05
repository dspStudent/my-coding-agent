from fastapi import APIRouter
from backend.api.v1.endpoints import auth, resumes, user_data_sources

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(
    user_data_sources.router, prefix="/user/datasources", tags=["user_data_sources"]
)
