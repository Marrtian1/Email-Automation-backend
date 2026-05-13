from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TemplateBase(BaseModel):
    name: str
    subject: str
    body: str

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(TemplateBase):
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None

class Template(TemplateBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
