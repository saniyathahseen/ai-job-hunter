import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.database.session import SessionLocal
from app.services.job_service import JobService

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def scheduled_sync():
    """Run by the scheduler — fetches and saves new Python jobs."""
    logger.info("Scheduler triggered: starting job sync")
    db = SessionLocal()
    try:
        service = JobService(db)
        saved = service.sync_jobs()
        logger.info("Scheduler sync complete: %d new jobs saved", saved)
    except Exception:
        logger.exception("Scheduler sync failed")
    finally:
        db.close()


scheduler.add_job(scheduled_sync, trigger="cron", hour=8, minute=0)
