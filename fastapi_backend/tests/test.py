from random import choice
import string
import sys
sys.path.append("e:\\WorkSpace\\just_test\\fastapi_backend")
from app.db import get_session
from app.crud import create_file
from app.models import File

def random_string(length:int):
    chars = string.ascii_letters + string.digits
    return ''.join(choice(chars) for _ in range(length))

def insert_files(nums:int):
    session = next(get_session())
    file = File()
    file.name = random_string(10)
    file.leaf = False
    file.parent_id = 0
    file.file_size = random_string(15)
    file.url = random_string(20)
    result_file = create_file(file,session)
    for i in range(nums):
        tmp_file = File()
        tmp_file.name = random_string(10)
        tmp_file.leaf = True
        tmp_file.parent_id = result_file.id
        tmp_file.file_size = random_string(15)
        tmp_file.url = random_string(20)
        create_file(tmp_file,session)

if __name__ == "__main__":
    insert_files(20)
