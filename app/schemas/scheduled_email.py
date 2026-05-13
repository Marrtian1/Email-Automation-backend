from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ScheduledEmailBase(BaseModel):
    recipient: EmailStr
    subject: str
    body: str
    send_time: datetime

class ScheduledEmailCreate(ScheduledEmailBase):
    pass

class ScheduledEmailUpdate(BaseModel):
    status: Optional[str] = None

class ScheduledEmail(ScheduledEmailBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True