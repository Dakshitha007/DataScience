from fastapi import FastAPI
from sqlalchemy import text

from app.database.connection import engine
from app.database.init_db import init_db
from app.api.auth import router as auth_router

app = FastAPI(
    title="CrimeMind AI",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Welcome to CrimeMind AI 🚔"}


@app.get("/database")
def database_status():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "Database Connected Successfully ✅"}