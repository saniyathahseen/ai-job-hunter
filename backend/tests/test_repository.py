"""Tests for the JobRepository layer."""

import pytest
from app.repositories.job_repository import JobRepository
from app.models.job import Job

SAMPLE_JOB = {
    "company": "TestCorp",
    "title": "Python Developer",
    "location": "Remote",
    "remote": True,
    "salary": "$100k",
    "description": "Build APIs with Python",
    "apply_url": "https://testcorp.com/apply",
    "source": "TestSource",
    "posted_date": "2026-07-20",
}


class TestJobRepository:
    def test_save_and_retrieve_job(self, db_session):
        repo = JobRepository(db_session)
        saved = repo.save_jobs([SAMPLE_JOB])
        assert saved == 1

        jobs = repo.get_jobs()
        assert len(jobs) == 1
        assert jobs[0].company == "TestCorp"
        assert jobs[0].title == "Python Developer"

    def test_duplicate_detection(self, db_session):
        repo = JobRepository(db_session)
        repo.save_jobs([SAMPLE_JOB])
        saved = repo.save_jobs([SAMPLE_JOB])
        assert saved == 0  # duplicate should be skipped

    def test_get_job_by_id(self, db_session):
        repo = JobRepository(db_session)
        repo.save_jobs([SAMPLE_JOB])
        job = repo.get_job_by_id(1)
        assert job is not None
        assert job.id == 1

    def test_get_job_by_id_not_found(self, db_session):
        repo = JobRepository(db_session)
        assert repo.get_job_by_id(999) is None

    def test_pagination(self, db_session):
        repo = JobRepository(db_session)
        jobs_data = [
            {**SAMPLE_JOB, "apply_url": f"https://test.com/{i}"} for i in range(5)
        ]
        repo.save_jobs(jobs_data)

        page_1 = repo.get_jobs(skip=0, limit=2)
        assert len(page_1) == 2

        page_2 = repo.get_jobs(skip=2, limit=2)
        assert len(page_2) == 2

    def test_job_exists(self, db_session):
        repo = JobRepository(db_session)
        assert repo.job_exists(SAMPLE_JOB["apply_url"]) is False
        repo.save_jobs([SAMPLE_JOB])
        assert repo.job_exists(SAMPLE_JOB["apply_url"]) is True
