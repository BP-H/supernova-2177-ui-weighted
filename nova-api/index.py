# nova-api/index.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/api")
def hello_world():
    return {"message": "Hello from the Python API!"}
