from app.crud import *
from fastapi import APIRouter
import os
from typing import Callable
import subprocess
import threading
from pathlib import Path
import time
from app.utils.util import *
from datetime import timedelta

router = APIRouter(prefix="/process",tags=["process"])

def exec_worker(cmd:str,callback:Callable,env:str = "",report_path:Path = "",id:int = 0,session:SessionDep = None):
    out_file = report_path / "process_out.log"
    with open(out_file,"w") as f:
        process = subprocess.Popen(cmd,shell=True,env=env,stdout=f,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL)
    process.wait()
    callback(process.returncode,id,session,str(report_path))

def callback_func(returncode:int,id:int,session:SessionDep,report_path:str):
    end_time = datetime.now(timezone.utc)
    process_db = get_process_by_id(session,id)
    start_time = process_db.start_time.replace(tzinfo=timezone.utc)
    seconds = int((end_time - start_time).total_seconds())
    delta = timedelta(seconds=seconds)
    duration = str(delta)
    if returncode == 0:
        process = ProcessUpdate(status="已完成",end_time=end_time,duration=duration,report_url=str(report_path))
    else:
        process = ProcessUpdate(status="失败",end_time=end_time,duration=duration,report_url=str(report_path))
    update_process(session,id,process)
        

def exec_command(type:str,name:str,args:str,id:int,session:SessionDep):
    app_path = Path(__file__).parents[2]
    time_stamp = int(time.time() * 1000)
    report_path = app_path / "reports" / "jmeter" / f"{time_stamp}_{name}"
    os.mkdir(report_path)
    tool_path = app_path / "tools"
    if type == "JMeter":
        jmeter_conf = data["tools"]["jmeter"]
        jmx_path = tool_path / "jmeter" / f"{jmeter_conf["file"]}"
        env = os.environ.copy()
        env["JMETER_HOME"] = jmeter_conf["home"]
        log_path = report_path / "jmeter_test.log"
        out_path = report_path / "log"
        os.mkdir(out_path)
        host = args.split("host:")[1]
        thread = threading.Thread(target=exec_worker,args=(f"{jmeter_conf["path"]} -n -t {jmx_path} -l {log_path}  -H {host} -P {jmeter_conf["port"]} -e -o {out_path}",callback_func,env,report_path,id,session))
        # thread.daemon = True
        thread.start()
        return {
            "report_path":report_path,
            "html_path":report_path / "log" / "index.html"
        }

@router.get("/")
def get_process_api(session:SessionDep,offset:int = 0,limit:int = 10):
    return get_process(session,offset,limit)

@router.get("/{id}")
def get_process_by_id_api(session:SessionDep,id:int):
    return get_process_by_id(session,id)

@router.post("/")
def insert_process_api(session:SessionDep,process:Process):
    process_db = insert_process(session,process)
    exec_command(process.type,process.name,process.args,process_db.id,session)
    return {
        "ok":True,
        "insert_process":process_db
    }

@router.patch("/{id}")
def update_process_api(session:SessionDep,id:int,process_update:ProcessUpdate):
    return update_process(session,id,process_update)

@router.delete("/{id}")
def delete_process_api(session:SessionDep,id:int):
    return delete_process(session,id)
    
@router.get("/url/{id}")
async def download_report(session:SessionDep,id:int):
    process = get_process_by_id(session,id)
    return await get_file(url=process.report_url)