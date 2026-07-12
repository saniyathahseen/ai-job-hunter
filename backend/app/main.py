from fastapi import FastAPI

app = FastAPI(
    title="AI Job Hunter",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "AI Job Hunter API is running"
    }