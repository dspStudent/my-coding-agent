from sqlalchemy.orm import Session
from backend import models


def create_resume(
    db: Session, user_id: int, filename: str, storage_url: str, parsed_json: str
):
    db_resume = models.Resume(
        user_id=user_id,
        filename=filename,
        storage_url=storage_url,
        parsed_json=parsed_json,
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume
