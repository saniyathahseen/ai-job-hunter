from sqlalchemy.orm import Session
from models.job import Job
from schemas.job import JobCreate
from sqlalchemy import select


def get_jobs(db, skip: int = 0, limit: int = 20):

    stmt = select(Job).order_by(Job.created_at.desc()).offset(skip).limit(limit)

    return db.scalars(stmt).all()


def create_job(db: Session, job: JobCreate):

    db_job = Job(**job.model_dump())

    db.add(db_job)

    db.commit()

    db.refresh(db_job)

    return db_job


# prevent duplicate jobs by checking if a job with the same apply_url already exists in the database
def job_exists(db, apply_url):

    stmt = select(Job).where(Job.apply_url == apply_url)

    return db.scalar(stmt)


def get_job_by_id(db, job_id: int):

    stmt = select(Job).where(Job.id == job_id)
    return db.scalar(stmt)


# Save jobs
def save_jobs(db, jobs):

    added = 0

    for job in jobs:

        if job_exists(db, job["apply_url"]):
            continue

        db.add(Job(**job))

        added += 1

    db.commit()
    return added
