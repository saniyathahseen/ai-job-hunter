from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from database.dependencies import get_db
from sqlalchemy.orm import Session
from crud.job import get_jobs
from services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/")
def list_jobs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return get_jobs(db, skip=skip, limit=limit)


@router.post("/sync")
def sync_jobs(db: Session = Depends(get_db)):

    total = JobService.sync_jobs(db)
    return {"saved": total}
