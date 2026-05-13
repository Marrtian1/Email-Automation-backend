from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings
from app.schemas.email import EmailCreate, EmailBulkSend
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAILS_FROM_EMAIL,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_FROM_NAME=settings.EMAILS_FROM_NAME,
    MAIL_STARTTLS=settings.SMTP_TLS,
    MAIL_SSL_TLS=settings.SMTP_SSL,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

class EmailEngine:
    def __init__(self):
        self.fastmail = FastMail(conf)

    async def send_email(self, recipient: str, subject: str, body: str, is_html: bool = True):
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            body=body,
            subtype=MessageType.html if is_html else MessageType.plain
        )
        await self.fastmail.send_message(message)
        return True

    async def send_bulk_email(self, recipients: List[str], subject: str, body: str, is_html: bool = True):
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=MessageType.html if is_html else MessageType.plain
        )
        await self.fastmail.send_message(message)
        return True

email_engine = EmailEngine()
