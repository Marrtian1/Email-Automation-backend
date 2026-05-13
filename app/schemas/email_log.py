from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmailLogBase(BaseModel):
    recipient: str
    subject: str
    status: str
    timestamp: Optional[datetime] = None
    user_id: int

class EmailLogCreate(EmailLogBase):
    pass

class EmailLog(EmailLogBase):
    id: int

    class Config:
        from_attributes = True
