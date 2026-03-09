from fastapi import APIRouter
from app.crud import *
from app.db import SessionDep

router = APIRouter(prefix="/file",tags=["file"])

@router.post("/")
def add_file(file:File,session:SessionDep):
    file = create_file(file,session)
    if file:
        result = {
            "ok":True,
            "file":file
        }
    else:
        result = {
            "ok":False
        }
    return result

@router.get("/")
def get_all_file(session:SessionDep,offset:int = 0,limit:Annotated[int,Query(le=1000)] = 1000):
    files = select_all_file(session,offset,limit)
    return files

@router.get("/{file_id}")
def get_file_by_id(session:SessionDep,file_id:int):
    file = select_file_by_id(session,file_id)
    return file

@router.post("/folder")
def add_files(files:List[File],session:SessionDep):
    files = create_file_array(files,session)
    if files:
        result = {
            "ok":True,
            "files":files
        }
    else:
        result = {
            "ok":False
        }
    return result

@router.get("/folder/{id}")
def get_file_under_folder(session:SessionDep,id:int):
    files = select_file_under_folder(session,id)
    return files

@router.delete("/folder/{id}")
def delete_file_under_folder(session:SessionDep,id:int):
    message = delete_file_folder(session,id)
    return message