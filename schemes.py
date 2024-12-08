from pydantic import BaseModel

class TaskADD(BaseModel):
    id : int
    title : str
    completed : bool = False