from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.core.db import get_db
from app.models.user import User
from app.schemas.email import EmailCreate, EmailBulkSend
from app.services.email_engine import email_engine
from app.services.template_service import template_service
from app.models.email import Email

router = APIRouter()

@router.post("/send-email")
async def send_single_email(
    email_in: EmailCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    body = email_in.body
    subject = email_in.subject

    # If template is provided, use it
    if email_in.template_id:
        template = template_service.get_template(db, email_in.template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        placeholders = email_in.placeholders or {}
        body = template_service.render_template(template.body, placeholders)
        subject = template.subject # Optionally override subject from template

    try:
        try:
            await email_engine.send_email(
                recipient=email_in.recipient,
                subject=subject,
                body=body,
                is_html=email_in.is_html
            )
            email_status = "sent"
        except Exception as e:
            email_status = "failed"
            # Log failure and re-raise after logging
            from app.services.email_log_service import email_log_service
            email_log_service.create_log(
                db=db,
                log_in={
                    "recipient": email_in.recipient,
                    "subject": subject,
                    "body_preview": body[:200] if body else None,
                    "status": email_status,
                    "sent_at": datetime.utcnow(),
                    "created_at": datetime.utcnow(),
                    "user_id": current_user.id,
                },
            )
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
        
        # Log success
        from app.services.email_log_service import email_log_service
        email_log_service.create_log(
            db=db,
            log_in={
                "recipient": email_in.recipient,
                "subject": subject,
                "body_preview": body[:200] if body else None,
                "status": email_status,
                "sent_at": datetime.utcnow(),
                "created_at": datetime.utcnow(),
                "user_id": current_user.id,
            },
        )
        
        # Also log to Email table for historical record
        db_email = Email(
            subject=subject,
            body=body,
            recipient=email_in.recipient,
            sender_id=current_user.id
        )
        db.add(db_email)
        db.commit()
        
        return {"status": "success", "message": f"Email sent to {email_in.recipient}"}

@router.post("/send-bulk")
async def send_bulk_emails(
    bulk_in: EmailBulkSend,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    body = bulk_in.body
    subject = bulk_in.subject

    if bulk_in.template_id:
        template = template_service.get_template(db, bulk_in.template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        placeholders = bulk_in.placeholders or {}
        body = template_service.render_template(template.body, placeholders)
        subject = template.subject

    try:
        try:
            await email_engine.send_bulk_email(
                recipients=bulk_in.recipients,
                subject=subject,
                body=body,
                is_html=bulk_in.is_html
            )
            email_status = "sent"
        except Exception as e:
            email_status = "failed"
            # Log failures and re-raise after logging
            from app.services.email_log_service import email_log_service
            for recipient in bulk_in.recipients:
                email_log_service.create_log(
                    db=db,
                    log_in={
                        "recipient": recipient,
                        "subject": subject,
                        "body_preview": body[:200] if body else None,
                        "status": email_status,
                        "sent_at": datetime.utcnow(),
                        "created_at": datetime.utcnow(),
                        "user_id": current_user.id,
                    },
                )
            raise HTTPException(status_code=500, detail=f"Failed to send bulk emails: {str(e)}")
        
        # Log each email individually
        from app.services.email_log_service import email_log_service
        for recipient in bulk_in.recipients:
            email_log_service.create_log(
                db=db,
                log_in={
                    "recipient": recipient,
                    "subject": subject,
                    "body_preview": body[:200] if body else None,
                    "status": email_status,
                    "sent_at": datetime.utcnow(),
                    "created_at": datetime.utcnow(),
                    "user_id": current_user.id,
                },
            )
        
        # Also log to Email table for historical record
        for recipient in bulk_in.recipients:
            db_email = Email(
                subject=subject,
                body=body,
                recipient=recipient,
                sender_id=current_user.id
            )
            db.add(db_email)
        db.commit()

        return {"status": "success", "message": f"Bulk emails sent to {len(bulk_in.recipients)} recipients"}
