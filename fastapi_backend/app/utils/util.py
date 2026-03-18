from pathlib import Path
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
import time
import aiofiles
from app.models import File,Process
import yaml
import zipfile
import urllib.parse

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

async def get_stream_file(path:Path):
        async with aiofiles.open(path,"rb") as f:
            while data := await f.read(1024 * 1024):
                yield data

async def get_file(file:File = None,url:str = ""):
    if url != "":
        folder_path = Path(url)
        zip_path = Path(url + ".zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 遍历文件夹下所有文件/子文件夹
            for file_path in folder_path.rglob('*'):
                # 只处理文件（跳过空文件夹）
                if file_path.is_file():
                    # 计算文件在 zip 中的相对路径（关键：保持文件夹结构）
                    arcname = file_path.relative_to(folder_path.parent)
                    # 将文件写入 zip
                    zipf.write(file_path, arcname=arcname)
        return StreamingResponse(get_stream_file(zip_path),headers={
        "Content-Disposition": f"attachment; filename={urllib.parse.quote(zip_path.name)}"
        }) 
    file_path = Path(__file__).parent.parent / "files" / f"{file.url}"
    return StreamingResponse(get_stream_file(file_path),headers={
        "Content-Disposition": f"attachment; filename={file.name}"
    })

def read_yaml() -> dict:
    utils_path = Path(__file__).parent
    yaml_path = utils_path / "variable.yml"
    with open(yaml_path,encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

data = read_yaml()