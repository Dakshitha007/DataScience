from fastapi import FastAPI
from sqlalchemy import text

from app.api.auth import router as auth_router
from app.api.case import router as case_router
from app.database.connection import engine
from app.database.init_db import init_db

app = FastAPI(
    title="CrimeMind AI",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_db()


# Register Routers
app.include_router(auth_router)
app.include_router(case_router)


@app.get("/")
def home():
    return {"message": "Welcome to CrimeMind AI 🚔"}


@app.get("/database")
def database_status():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"status": "Database Connected Successfully ✅"}