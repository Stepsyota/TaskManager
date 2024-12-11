from pydantic import BaseModel

class TaskADD(BaseModel):
    title : str
    completed : bool = False

class TaskUPDATE(BaseModel):
    id : int
    title: str
    completed: bool = False