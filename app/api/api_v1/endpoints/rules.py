from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.core.db import get_db
from app.models.user import User
from app.schemas.rule import Rule, RuleCreate
from app.services.rule_service import rule_service

router = APIRouter()


@router.post("/", response_model=Rule)
def create_rule(
    rule_in: RuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return rule_service.create_rule(db=db, rule_in=rule_in)


@router.get("/", response_model=List[Rule])
def read_rules(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
):
    return rule_service.get_rules(db=db, skip=skip, limit=limit)


@router.get("/{rule_id}", response_model=Rule)
def read_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    rule = rule_service.get_rule(db=db, rule_id=rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.delete("/{rule_id}", response_model=Rule)
def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    rule = rule_service.delete_rule(db=db, rule_id=rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule
