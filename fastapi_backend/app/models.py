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
    report_url: str = Field(default="")
    start_time: datetime = Field(default=datetime.now(timezone.utc))
    end_time: datetime | None = Field()
    status: str = Field(default="运行中")
    duration:datetime | None = Field()
    remain_time:datetime | None = Field()