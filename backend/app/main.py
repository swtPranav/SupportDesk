from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, notes, tickets, users

from app.models import Note, Ticket

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SupportDesk API",
    description="Customer Support Ticketing CRM API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(notes.router)
app.include_router(users.router)


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