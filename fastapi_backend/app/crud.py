from app.models import *

from typing import Annotated,List
from app.db import SessionDep
from fastapi import Query
from sqlmodel import select
from pathlib import Path
import shutil

#file
#====================================================
def create_file(file:File,session:SessionDep)->File:
    session.add(file)
    session.commit()
    session.refresh(file)
    return file

def create_file_array(files:List[File],session:SessionDep)->List[File]:
    for file in files:
        session.add(file)
    session.commit()
    for file in files:
        session.refresh(file)
    return files

def select_all_file(session:SessionDep,offset:int = 0,limit:Annotated[int, Query(le=10)] = 10):
    files = session.exec(select(File).offset(offset).limit(limit)).all()
    return files

def select_file_by_id(session:SessionDep,id:int):
    file = session.get(File,id)
    return file

def select_file_under_folder(session:SessionDep,id:int):
    files = session.exec(select(File).where(File.parent_id == id)).all()
    return files

def delete_file_folder(session:SessionDep,id:int):
    file = select_file_by_id(session,id)
    files_path = Path(__file__).parent / "files"
    if file.leaf == False:
        files = select_file_under_folder(session,id)
        for tmp_file in files:
            file_path = files_path / tmp_file.url
            file_path.unlink()
            session.delete(tmp_file)
    else:
        file_path = files_path / file.url
        file_path.unlink()
    session.delete(file)
    session.commit()
    return {"ok":True,"message":"delete success"}

#process
#====================================================
def get_process(session:SessionDep,offset:int = 0,limit:Annotated[int, Query(le=10)] = 10):
    processes = session.exec(select(Process).offset(offset).limit(limit)).all()
    return processes

def get_process_by_id(session:SessionDep,id:int):
    return session.get(Process,id)

def insert_process(session:SessionDep,process:Process):
    session.add(process)
    session.commit()
    session.refresh(process)
    return process

def update_process(session:SessionDep,id:int,process_update:ProcessUpdate):
    process = get_process_by_id(session,id)
    process_data = process_update.model_dump(exclude_unset=True)
    process.sqlmodel_update(process_data)
    session.add(process)
    session.commit()
    session.refresh(process)
    return {"ok":True,"message":"update success"}

def delete_process(session:SessionDep,id:int):
    process = get_process_by_id(session,id)
    folder = Path(process.report_url)
    if folder.is_dir():
        shutil.rmtree(folder)
    zip_path = Path(process.report_url + ".zip")
    zip_path.unlink()
    session.delete(process)
    session.commit()
    return {"ok":True,"message":"delete success"}