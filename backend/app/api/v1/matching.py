from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.resume import MatchResult, CoverLetterRequest, CoverLetterResponse
from app.services.matching_service import MatchingService
from app.services.cover_letter_service import CoverLetterService

router = APIRouter(prefix="/matching", tags=["Matching"])


@router.get("/match/{job_id}/{resume_id}")
def get_match(
    job_id: int,
    resume_id: int,
    db: Session = Depends(get_db),
):
    """Return the skill match score between a job and a resume."""
    service = MatchingService(db)
    try:
        result = service.compute_match(job_id, resume_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/cover-letter")
def generate_cover_letter(
    request: CoverLetterRequest,
    db: Session = Depends(get_db),
):
    """Generate a personalised cover letter for a job using a resume."""
    service = CoverLetterService(db)
    try:
        letter = service.generate(request.job_id, request.resume_id, request.tone)
        return CoverLetterResponse(
            job_id=request.job_id,
            resume_id=request.resume_id,
            cover_letter=letter,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
