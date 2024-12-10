import streamlit as st
def apply_css():
    st.markdown(
        """
        <style>
        .task-container {
            margin-bottom: 10px;
            padding: 15px;
            border-radius: 10px;
            background-color: #333;
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: #fff;
            font-family: 'Arial', sans-serif;
        }
        .task-title {
            margin: 0;
            font-size: 18px;
            cursor: pointer;
        }
        .task-checkbox {
            width: 30px;
            height: 30px;
            border: 2px solid #fff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        .task-checkbox.checked {
            background-color: #4B0082;
            color: #D3D3D3;
            border: none;
    
        }
        .task-add{
            margin: 0;
            font-size: 25px;
            margin-left: auto;
            margin-right: auto;
            cursor: pointer;
        }
        .task-edit{
            width: 30px;
            height: 30px;
            border: none;
            margin-left: auto;
            margin-right: 30px;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True,

    )

# Создание интерфейса задач

def show_task_buttons(tasks):
    for task in tasks:
        checked_class = "checked" if task["completed"] else ""
        checkbox_status = "✔" if task["completed"] else ""
        st.markdown(
            f"""
            <div class="task-container">
                <p class="task-title">{task['title']}</p>
                <div class="task-edit">{'✏️'}</div>
                <div class="task-checkbox {checked_class}">{checkbox_status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def add_task_button():
    st.markdown(
        f"""
            <div class="task-container">
                <p class = 'task-add'>{'+'}</p>
            </div>
            """,
        unsafe_allow_html=True,
    )