from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List

from app.api import deps
from app.core.db import get_db
from app.models.user import User
from app.schemas.email_log import EmailLog, EmailLogCreate
from app.services.email_log_service import email_log_service

router = APIRouter()

@router.get("/", response_model=List[EmailLog])
def read_logs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filter by status (sent, failed, pending, rejected)"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date (ISO format)"),
    current_user: User = Depends(deps.get_current_user)
):
    return email_log_service.get_logs(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/{log_id}", response_model=EmailLog)
def read_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    log = email_log_service.get_log_by_id(db=db, log_id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Email log not found")
    return log

@router.get("/status/{log_id}", response_model=dict)
def get_email_status(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    log = email_log_service.get_log_by_id(db=db, log_id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Email log not found")
    
    return {
        "id": log.id,
        "recipient": log.recipient,
        "subject": log.subject,
        "status": log.status,
        "sent_at": log.sent_at,
        "created_at": log.created_at
    }