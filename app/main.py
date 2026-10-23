from fastapi import FastAPI

from app.routers import reports


app = FastAPI(
    title="Background Tasks API",
    version="1.0.0"
)


app.include_router(
    reports.router,
    prefix="/reports",
    tags=["Reports"]
)


@app.get("/")
def root():
    return {
        "message": "Background Tasks API is running"
    }