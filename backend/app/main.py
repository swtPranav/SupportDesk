import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, dashboard, notes, tickets, users

from app.models import Note, Ticket, User
from app.security import hash_password

load_dotenv()

Base.metadata.create_all(bind=engine)


def seed_admin_account():
    """Create a staff login only when deployment environment variables request it."""
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    if not email or not password:
        return

    from app.database import SessionLocal

    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == email).first():
            db.add(User(
                name=os.getenv("ADMIN_NAME", "SupportDesk Admin"),
                email=email,
                password_hash=hash_password(password),
                role="admin",
                is_active=True,
            ))
            db.commit()
    finally:
        db.close()


seed_admin_account()


app = FastAPI(
    title="SupportDesk API",
    description="Customer Support Ticketing CRM API",
    version="1.0.0",
)

allowed_origins = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
).split(",")


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(dashboard.router)
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
