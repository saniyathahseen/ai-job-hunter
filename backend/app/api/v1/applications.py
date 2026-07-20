from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.dependencies import get_db
from crud.application import (
    get_applications,
    get_application,
    create_application,
    update_application_status,
)
from schemas.application import ApplicationCreate, ApplicationResponse

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
    return get_applications(db, skip=skip, limit=limit)


@router.get("/{application_id}")
def get_application_endpoint(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.post("/", status_code=201)
def create_application_endpoint(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
):
    return create_application(db, application)


@router.patch("/{application_id}/status")
def update_application_status_endpoint(
    application_id: int,
    status: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    application = update_application_status(db, application_id, status)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application
