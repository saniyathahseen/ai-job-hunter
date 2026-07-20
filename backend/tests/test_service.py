"""Tests for the JobService layer — uses mocked scrapers to avoid network calls."""

from unittest.mock import patch
from app.services.job_service import JobService

SAMPLE_RAW_JOB = {
    "company": "MockCorp",
    "position": "Python Backend",
    "location": "Remote",
    "remote": True,
    "salary_min": "120k",
    "description": "We need a Python dev",
    "url": "https://mockcorp.com/job",
    "source": "MockSource",
    "date": "2026-07-20",
}


class TestJobService:
    @patch("app.services.job_service.fetch_remote_ok", return_value=[SAMPLE_RAW_JOB])
    @patch("app.services.job_service.fetch_remotive", return_value=[])
    @patch("app.services.job_service.fetch_wework", return_value=[])
    def test_sync_jobs_returns_count(
        self, mock_wework, mock_remotive, mock_remoteok, db_session
    ):
        service = JobService(db_session)
        saved = service.sync_jobs()
        assert saved == 1

    @patch("app.services.job_service.fetch_remote_ok", return_value=[])
    @patch("app.services.job_service.fetch_remotive", return_value=[])
    @patch("app.services.job_service.fetch_wework", return_value=[])
    def test_sync_jobs_no_jobs(
        self, mock_wework, mock_remotive, mock_remoteok, db_session
    ):
        service = JobService(db_session)
        saved = service.sync_jobs()
        assert saved == 0
