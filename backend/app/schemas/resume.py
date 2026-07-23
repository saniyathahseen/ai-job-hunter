from datetime import datetime
from pydantic import BaseModel


class ResumeCreate(BaseModel):
    name: str
    skills: str
    experience: str | None = None
    education: str | None = None


class ResumeUpdate(BaseModel):
    name: str | None = None
    skills: str | None = None
    experience: str | None = None
    education: str | None = None


class ResumeResponse(BaseModel):
    id: int
    name: str
    skills: str
    experience: str | None = None
    education: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class MatchResult(BaseModel):
    job_id: int
    job_title: str
    company: str
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    total_required_skills: int


class CoverLetterRequest(BaseModel):
    job_id: int
    resume_id: int
    tone: str = "professional"


class CoverLetterResponse(BaseModel):
    job_id: int
    resume_id: int
    cover_letter: str
