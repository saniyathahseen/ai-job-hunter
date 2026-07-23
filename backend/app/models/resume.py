from sqlalchemy import DateTime, Integer, String, Text
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(200))

    skills: Mapped[str] = mapped_column(Text)
    """Comma-separated list of skills, e.g. 'Python, FastAPI, PostgreSQL'"""

    experience: Mapped[str | None] = mapped_column(Text)
    """Free-text summary of professional experience."""

    education: Mapped[str | None] = mapped_column(Text)
    """Free-text summary of education."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
