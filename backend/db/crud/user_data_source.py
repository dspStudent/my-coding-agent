from sqlalchemy.orm import Session
from backend import models, schemas
from backend.core.encryption import encrypt

def create_or_update_user_data_source(db: Session, user_id: int, config: schemas.UserDataSourceConfigCreate):
    data_source = db.query(models.DataSource).filter(models.DataSource.key == config.data_source_key).first()
    if not data_source:
        return None

    db_config = db.query(models.UserDataSourceConfig).filter(
        models.UserDataSourceConfig.user_id == user_id,
        models.UserDataSourceConfig.data_source_id == data_source.id
    ).first()

    if db_config:
        db_config.is_enabled = config.is_enabled
        db_config.is_paid = config.is_paid
        if config.encrypted_credentials:
            db_config.encrypted_credentials = encrypt(config.encrypted_credentials)
        db_config.config_json = config.config_json
    else:
        db_config = models.UserDataSourceConfig(
            user_id=user_id,
            data_source_id=data_source.id,
            is_enabled=config.is_enabled,
            is_paid=config.is_paid,
            encrypted_credentials=encrypt(config.encrypted_credentials) if config.encrypted_credentials else None,
            config_json=config.config_json,
        )
        db.add(db_config)

    db.commit()
    db.refresh(db_config)
    return db_config

def get_user_data_source_by_user_id_and_key(db: Session, user_id: int, key: str):
    return (
        db.query(models.UserDataSourceConfig)
        .join(models.DataSource)
        .filter(
            models.UserDataSourceConfig.user_id == user_id,
            models.DataSource.key == key,
            models.UserDataSourceConfig.is_enabled == 1,
        )
        .first()
    )

def get_user_data_sources_by_user_id_and_type(db: Session, user_id: int, type: str):
    return (
        db.query(models.UserDataSourceConfig)
        .join(models.DataSource)
        .filter(
            models.UserDataSourceConfig.user_id == user_id,
            models.DataSource.type == type,
            models.UserDataSourceConfig.is_enabled == 1,
        )
        .all()
    )
