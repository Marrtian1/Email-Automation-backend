from pydantic import BaseModel
from typing import Dict, Any


class RuleBase(BaseModel):
    trigger_type: str
    condition: Dict[str, Any]
    template_id: int


class RuleCreate(RuleBase):
    pass


class Rule(RuleBase):
    id: int

    class Config:
        from_attributes = True
