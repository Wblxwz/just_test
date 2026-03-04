from sqlmodel import create_engine,SQLModel,Session
from typing import Annotated
from fastapi import Depends

mysql_url = "mysql+pymysql://root:a2394559659@localhost:3306/just_test?charset=utf8mb4"

engine = create_engine(mysql_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]