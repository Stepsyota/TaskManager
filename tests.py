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

def test_get_item_by_status_TRUE():
    response1 = client.post("/tasks/", json={"title": "Another Task", "completed": True})
    task_id1 = response1.json()['id']
    response2 = client.post("/tasks/", json={"title": "And Another Task", "completed": False})
    task_id2 = response2.json()['id']
    response3 = client.post("/tasks/", json={"title": "And And Another Task", "completed": True})
    task_id3 = response3.json()['id']

    response_get = client.get("/tasks/", params={'completed' : True})
    assert response_get.status_code == 200
    for task in response_get.json():
            assert task["completed"] == True

    response_delete = client.delete("/tasks/", params={'task_id': task_id1})
    response_delete = client.delete("/tasks/", params={'task_id': task_id2})
    response_delete = client.delete("/tasks/", params={'task_id': task_id3})

def test_get_item_by_lmit_2():
    response1 = client.post("/tasks/", json={"title": "Another Task", "completed": True})
    task_id1 = response1.json()['id']
    response2 = client.post("/tasks/", json={"title": "And Another Task", "completed": False})
    task_id2 = response2.json()['id']
    response3 = client.post("/tasks/", json={"title": "And And Another Task", "completed": True})
    task_id3 = response3.json()['id']

    response_get = client.get("/tasks/", params={'limit' : 2})
    assert response_get.status_code == 200
    assert len(response_get.json()) == 2

    response_delete = client.delete("/tasks/", params={'task_id': task_id1})
    response_delete = client.delete("/tasks/", params={'task_id': task_id2})
    response_delete = client.delete("/tasks/", params={'task_id': task_id3})

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

