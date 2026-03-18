from sqlmodel import SQLModel,Field
from datetime import datetime,timezone

class File(SQLModel,table=True):
    id: int | None = Field(default=None,primary_key=True)
    name: str = Field(default="")
    leaf: bool = Field(default=True)
    parent_id: int = Field(default=0)
    file_size: str = Field(default="0kb")
    url: str = Field(default="")

#后续实现上传自定义脚本功能
class Script(SQLModel,table=True):
    id:int | None = Field(default=None,primary_key=True)
    name: str = Field(default="")
    describe: str | None = Field(default="")
    params: str | None = Field(default="")
    report_url: str = Field(default="")
    duration:datetime | None = Field()

class Process(SQLModel,table=True):
    id:int | None = Field(default=None,primary_key=True)
    name: str = Field(default="")
    describe: str | None = Field(default="")
    type: str | None = Field(default="")
    args: str = Field(default="")
    command: str | None = Field(default="")
    report_url: str = Field(default="")
    start_time: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    end_time: datetime | None = Field()
    status: str = Field(default="运行中")
    duration:str | None = Field()
    remain_time:datetime | None = Field()
    elapsed_time:datetime | None = Field()

class ProcessUpdate(SQLModel,table=False):
    id:int | None = None
    name: str = None
    describe: str | None = None
    type: str | None = None
    host: str | None = None
    command: str | None = None
    report_url: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: str | None = None
    duration:str | None = None
    remain_time:datetime | None = None
    elapsed_time:datetime | None = None