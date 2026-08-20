from fastapi import FastAPI

from app.database import Base, engine
from app.routers import tickets

from app.models import Note, Ticket

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SupportDesk API",
    description="Customer Support Ticketing CRM API",
    version="1.0.0",
)

app.include_router(tickets.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to SupportDesk API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }