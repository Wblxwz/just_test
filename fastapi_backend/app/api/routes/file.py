from fastapi import APIRouter,UploadFile,File
import os
from app.utils.util import *
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

@router.post("/upload")
async def upload_file(file:UploadFile):
    file_name = await save_file(file)
    return {
        "file":file_name
    }

@router.post("/uploadFiles")
async def upload_files(files:List[UploadFile]):
    #不允许文件夹嵌套，在前端应做限制，因为是扁平化处理文件，不创建多个文件夹节点
    timestamp = int(time.time() * 1000)
    files_name = []
    file_name = files[0].filename
    file_path = Path(file_name)
    folder_name = f"{timestamp}_{file_path.parent}"
    os.makedirs(folder_name,exist_ok=True)
    for file in files:
        file.filename = folder_name + file.filename.split("\\")[1]
        file_name = await save_files(file)
        files_name.append(file_name)
    return {
        "files":files_name
    }

@router.get("/download/{id}")
async def download_file(session:SessionDep,id:int):
    file = select_file_by_id(session,id)
    return await get_file(file)