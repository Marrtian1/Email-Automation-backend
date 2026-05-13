"""
Background scheduler that periodically checks for due scheduled emails
and sends them. Runs as a separate thread on application startup.
"""
import asyncio
from datetime import datetime, timezone
from typing import Callable

from app.core.db import get_db
from app.services.scheduler_service import scheduler_service


async def _run_scheduler_once():
    """Single pass: query and send all due emails."""
    try:
        db = next(get_db())
        scheduler_service.process_due_emails(db)
    except Exception:
        pass


async def _scheduler_loop(stop_event: asyncio.Event):
    """Poll every 60 seconds for due emails."""
    while not stop_event.is_set():
        await _run_scheduler_once()
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=60)
        except asyncio.TimeoutError:
            continue


def start_scheduler(app):
    """Attach the background scheduler to the FastAPI lifespan."""
    stop_event = asyncio.Event()

    async def startup():
        app.state._scheduler_stop = stop_event
        app.state._scheduler_task = asyncio.create_task(_scheduler_loop(stop_event))

    async def shutdown():
        stop_event.set()
        task = getattr(app.state, "_scheduler_task", None)
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    return startup, shutdown