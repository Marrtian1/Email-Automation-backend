from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Optional

from app.models.email_log import EmailLog
from app.schemas.email_log import EmailLogCreate, EmailLogUpdate

class EmailLogService:
    @staticmethod
    def create_log(db: Session, log_in: EmailLogCreate) -> EmailLog:
        db_log = EmailLog(**log_in.dict())
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log

    @staticmethod
    def get_logs(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[EmailLog]:
        query = db.query(EmailLog)

        if status:
            query = query.filter(EmailLog.status == status)
        if start_date:
            query = query.filter(EmailLog.sent_at >= start_date)
        if end_date:
            query = query.filter(EmailLog.sent_at <= end_date)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_log_by_id(db: Session, log_id: int) -> Optional[EmailLog]:
        return db.query(EmailLog).filter(EmailLog.id == log_id).first()

    @staticmethod
    def update_log_status(db: Session, log_id: int, status: str) -> Optional[EmailLog]:
        log = db.query(EmailLog).filter(EmailLog.id == log_id).first()
        if log:
            log.status = status
            db.add(log)
            db.commit()
            db.refresh(log)
        return log

    @staticmethod
    def delete_log(db: Session, log_id: int) -> Optional[EmailLog]:
        log = db.query(EmailLog).filter(EmailLog.id == log_id).first()
        if log:
            db.delete(log)
            db.commit()
        return log

email_log_service = EmailLogService()