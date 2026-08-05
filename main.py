from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.models.db import engine
from app.scheduler.gmail_scheduler import GmailScheduler
from app.api.jobs import router as job_router

def create_db_and_tables():

    SQLModel.metadata.create_all(
        engine
    )

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup

    create_db_and_tables()


    scheduler = GmailScheduler()


    scheduler.start()


    app.state.scheduler = scheduler


    print(
        "Scheduler Started..."
    )


    yield


    # Shutdown

    scheduler.shutdown()


    print(
        "Scheduler Stopped..."
    )



app = FastAPI(
    lifespan=lifespan
)

app.include_router(job_router)

@app.get("/ai-recruiter")
async def ai_recruiter():

    return {
        "message":
        "Welcome to AI Recruiter API"
    }