from api.routes import file
from fastapi import FastAPI

from models import *
from db import create_db_and_tables

app = FastAPI()

app.include_router(file.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()