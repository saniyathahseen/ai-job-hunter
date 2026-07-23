from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.resume_repository import ResumeRepository
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeResponse

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.get("/")
def list_resumes(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    repo = ResumeRepository(db)
    return repo.get_resumes(skip=skip, limit=limit)


@router.get("/{resume_id}")
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    repo = ResumeRepository(db)
    resume = repo.get_resume_by_id(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.post("/", status_code=201)
def create_resume(data: ResumeCreate, db: Session = Depends(get_db)):
    repo = ResumeRepository(db)
    return repo.create_resume(data.model_dump())


@router.put("/{resume_id}")
def update_resume(resume_id: int, data: ResumeUpdate, db: Session = Depends(get_db)):
    repo = ResumeRepository(db)
    resume = repo.update_resume(resume_id, data.model_dump(exclude_unset=True))
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.delete("/{resume_id}", status_code=204)
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    repo = ResumeRepository(db)
    deleted = repo.delete_resume(resume_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Resume not found")
