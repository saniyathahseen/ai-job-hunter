from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

# Import all models so Alembic can discover them
# from models.job import Job
# from models.application import Application