from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.models.user import Base

class ScheduledEmail(Base):
    __tablename__ = "scheduled_emails"

    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String, index=True, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    send_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="pending")  # pending, sent, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)