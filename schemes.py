from pydantic import BaseModel
from typing import Optional

class TaskADD(BaseModel):
    id : int
    title : str
    completed : bool
    description : Optional[str] = None