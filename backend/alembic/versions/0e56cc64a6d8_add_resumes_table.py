"""add resumes table + unique apply_url

Revision ID: 0e56cc64a6d8
Revises: 2f8f37cb38e9
Create Date: 2026-07-23 19:44:17.002026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0e56cc64a6d8"
down_revision: Union[str, Sequence[str], None] = "2f8f37cb38e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create the resumes table
    op.create_table(
        "resumes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("skills", sa.Text(), nullable=False),
        sa.Column("experience", sa.Text(), nullable=True),
        sa.Column("education", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # 2. Add index on created_at for faster sorting
    op.create_index("idx_jobs_created_at", "jobs", ["created_at"], unique=False)

    # 3. Remove duplicate apply_url rows before adding a unique constraint.
    #    Keep only the most recent row for each duplicate apply_url.
    op.execute(
        """
        DELETE FROM jobs
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM jobs
            GROUP BY apply_url
        )
        """
    )
    op.create_unique_constraint(None, "jobs", ["apply_url"])


def downgrade() -> None:
    op.drop_constraint(None, "jobs", type_="unique")
    op.drop_index("idx_jobs_created_at", table_name="jobs")
    op.drop_table("resumes")