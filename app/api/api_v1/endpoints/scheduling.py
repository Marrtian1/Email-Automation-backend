from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.core.db import get_db
from app.schemas.scheduled_email import ScheduledEmail, ScheduledEmailCreate
from app.models.scheduled_email import ScheduledEmail as ScheduledEmailModel
from app.services.template_service import template_service
from app.models.user import User

router = APIRouter()

@router.post("/schedule-email", response_model=ScheduledEmail)
async def schedule_email(
    email_in: ScheduledEmailCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    body = email_in.body
    subject = email_in.subject

    if email_in.template_id:
        template = template_service.get_template(db, email_in.template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        placeholders = email_in.placeholders or {}
        body = template_service.render_template(template.body, placeholders)
        subject = template.subject

    db_scheduled = ScheduledEmailModel(
        recipient=email_in.recipient,
        subject=subject,
        body=body,
        send_time=email_in.send_time,
        user_id=current_user.id
    )
    db.add(db_scheduled)
    db.commit()
    db.refresh(db_scheduled)
    return db_scheduled

@router.get("/scheduled", response_model=list[ScheduledEmail])
async def list_scheduled_emails(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return db.query(ScheduledEmailModel).filter(ScheduledEmailModel.user_id == current_user.id).all()
