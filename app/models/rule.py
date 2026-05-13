from sqlalchemy import Column, Integer, String, JSON
from app.models.user import Base

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    trigger_type = Column(String, nullable=False)  # user_registration, time_based, api_trigger
    condition = Column(JSON, nullable=False)  # JSON string for condition logic
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
