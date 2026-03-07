from api.routes import file
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import *
from db import create_db_and_tables

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

@app.on_event("startup")
def on_startup():
    create_db_and_tables()