import logging
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.job import Job
from app.schemas.job import JobCreate

logger = logging.getLogger(__name__)


class JobRepository:
    """Handles all database operations for Job entities."""

    def __init__(self, db: Session):
        self.db = db

    def get_jobs(self, skip: int = 0, limit: int = 20) -> list[Job]:
        """Return paginated jobs ordered by creation date (newest first)."""
        stmt = select(Job).order_by(Job.created_at.desc()).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get_job_by_id(self, job_id: int) -> Job | None:
        """Fetch a single job by its primary key."""
        stmt = select(Job).where(Job.id == job_id)
        return self.db.scalar(stmt)

    def job_exists(self, apply_url: str) -> bool:
        """Check whether a job with the given apply_url already exists."""
        stmt = select(Job).where(Job.apply_url == apply_url)
        return self.db.scalar(stmt) is not None

    def create_job(self, job_data: dict) -> Job:
        """Create and persist a new Job from a dictionary of field values."""
        db_job = Job(**job_data)
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        return db_job

    def save_jobs(self, jobs: list[dict]) -> int:
        """Bulk-save a list of job dicts, skipping duplicates. Returns count of new records."""
        added = 0
        for job in jobs:
            if self.job_exists(job["apply_url"]):
                logger.debug("Duplicate skipped: %s", job["apply_url"])
                continue
            self.db.add(Job(**job))
            added += 1
        self.db.commit()
        logger.info("Saved %d new jobs to database", added)
        return added
