from datetime import datetime
from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    job_id: int
    status: str
    notes: str | None = None


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    status: str
    notes: str | None = None
    applied_on: datetime | None = None

    model_config = {"from_attributes": True}