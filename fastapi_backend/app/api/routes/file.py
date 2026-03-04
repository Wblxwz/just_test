from fastapi import APIRouter
from crud import *
from db import SessionDep

router = APIRouter(prefix="/file",tags=["file"])

@router.post("/")
def add_file(file:File,session:SessionDep):
    file = create_file(file,session)
    return file