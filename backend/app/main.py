from fastapi import FastAPI
from sqlalchemy import text

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.officers import router as officers_router
from app.api.case import router as case_router
from app.api.investigation import router as investigation_router
from app.api.evidence import router as evidence_router

from app.database.connection import engine
from app.database.init_db import init_db


app = FastAPI(
    title="CrimeMind AI",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_db()


# ==========================
# Register Routers
# ==========================

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(officers_router)
app.include_router(case_router)
app.include_router(investigation_router)
app.include_router(evidence_router)


# ==========================
# Home Endpoint
# ==========================

@app.get("/")
def home():
    return {
        "message": "Welcome to CrimeMind AI 🚔"
    }


# ==========================
# Database Health Check
# ==========================

@app.get("/database")
def database_status():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "Database Connected Successfully ✅"
    }