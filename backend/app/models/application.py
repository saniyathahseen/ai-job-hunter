from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class Application(Base):

    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id")
    )

    status: Mapped[str] = mapped_column(String(50))

    notes: Mapped[str | None]

    
    applied_on: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),)