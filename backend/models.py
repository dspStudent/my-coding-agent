from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String)
    created_at = Column(DateTime, default=func.now())
    senders = relationship("Sender", back_populates="user")
    resumes = relationship("Resume", back_populates="user")
    user_data_source_configs = relationship("UserDataSourceConfig", back_populates="user")
    discovery_runs = relationship("DiscoveryRun", back_populates="user")
    sends = relationship("Send", back_populates="user")
    suppressions = relationship("Suppression", back_populates="user")
    rate_limits = relationship("RateLimit", back_populates="user")
    email_templates = relationship("EmailTemplate", back_populates="user")


class Sender(Base):
    __tablename__ = "senders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    email = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    display_name = Column(String)
    encrypted_token = Column(String)
    verified = Column(Integer, default=0)
    daily_limit = Column(Integer, default=50)
    created_at = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="senders")
    sends = relationship("Send", back_populates="sender")
    rate_limits = relationship("RateLimit", back_populates="sender")


class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String)
    storage_url = Column(String)
    parsed_json = Column(String)
    created_at = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="resumes")
    sends = relationship("Send", back_populates="resume")


class DataSource(Base):
    __tablename__ = "data_sources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    is_paid = Column(Integer, nullable=False, default=0)
    requires_keys = Column(Integer, nullable=False, default=0)
    config_schema_json = Column(String)
    enabled = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=func.now())
    user_data_source_configs = relationship("UserDataSourceConfig", back_populates="data_source")


class UserDataSourceConfig(Base):
    __tablename__ = "user_data_source_configs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False)
    is_enabled = Column(Integer, nullable=False, default=1)
    is_paid = Column(Integer, nullable=False, default=0)
    encrypted_credentials = Column(String)
    config_json = Column(String)
    created_at = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="user_data_source_configs")
    data_source = relationship("DataSource", back_populates="user_data_source_configs")


class DiscoveryRun(Base):
    __tablename__ = "discovery_runs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    since_datetime = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="queued")
    stats_json = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="discovery_runs")
    job_postings = relationship("JobPosting", back_populates="discovery_run")


class JobPosting(Base):
    __tablename__ = "job_postings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    discovery_run_id = Column(Integer, ForeignKey("discovery_runs.id"))
    source_key = Column(String, nullable=False)
    external_id = Column(String)
    job_title = Column(String)
    company = Column(String)
    location = Column(String)
    posting_url = Column(String)
    posting_date = Column(DateTime)
    raw_json = Column(String)
    discovered_at = Column(DateTime, default=func.now())
    discovery_run = relationship("DiscoveryRun", back_populates="job_postings")
    contacts = relationship("Contact", back_populates="job_posting")


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"))
    email = Column(String)
    name = Column(String)
    role = Column(String)
    confidence = Column(Float, default=0.5)
    validated = Column(Integer, default=0)
    validation_status = Column(String)
    source_key = Column(String)
    created_at = Column(DateTime, default=func.now())
    job_posting = relationship("JobPosting", back_populates="contacts")
    sends = relationship("Send", back_populates="contact")


class EmailTemplate(Base):
    __tablename__ = "email_templates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    subject_template = Column(String, nullable=False)
    body_template = Column(String, nullable=False)
    is_system = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="email_templates")


class Send(Base):
    __tablename__ = "sends"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("senders.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    subject = Column(String)
    body = Column(String)
    status = Column(String, nullable=False, default="queued")
    provider_message_id = Column(String)
    error = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="sends")
    sender = relationship("Sender", back_populates="sends")
    contact = relationship("Contact", back_populates="sends")
    resume = relationship("Resume", back_populates="sends")


class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    provider = Column(String)
    event_type = Column(String)
    event_json = Column(String)
    message_id = Column(String)
    received_at = Column(DateTime, default=func.now())


class Suppression(Base):
    __tablename__ = "suppressions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String, nullable=False)
    reason = Column(String)
    created_at = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="suppressions")


class RateLimit(Base):
    __tablename__ = "rate_limits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sender_id = Column(Integer, ForeignKey("senders.id"))
    max_per_hour = Column(Integer, default=20)
    max_per_day = Column(Integer, default=50)
    user = relationship("User", back_populates="rate_limits")
    sender = relationship("Sender", back_populates="rate_limits")
