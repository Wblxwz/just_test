from app.api.routes import file,process
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.models import *
from app.db import create_db_and_tables

origins = [
    "https://",
    "https://:8080",
    "http://localhost:5173",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file.router)
app.include_router(process.router)

app.mount("/reports",StaticFiles(directory=Path(__file__).parents[1] / "reports",html=True),name="report")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()