from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.scheduled_email import ScheduledEmail
from app.schemas.scheduled_email import ScheduledEmailCreate
from app.services.email_engine import email_engine

class SchedulerService:
    @staticmethod
    def schedule_email(db: Session, email_in: ScheduledEmailCreate, user_id: int) -> ScheduledEmail:
        db_email = ScheduledEmail(**email_in.dict(), user_id=user_id, status="pending")
        db.add(db_email)
        db.commit()
        db.refresh(db_email)
        return db_email

    @staticmethod
    def get_scheduled_emails(db: Session, skip: int = 0, limit: int = 100):
        return db.query(ScheduledEmail).offset(skip).limit(limit).all()

    @staticmethod
    def get_scheduled_email(db: Session, email_id: int):
        return db.query(ScheduledEmail).filter(ScheduledEmail.id == email_id).first()

    @staticmethod
    def delete_scheduled_email(db: Session, email_id: int):
        email = db.query(ScheduledEmail).filter(ScheduledEmail.id == email_id).first()
        if email:
            db.delete(email)
            db.commit()
        return email

    @staticmethod
    def process_due_emails(db: Session):
        """Fetch and send all pending emails whose send_time has passed."""
        now = datetime.now(timezone.utc)
        due_emails = (
            db.query(ScheduledEmail)
            .filter(ScheduledEmail.status == "pending")
            .filter(ScheduledEmail.send_time <= now)
            .all()
        )
        results = []
        for email in due_emails:
            try:
                try:
                    email_engine.send_email(
                        recipient=email.recipient,
                        subject=email.subject,
                        body=email.body,
                        is_html=True
                    )
                    email_status = "sent"
                except Exception:
                    email_status = "failed"
                # Log email activity
                from app.services.email_log_service import email_log_service
                email_log_service.create_log(
                    db=db,
                    log_in={
                        "recipient": email.recipient,
                        "subject": email.subject,
                        "body_preview": email.body[:200] if email.body else None,
                        "status": email_status,
                        "sent_at": datetime.utcnow(),
                        "created_at": datetime.utcnow(),
                        "user_id": email.sender_id,
                    },
                )
                email.status = email_status
                results.append({"id": email.id, "status": email_status})
                db.add(email)
        db.commit()
        return results

scheduler_service = SchedulerService()