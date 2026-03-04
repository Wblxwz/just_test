from models import *

from sqlmodel import Session

def create_file(file:File,session:Session)->File:
    session.add(file)
    session.commit()
    session.refresh(file)
    return file