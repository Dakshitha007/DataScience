from fastapi import FastAPI
from sqlalchemy import text

from app.database.connection import engine

app = FastAPI(
    title="CrimeMind AI",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "Welcome to CrimeMind AI 🚔"}


@app.get("/database")
def database_status():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "Database Connected Successfully ✅"}