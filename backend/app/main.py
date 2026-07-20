import sys
from pathlib import Path

# Ensure the backend/ directory is on sys.path so that imports like
# "from app.api.v1.jobs import ..." work regardless of how main.py is invoked.
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from app.api.v1.jobs import router as jobs_router
from app.api.v1.applications import router as applications_router
from app.scheduler.scheduler import scheduler
from app.core.logging import setup_logging

# Configure application-wide logging first
setup_logging()

app = FastAPI(title="AI Job Hunter", version="1.0.0")
app.include_router(jobs_router)
app.include_router(applications_router)


@app.get("/")
def root():
    return {"message": "AI Job Hunter API is running"}


if __name__ == "__main__":
    import uvicorn

    # The scheduler will only start if you run this file directly,
    # not when Alembic imports it!
    scheduler.start()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
