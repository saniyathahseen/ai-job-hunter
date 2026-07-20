from fastapi import FastAPI
from api.v1.jobs import router as jobs_router
from api.v1.applications import router as applications_router
from scheduler.scheduler import scheduler

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
