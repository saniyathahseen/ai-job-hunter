from apscheduler.schedulers.background import BackgroundScheduler
from database.session import SessionLocal
from services.job_service import JobService

scheduler = BackgroundScheduler()


def scheduled_sync():

    db = SessionLocal()

    try:

        JobService.sync_jobs(db)

    finally:

        db.close()

scheduler.add_job(
    scheduled_sync,

    trigger="cron",

    hour=8,

    minute=0,
)
# Look for where you call scheduler.start()
if not scheduler.running:
    scheduler.start()
