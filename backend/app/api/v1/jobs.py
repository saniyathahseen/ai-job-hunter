from fastapi import APIRouter
from fastapi import Depends
from services.job_mapper import map_remote_ok
from database.dependencies import get_db
from sqlalchemy.orm import Session
from crud.job import save_jobs,get_job
from services.job_service import JobService
router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)




@router.get("/")
def get_jobs(db: Session = Depends(get_db)):

    
    return get_job(db)
@router.post("/sync")
def sync_jobs(db: Session = Depends(get_db)):

    
    total = JobService.sync_jobs(db)
    return {
        "saved": total
    }

@router.post("/sync")
def sync_jobs(
    db: Session = Depends(get_db),
):

    

    return {
        "saved": total
    }