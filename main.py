from fastapi import FastAPI, Depends
from sqlalchemy import Integer, Boolean, String
from sqlalchemy.orm import Session

from schemes import TaskADD
from database import TaskDB, Base, engine, get_db

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message" : "Start"}

@app.post("/tasks/")
def create_task(task : TaskADD, db : Session  = Depends(get_db)):
    new_task = TaskDB(id =task.id, title = task.title, completed = task.completed)
    try:
        db.add(new_task)
        db.commit()
        return {'message': f'Task {task.id} was created', 'task': task}
    except:
        return {'message': f'Task {task.id} was failed', 'task': task}

@app.get("/tasks/")
def get_tasks(db : Session = Depends(get_db), completed : bool = None, limit : int = None):
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
def update_task(task_id : int, new_status : bool, db : Session = Depends(get_db)):
    db.query(TaskDB).filter(TaskDB.id == task_id).update({TaskDB.completed :  new_status})
    db.commit()
    return {'message': f'Task {task_id} status was updated'}