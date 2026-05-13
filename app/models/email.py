from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.models.user import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    body = Column(Text)
    recipient = Column(String, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
