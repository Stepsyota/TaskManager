from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_create_item():
    response = client.post("/tasks/", json={"title": "New Task", "completed": False})
    task_id = response.json()['id']
    assert response.status_code == 200
    assert response.json() == {
        'title' : 'New Task',
        'completed' : False,
        'id' : task_id
    }
    response_delete = client.delete("/tasks/", params={'task_id': task_id})

def test_get_item():
    response = client.post("/tasks/", json={"title": "Another Task", "completed": True})
    task_id = response.json()['id']

    response_get = client.get("/tasks/")
    assert response_get.status_code == 200
    for task in response_get.json():
        if task['id'] == task_id:
            assert task["title"] == "Another Task" and task["completed"] == True

    response_delete = client.delete("/tasks/", params={'task_id': task_id})

def test_update_item():
    response = client.post("/tasks/", json={"title": "Task to Update", "completed": False})
    task_id = response.json()["id"]

    response_update = client.patch("/tasks/", json={"id": task_id, "title": "Updated Task", "completed": True})
    assert response_update.status_code == 200
    assert response_update.json() == {
        "title" : "Updated Task",
        "completed" : True,
        "id" : task_id
    }
    response_delete = client.delete("/tasks/", params={'task_id' : task_id})

def test_delete_item():
    response = client.post("/tasks/", json={"title": "Task to del", "completed": True})
    task_id = response.json()['id']

    response_delete = client.delete("/tasks/", params={'task_id' : task_id})
    assert response_delete.status_code == 200
    assert response_delete.json() == {
        'id' : task_id,
        'title' : "Task to del",
        'completed' :  True
    }

