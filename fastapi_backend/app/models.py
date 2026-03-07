from sqlmodel import SQLModel,Field

class File(SQLModel,table=True):
    id: int | None = Field(default=None,primary_key=True)
    name: str = Field(default="")
    leaf: bool = Field(default=True)
    parent_id: int = Field(default=0)
    file_size: str = Field(default="")
    url: str = Field(default="")