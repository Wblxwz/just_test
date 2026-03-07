from models import *

from typing import Annotated
from db import SessionDep
from fastapi import Query
from sqlmodel import select

#file
#====================================================
def create_file(file:File,session:SessionDep)->File:
    session.add(file)
    session.commit()
    session.refresh(file)
    return file

def select_all_file(session:SessionDep,offset:int = 0,limit:Annotated[int, Query(le=10)] = 10):
    files = session.exec(select(File).offset(offset).limit(limit)).all()
    return files

def select_file_by_id(session:SessionDep,id:int):
    file = session.get(File,id)
    return file

def select_file_under_folder(session:SessionDep,id:int):
    files = session.exec(select(File).where(File.parent_id == id)).all()
    return files