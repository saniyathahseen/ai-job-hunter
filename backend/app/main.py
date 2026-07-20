from fastapi import FastAPI
from api.v1.jobs import router
from scheduler.scheduler import scheduler

app = FastAPI(
    title="AI Job Hunter",
    version="1.0.0"
)
app.include_router(router)
@app.get("/")
def root():
    return {
        "message": "AI Job Hunter API is running"
    }


if __name__ == "__main__":
    import uvicorn
    # The scheduler will only start if you run this file directly,
    # not when Alembic imports it!
    if not scheduler.running:
        scheduler.start() 
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
