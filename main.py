from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from schemes import TaskADD
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

@app.get("/")
def read_root():
    return {"message" : "Start"}

@app.post("/tasks/")
def create_task(task : TaskADD, db : Session  = Depends(get_db)):
    new_task = TaskDB(title = task.title, completed = task.completed)
    db.add(new_task)
    db.commit()
    return {'message' : f'Task {task.id} was created'}

@app.get("/tasks/")
def get_tasks(completed : bool = None, limit : int = None, db : Session = Depends(get_db)):
    query = db.query(TaskDB)
    if completed:
        query = query.filter(TaskDB.completed == completed)
    if limit:
        query = query.limit(limit)
    return query.all()

@app.delete("/tasks/")
def delete_task(task_id : int, db : Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    db.delete(task)
    db.commit()
    return {'message' : f'Task {task_id} was deleted'}

@app.patch("/tasks/")
def update_task(task : TaskADD, db : Session = Depends(get_db)):
    db.query(TaskDB).filter(TaskDB.id == task.id).update({TaskDB.completed : task.completed, TaskDB.title : task.title})
    db.commit()
    return {'message': f'Task {task.id} status was updated'}