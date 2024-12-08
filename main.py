from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from typing import Optional


app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "Start"}

@app.post("/tasks/")
def create_task():
    pass

@app.get("/tasks/")
def get_task():
    pass

@app.delete("/tasks/")
def delete_task():
    pass

@app.patch("/tasks/")
def update_task():
    pass