import streamlit as st
import requests

API_URL = 'http://127.0.0.1:8000/'
st.title("Task Manager")

email = 'zaglyshka@gate.not'

def get_tasks():
    response = requests.get(f"{API_URL}/tasks")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch tasks")
        return {}

def update_task(task):
    response = requests.patch(f"{API_URL}/tasks", json=task)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch tasks")

def delete_task(task_id):
    response = requests.delete(f"{API_URL}/tasks", params={'task_id' : task_id})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch tasks")

def create_task(task):
    response = requests.post(f"{API_URL}/tasks", json=task)
    if response.status_code == 200:
        params_email = {'email' : email}
        response_email = requests.post(f"{API_URL}/send-notification/{email}", params=params_email)
        if response_email.status_code == 200:
            st.write(response_email)
        else:
            st.write('Failed to send email')
        return response.json()
    else:
        st.error("Failed to fetch tasks")


def show_add_menu():
    st.header(f"Добавление задачи")
    with st.form("add_form"):
        title = st.text_input("Название задачи")
        completed = st.checkbox("Задача выполнена")
        submitted = st.form_submit_button("Сохранить")

        if submitted:
            st.success(f"Задача сохранена: {title}, выполнена: {completed}")
            st.session_state.show_add_menu = False
            new_task = {
                'id' : 0,
                'title' : title,
                'completed' : completed
            }
            st.write(new_task)
            create_task(new_task)
            st.rerun()

def show_edit_menu(task):
    st.header(f"Редактирование задачи")
    with st.form(f"edit_form{task['id']}"):
        title = st.text_input("Название задачи", value= f"{task['title']}")
        col1, col2, col3 = st.columns([2, 6, 2])
        with col1:
            submitted = st.form_submit_button("Сохранить")
        with col3:
            deleted = st.form_submit_button("Удалить")

        if deleted:
            delete_task(task['id'])
            st.rerun()
        elif submitted:
            st.success(f"Задача обновлена")
            task['title'] = title
            update_task(task)
            st.session_state.show_edit_menu = False
            st.rerun()

def show_task_menu(task):
    st.subheader("Подробное описание задачи")
    st.write("---")
    st.markdown(f"**Название:** {task['title']}")
    st.markdown(f"**Выполнена:** {'Да' if task['completed'] else 'Нет'}")
    if st.button("Закрыть", key=f"close_details_{task['id']}"):
        st.session_state[f"show_details_{task['id']}"] = False
    st.write("---")

def show_all_tasks(tasks):
    for task in tasks:
        with st.container(border=True):
            col1, col2, col3 = st.columns([8, 1, 1])  # Название задачи, кнопка, чекбокс
            with col1:
                if st.button(task["title"], key=f"title_{task['id']}", use_container_width=True):
                    current_state = st.session_state.get(f"show_details_{task['id']}", False)
                    st.session_state[f"show_details_{task['id']}"] = not current_state

            with col2:
                if st.button("✏️", key=f"edit_{task['id']}"):
                    current_state = st.session_state.get(f"show_edit_{task['id']}", False)
                    st.session_state[f"show_edit_{task['id']}"] = not current_state

            with col3:
                completed = st.checkbox("", value=task["completed"], key=f"chk_{task['id']}")
                if completed != task["completed"]:
                    task["completed"] = completed
                    update_task(task)
                    st.rerun()

        if st.session_state.get(f"show_details_{task['id']}", False):
            show_task_menu(task)
        if st.session_state.get(f"show_edit_{task['id']}", False):
            show_edit_menu(task)

    if st.button("Add Task", use_container_width=True):
        current_state = st.session_state.get(f"show_add_menu", False)
        st.session_state[f"show_add_menu"] = not current_state

    if st.session_state.get(f"show_add_menu", False):
        show_add_menu()

show_all_tasks(get_tasks())