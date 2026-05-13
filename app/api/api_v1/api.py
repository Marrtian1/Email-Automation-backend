from fastapi import APIRouter
from app.api.api_v1.endpoints import emails, users, auth, templates, scheduled_emails, rules, email_logs

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(emails.router, prefix="/emails", tags=["emails"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(scheduled_emails.router, prefix="/scheduled-emails", tags=["scheduled-emails"])
api_router.include_router(rules.router, prefix="/rules", tags=["rules"])
api_router.include_router(email_logs.router, prefix="/email-logs", tags=["email-logs"])
