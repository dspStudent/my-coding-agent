from sqlalchemy.orm import Session
from backend import models, schemas
from backend.security import get_password_hash


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_data_source_by_user_id_and_type(db: Session, user_id: int, type: str):
    return (
        db.query(models.UserDataSourceConfig)
        .join(models.DataSource)
        .filter(
            models.UserDataSourceConfig.user_id == user_id,
            models.DataSource.type == type,
            models.UserDataSourceConfig.is_enabled == 1,
        )
        .first()
    )
