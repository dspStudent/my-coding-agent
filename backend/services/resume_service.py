import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from backend.db import crud
from pyresparser import ResumeParser
import json

async def create_resume(db: Session, user_id: int, file: UploadFile):
    file_id = uuid.uuid4()
    file_ext = os.path.splitext(file.filename)[1]
    storage_filename = f"{file_id}{file_ext}"
    storage_path = f"files/{user_id}/{storage_filename}"

    os.makedirs(os.path.dirname(storage_path), exist_ok=True)

    with open(storage_path, "wb") as buffer:
        buffer.write(await file.read())

    data = ResumeParser(storage_path).get_extracted_data()
    parsed_json = json.dumps({
        "name": data.get("name"),
        "skills": data.get("skills")
    })

    resume = crud.create_resume(
        db=db,
        user_id=user_id,
        filename=file.filename,
        storage_url=storage_path,
        parsed_json=parsed_json,
    )
    return resume
