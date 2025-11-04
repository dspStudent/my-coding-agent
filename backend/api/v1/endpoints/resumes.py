from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.services import resume_service
from backend.services import auth_service
from backend.db.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Resume)
async def create_resume(
    file: UploadFile,
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    return await resume_service.create_resume(
        db=db, user_id=current_user.id, file=file
    )
