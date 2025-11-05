from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.db import crud
from backend.services import auth_service
from backend.db.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.UserDataSourceConfig)
def create_user_data_source_config(
    config: schemas.UserDataSourceConfigCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user),
):
    db_config = crud.create_or_update_user_data_source(
        db=db, user_id=current_user.id, config=config
    )
    if not db_config:
        raise HTTPException(status_code=404, detail="Data source not found")
    return db_config
