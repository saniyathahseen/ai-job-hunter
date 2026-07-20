from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.repositories.job_repository import JobRepository
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/")
def list_jobs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    """Return paginated job listings."""
    repo = JobRepository(db)
    return repo.get_jobs(skip=skip, limit=limit)


@router.post("/sync")
def sync_jobs(db: Session = Depends(get_db)):
    """Trigger a full sync from all job sources."""
    service = JobService(db)
    saved = service.sync_jobs()
    return {"saved": saved}
