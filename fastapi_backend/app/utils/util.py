from pathlib import Path
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
import time
import aiofiles
from app.crud import File
import yaml

async def save_file(upload_file:UploadFile):
    file_name = f"{int(time.time() * 1000)}_{upload_file.filename}"
    file_path = Path(__file__).parent.parent / "files" / f"{file_name}"
    async with aiofiles.open(file_path,"wb") as f:
        while data := await upload_file.read(1024 * 1024):
            await f.write(data)
    return file_name

async def save_files(upload_file:UploadFile):
    file_path = Path(__file__).parent.parent / "files" /  f"{upload_file.filename}"
    async with aiofiles.open(file_path,"wb") as f:
        while data := await upload_file.read(1024 * 1024):
            await f.write(data)

async def get_file(file:File):
    file_path = Path(__file__).parent.parent / "files" / f"{file.url}"
    async def get_stream_file():
        async with aiofiles.open(file_path,"rb") as f:
            while data := await f.read(1024 * 1024):
                yield data
    return StreamingResponse(get_stream_file(),headers={
        "Content-Disposition": f"attachment; filename={file.name}"
    })

def read_yaml() -> dict:
    utils_path = Path(__file__).parent
    yaml_path = utils_path / "variable.yml"
    with open(yaml_path,encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

data = read_yaml()