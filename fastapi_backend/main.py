from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def test1():
    return "123"