from scrapers.remote_ok import (
    fetch_remote_ok,
    filter_python_jobs,
)
from services.job_mapper import map_job
from crud.job import save_jobs
from scrapers.remotive import fetch_remotive
from scrapers.wework import fetch_wework


class JobService:

    @staticmethod
    def sync_jobs(db):
        remote_ok_jobs = fetch_remote_ok()

        remotive_jobs = fetch_remotive()

        wework_jobs = fetch_wework()

        jobs = remote_ok_jobs + remotive_jobs + wework_jobs

        jobs = filter_python_jobs(jobs)

        jobs = [map_job(job) for job in jobs]

        return save_jobs(db, jobs)
