from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.scheduler import start_scheduler

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to the Email Automation API"}

# Initialize scheduler on startup
startup_event, shutdown_event = start_scheduler(app)

@app.on_event("startup")
async def on_startup():
    # The scheduler is started automatically by the returned task
    pass

@app.on_event("shutdown")
async def on_shutdown():
    # Gracefully stop the scheduler task
    shutdown_event.set()