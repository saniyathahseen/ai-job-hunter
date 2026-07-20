import logging
from sqlalchemy.orm import Session
from app.repositories.job_repository import JobRepository
from app.scrapers.remote_ok import fetch_remote_ok, filter_python_jobs
from app.scrapers.remotive import fetch_remotive
from app.scrapers.wework import fetch_wework
from app.services.job_mapper import map_job

logger = logging.getLogger(__name__)


class JobService:
    """Coordinates the job-sync workflow: fetch → filter → map → persist."""

    def __init__(self, db: Session):
        self.repository = JobRepository(db)

    def sync_jobs(self) -> int:
        """Fetch jobs from all sources, filter for Python roles, and persist new ones."""
        logger.info("Starting job sync from all sources")

        remote_ok_jobs = fetch_remote_ok()
        logger.info("Fetched %d jobs from Remote OK", len(remote_ok_jobs))

        remotive_jobs = fetch_remotive()
        logger.info("Fetched %d jobs from Remotive", len(remotive_jobs))

        wework_jobs = fetch_wework()
        logger.info("Fetched %d jobs from We Work Remotely", len(wework_jobs))

        all_jobs = remote_ok_jobs + remotive_jobs + wework_jobs
        logger.info("Total raw jobs before filtering: %d", len(all_jobs))

        filtered = filter_python_jobs(all_jobs)
        logger.info("Jobs after Python filter: %d", len(filtered))

        mapped = [map_job(job) for job in filtered]

        saved = self.repository.save_jobs(mapped)
        logger.info("Sync complete: %d new jobs saved", saved)
        return saved
