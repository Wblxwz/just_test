from fastapi import APIRouter
from crud import *
from db import SessionDep

router = APIRouter(prefix="/file",tags=["file"])

@router.post("/")
def add_file(file:File,session:SessionDep):
    file = create_file(file,session)
    return file

@router.get("/")
def get_all_file(session:SessionDep,offset:int = 0,limit:Annotated[int,Query(le=10)] = 10):
    files = select_all_file(session,offset,limit)
    return files

@router.get("/{file_id}")
def get_file_by_id(session:SessionDep,file_id:int):
    file = select_file_by_id(session,file_id)
    return file

@router.get("/folder/{id}")
def get_file_under_folder(session:SessionDep,id:int):
    files = select_file_under_folder(session,id)
    return files