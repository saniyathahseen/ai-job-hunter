from sqlalchemy import Boolean
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Index
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    company: Mapped[str] = mapped_column(String(150))

    title: Mapped[str] = mapped_column(String(200))

    location: Mapped[str] = mapped_column(String(150))

    remote: Mapped[bool] = mapped_column(Boolean)

    salary: Mapped[str | None] = mapped_column(String(100))

    description: Mapped[str] = mapped_column(Text)

    apply_url: Mapped[str] = mapped_column(Text, unique=True)

    source: Mapped[str] = mapped_column(String(100))

    posted_date: Mapped[str] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    applications = relationship("Application", back_populates="job")

    __table_args__ = (Index("idx_jobs_created_at", "created_at"),)
