from sqlalchemy.orm import Session
from backend import models, schemas
from backend.core.encryption import encrypt

def get_data_source_by_key(db: Session, key: str):
    return db.query(models.DataSource).filter(models.DataSource.key == key).first()

def create_or_update_user_data_source(
    db: Session, user_id: int, config: schemas.UserDataSourceConfigCreate
):
    data_source = get_data_source_by_key(db, config.data_source_key)
    if not data_source:
        return None

    db_config = (
        db.query(models.UserDataSourceConfig)
        .filter(
            models.UserDataSourceConfig.user_id == user_id,
            models.UserDataSourceConfig.data_source_id == data_source.id,
        )
        .first()
    )

    if db_config:
        db_config.is_enabled = config.is_enabled
        db_config.is_paid = config.is_paid
        db_config.encrypted_credentials = encrypt(config.credentials)
        db_config.config_json = config.config_json
    else:
        db_config = models.UserDataSourceConfig(
            user_id=user_id,
            data_source_id=data_source.id,
            is_enabled=config.is_enabled,
            is_paid=config.is_paid,
            encrypted_credentials=encrypt(config.credentials),
            config_json=config.config_json,
        )
        db.add(db_config)

    db.commit()
    db.refresh(db_config)
    return db_config
