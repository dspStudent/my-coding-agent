import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from backend.db import crud
from backend.connectors import OpenAIConnector
import json
from pypdf import PdfReader
import io

def get_parsing_connector(db: Session, user_id: int):
    # This is a placeholder for the logic to get the user's configured parsing connector
    # In a real application, you would get the user's configured data source from the database
    # and then instantiate the correct connector.
    # For now, we'll just use the OpenAI connector.
    user_data_source = crud.get_user_data_source_by_user_id_and_type(db, user_id, "parsing")
    if not user_data_source:
        return None

    from backend.core.encryption import decrypt

    if user_data_source.data_source.key == "openai":
        return OpenAIConnector(api_key=decrypt(user_data_source.encrypted_credentials))

    return None

async def create_resume(db: Session, user_id: int, file: UploadFile):
    file_id = uuid.uuid4()
    file_ext = os.path.splitext(file.filename)[1]
    storage_filename = f"{file_id}{file_ext}"
    storage_path = f"files/{user_id}/{storage_filename}"

    os.makedirs(os.path.dirname(storage_path), exist_ok=True)

    file_content = await file.read()

    with open(storage_path, "wb") as buffer:
        buffer.write(file_content)

    reader = PdfReader(io.BytesIO(file_content))
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text()

    parsing_connector = get_parsing_connector(db, user_id)
    if not parsing_connector:
        raise Exception("No parsing connector configured for this user")

    parsed_json = json.dumps(parsing_connector.parse_resume(resume_text))

    resume = crud.create_resume(
        db=db,
        user_id=user_id,
        filename=file.filename,
        storage_url=storage_path,
        parsed_json=parsed_json,
    )
    return resume
