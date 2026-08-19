from fastapi import FastAPI

app = FastAPI(
    title="SupportDesk API",
    description="Customer Support Ticketing CRM API",
    version="1.0.0",
)


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