from sqlalchemy.orm import Session
from models.application import Application
from schemas.application import ApplicationCreate
from sqlalchemy import select


def get_applications(db: Session, skip: int = 0, limit: int = 20):
    stmt = (
        select(Application)
        .order_by(Application.applied_on.desc())
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()


def get_application(db: Session, application_id: int):
    stmt = select(Application).where(Application.id == application_id)
    return db.scalar(stmt)


def create_application(db: Session, application: ApplicationCreate):
    db_application = Application(**application.model_dump())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


def update_application_status(db: Session, application_id: int, status: str):
    stmt = select(Application).where(Application.id == application_id)
    db_application = db.scalar(stmt)
    if db_application:
        db_application.status = status
        db.commit()
        db.refresh(db_application)
    return db_application
