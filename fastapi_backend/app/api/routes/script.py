from app.crud import *
from fastapi import APIRouter

router = APIRouter(prefix="/process",tags=["process"])

@router.get("/")
def get_process_api(session:SessionDep,offset:int = 0,limit:int = 10):
    return get_process(session,offset,limit)

@router.get("/{id}")
def get_process_by_id_api(session:SessionDep,id:int):
    return get_process_by_id(session,id)

@router.post("/")
def insert_process_api(session:SessionDep,process:Process):
    return insert_process(session,process)