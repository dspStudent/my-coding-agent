from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.services import job_discovery_service
from backend.services import auth_service
from backend.db.database import get_db

router = APIRouter()


@router.post("/run")
async def run_discovery(
    query: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user),
):
    jobs = await job_discovery_service.run_discovery(
        db=db, user_id=current_user.id, query=query
    )
    return jobs
