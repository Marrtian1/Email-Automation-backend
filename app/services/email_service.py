from sqlalchemy.orm import Session
from app.models.email import Email
from app.schemas.email import EmailCreate

class EmailService:
    @staticmethod
    def create_email(db: Session, email: EmailCreate, user_id: int):
        db_email = Email(**email.dict(), sender_id=user_id)
        db.add(db_email)
        db.commit()
        db.refresh(db_email)
        return db_email

    @staticmethod
    def get_user_emails(db: Session, user_id: int):
        return db.query(Email).filter(Email.sender_id == user_id).all()

email_service = EmailService()
