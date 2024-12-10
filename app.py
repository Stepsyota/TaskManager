import streamlit as st

from frontend import show_task_buttons, add_task_button, apply_css
from database import get_db, Session
from main import create_task, get_tasks
from schemes import TaskADD
import pandas as pd
import requests

API_URL = 'http://127.0.0.1:8000/'
st.title("Task Manager")
apply_css()
def show_tasks():
    response = requests.get(f"{API_URL}/tasks")
    if response.status_code == 200:
        show_task_buttons(response.json())
    else:
        st.error("Failed to fetch tasks")

def delete_task(task_id):
    params = {}
    params['task_id'] = task_id
    response = requests.delete(f"{API_URL}/tasks", params=params)
    if response.status_code == 200:
        st.write("SUCCES")
    else:
        st.error("Failed to fetch tasks")
show_tasks()
add_task_button()

delete_task(1200)