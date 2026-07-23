"""Generate personalised cover letters using OpenAI."""

import logging
import os
from sqlalchemy.orm import Session

from app.repositories.job_repository import JobRepository
from app.repositories.resume_repository import ResumeRepository
from app.services.matching_service import MatchingService

logger = logging.getLogger(__name__)


class CoverLetterService:
    """Generates a tailored cover letter by combining job + resume context."""

    def __init__(self, db: Session):
        self.job_repo = JobRepository(db)
        self.resume_repo = ResumeRepository(db)
        self.matching = MatchingService(db)

    def generate(self, job_id: int, resume_id: int, tone: str = "professional") -> str:
        """Produce a cover letter for the given job and resume.

        Uses the OpenAI API when a token is configured; otherwise falls
        back to a template-based letter built from the match data.
        """
        job = self.job_repo.get_job_by_id(job_id)
        if not job:
            raise ValueError(f"Job with id {job_id} not found")

        resume = self.resume_repo.get_resume_by_id(resume_id)
        if not resume:
            raise ValueError(f"Resume with id {resume_id} not found")

        match = self.matching.compute_match(job_id, resume_id)

        # Try OpenAI if a token is available
        api_key = os.getenv("OPENAI_API_KEY", "")
        if api_key:
            try:
                return self._generate_with_ai(job, resume, match, tone, api_key)
            except Exception:
                logger.exception(
                    "AI cover letter generation failed; using template fallback"
                )

        # Fallback: template-based letter
        return self._generate_template(job, resume, match, tone)

    def _generate_template(self, job, resume, match, tone: str = "professional") -> str:
        """Build a cover letter from a template using match data."""
        matched_str = (
            ", ".join(match.matched_skills)
            if match.matched_skills
            else "various relevant skills"
        )
        missing_str = (
            ", ".join(match.missing_skills) if match.missing_skills else "none"
        )

        letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job.title} position at {job.company}. With my background in {resume.skills}, I am confident that I would be a valuable addition to your team.

My experience aligns well with the requirements of this role. I bring expertise in {matched_str}, which directly matches the skills you are looking for.

"""

        if match.missing_skills:
            letter += f"""I am actively working to strengthen my knowledge in {missing_str} and am confident I can quickly ramp up in these areas to contribute effectively.

"""

        if resume.experience:
            letter += f"""In my previous roles, {resume.experience[:500]}

"""

        letter += f"""I am excited about the opportunity to bring my skills to {job.company} and would welcome the chance to discuss how I can contribute to your team.

Thank you for your time and consideration.

Best regards,
{resume.name}"""

        return letter

    def _generate_with_ai(self, job, resume, match, tone: str, api_key: str) -> str:
        """Generate a cover letter using the OpenAI API."""
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        matched_str = (
            ", ".join(match.matched_skills)
            if match.matched_skills
            else "various skills"
        )
        missing_str = (
            ", ".join(match.missing_skills) if match.missing_skills else "none"
        )

        prompt = f"""Write a {tone} cover letter for the following:

Job Title: {job.title}
Company: {job.company}
Job Description: {job.description[:1500]}

Candidate Name: {resume.name}
Candidate Skills: {resume.skills}
Candidate Experience: {resume.experience or 'Not provided'}
Candidate Education: {resume.education or 'Not provided'}

Skills Match: {matched_str}
Skills to Develop: {missing_str}

Write a concise, compelling cover letter (max 300 words) that highlights the candidate's relevant skills and experience."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional cover letter writer. Write in a {tone} tone.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=600,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()
