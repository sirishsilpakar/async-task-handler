import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class LogStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True)

    task_id = Column(String, nullable=False)
    request_data = Column(String)
    status = Column(Enum(LogStatus), default=LogStatus.PENDING)
    completed = Column(Boolean, default=False)
    retry = Column(Boolean, default=False)
    remarks = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)
