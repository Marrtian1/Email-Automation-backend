from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.core.db import get_db
from app.models.user import User
from app.schemas.scheduled_email import ScheduledEmail, ScheduledEmailCreate
from app.services.scheduler_service import scheduler_service

router = APIRouter()

@router.post("/", response_model=ScheduledEmail)
def schedule_email(
    email_in: ScheduledEmailCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if email_in.send_time <= datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="send_time must be in the future")
    return scheduler_service.schedule_email(db=db, email_in=email_in, user_id=current_user.id)

@router.get("/", response_model=List[ScheduledEmail])
def read_scheduled_emails(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
):
    return scheduler_service.get_scheduled_emails(db=db, skip=skip, limit=limit)

@router.get("/{email_id}", response_model=ScheduledEmail)
def read_scheduled_email(
    email_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    email = scheduler_service.get_scheduled_email(db=db, email_id=email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Scheduled email not found")
    return email

@router.delete("/{email_id}", response_model=ScheduledEmail)
def delete_scheduled_email(
    email_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    email = scheduler_service.delete_scheduled_email(db=db, email_id=email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Scheduled email not found")
    return email