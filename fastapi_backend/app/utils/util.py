from pathlib import Path

def mkdir(type:str,path:str):
    tmp_path = Path(path)
    if type == "file":
        tmp_path.touch()
    elif type == "folder":
        tmp_path.mkdir()


if __name__ == "__main__":
    mkdir()