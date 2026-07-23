import logging
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.resume import Resume

logger = logging.getLogger(__name__)


class ResumeRepository:
    """Handles database operations for Resume entities."""

    def __init__(self, db: Session):
        self.db = db

    def get_resumes(self, skip: int = 0, limit: int = 20) -> list[Resume]:
        stmt = (
            select(Resume).order_by(Resume.updated_at.desc()).offset(skip).limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def get_resume_by_id(self, resume_id: int) -> Resume | None:
        stmt = select(Resume).where(Resume.id == resume_id)
        return self.db.scalar(stmt)

    def create_resume(self, data: dict) -> Resume:
        resume = Resume(**data)
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def update_resume(self, resume_id: int, data: dict) -> Resume | None:
        resume = self.get_resume_by_id(resume_id)
        if not resume:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(resume, key, value)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def delete_resume(self, resume_id: int) -> bool:
        resume = self.get_resume_by_id(resume_id)
        if not resume:
            return False
        self.db.delete(resume)
        self.db.commit()
        return True
