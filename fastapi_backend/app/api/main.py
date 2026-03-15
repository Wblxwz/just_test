from app.api.routes import file,script
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
app.include_router(script.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()