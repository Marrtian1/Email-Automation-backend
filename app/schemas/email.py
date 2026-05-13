from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any

class EmailBase(BaseModel):
    subject: str
    recipient: EmailStr
    body: Optional[str] = None
    template_id: Optional[int] = None
    placeholders: Optional[Dict[str, Any]] = None
    is_html: bool = True

class EmailCreate(EmailBase):
    pass

class EmailBulkSend(BaseModel):
    subject: str
    recipients: List[EmailStr]
    body: Optional[str] = None
    template_id: Optional[int] = None
    placeholders: Optional[Dict[str, Any]] = None # Global placeholders
    is_html: bool = True

class EmailResponse(BaseModel):
    id: int
    recipient: str
    subject: str
    status: str

    class Config:
        from_attributes = True
