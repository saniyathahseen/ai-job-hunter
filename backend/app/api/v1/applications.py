from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.repositories.job_repository import JobRepository
from app.schemas.application import ApplicationCreate, ApplicationResponse

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.get("/")
def list_applications(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    """List all applications (placeholder — full CRUD via repository)."""
    return []


@router.get("/{application_id}")
def get_application_endpoint(
    application_id: int,
    db: Session = Depends(get_db),
):
    """Get a single application (placeholder)."""
    raise HTTPException(status_code=404, detail="Application not found")


@router.post("/", status_code=201)
def create_application_endpoint(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
):
    """Create an application (placeholder)."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.patch("/{application_id}/status")
def update_application_status_endpoint(
    application_id: int,
    status: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    """Update application status (placeholder)."""
    raise HTTPException(status_code=501, detail="Not implemented")
