"""Match a resume against a job description to produce a match score."""

import logging
from sqlalchemy.orm import Session

from app.repositories.job_repository import JobRepository
from app.repositories.resume_repository import ResumeRepository
from app.services.skill_extractor import extract_skills
from app.schemas.resume import MatchResult

logger = logging.getLogger(__name__)


class MatchingService:
    """Compares resume skills against job-required skills and computes a score."""

    def __init__(self, db: Session):
        self.job_repo = JobRepository(db)
        self.resume_repo = ResumeRepository(db)

    def compute_match(self, job_id: int, resume_id: int) -> MatchResult:
        """Compute the match score between a resume and a job.

        Steps:
          1. Extract skills from the job description.
          2. Parse the resume's stored skills.
          3. Compare → matched / missing.
          4. Score = matched / total_required (0.0 – 1.0).
        """
        job = self.job_repo.get_job_by_id(job_id)
        if not job:
            raise ValueError(f"Job with id {job_id} not found")

        resume = self.resume_repo.get_resume_by_id(resume_id)
        if not resume:
            raise ValueError(f"Resume with id {resume_id} not found")

        # Skills required by the job (from description + title)
        job_text = f"{job.title} {job.description}"
        required_skills = extract_skills(job_text)

        # Skills the candidate has
        candidate_skills = {
            s.strip().lower() for s in resume.skills.split(",") if s.strip()
        }

        if not required_skills:
            # No tech skills detected in the job posting → score is N/A
            return MatchResult(
                job_id=job.id,
                job_title=job.title,
                company=job.company,
                match_score=0.0,
                matched_skills=[],
                missing_skills=[],
                total_required_skills=0,
            )

        matched: list[str] = []
        missing: list[str] = []

        for skill in required_skills:
            if skill.lower() in candidate_skills:
                matched.append(skill)
            else:
                missing.append(skill)

        score = round(len(matched) / len(required_skills), 2)

        logger.info(
            "Match: job=%d resume=%d score=%.2f matched=%d missing=%d",
            job_id,
            resume_id,
            score,
            len(matched),
            len(missing),
        )

        return MatchResult(
            job_id=job.id,
            job_title=job.title,
            company=job.company,
            match_score=score,
            matched_skills=matched,
            missing_skills=missing,
            total_required_skills=len(required_skills),
        )
