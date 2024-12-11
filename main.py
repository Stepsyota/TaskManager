from http.client import HTTPException

from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.openapi.utils import status_code_ranges
from sqlalchemy.orm import Session

from schemes import TaskADD, TaskUPDATE
from database import TaskDB, Base, engine, get_db
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или укажите конкретный домен фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def write_notification(email : str, message =""):
    with open("log.txt", mode='w') as email_file:
        content = f'notification for {email} : {message}'
        email_file.write(content)

@app.post("/send-notification/{email}/")
def send_notification(email : str, background_tasks : BackgroundTasks):
    background_tasks.add_task(write_notification, email, message= 'some notification')
    return {'message' : 'Notification sent in the background'}

@app.post("/tasks/")
def create_task(task : TaskADD, db : Session  = Depends(get_db)):
    new_task = TaskDB(title = task.title, completed = task.completed)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/")
def get_tasks(completed : bool | None = None, limit : int | None = None, db : Session = Depends(get_db)):
    query = db.query(TaskDB)
    if completed != None:
        query = query.filter(TaskDB.completed == completed)
    elif limit != None:
        query = query.limit(limit)
    return query.all()

@app.delete("/tasks/")
def delete_task(task_id : int, db : Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    db.delete(task)
    db.commit()
    return task

@app.patch("/tasks/")
def update_task(task : TaskUPDATE, db : Session = Depends(get_db)):
    exist_task = db.query(TaskDB).filter(TaskDB.id == task.id).first()
    if not exist_task:
        raise HTTPException(status_code=404, detail=f"Task {task.id} not found")
    exist_task.title = task.title
    exist_task.completed = task.completed
    db.commit()
    db.refresh(exist_task)
    return exist_task