import streamlit as st
import sqlite3
from datetime import datetime

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        st.error(e)
    return conn

# Function to create tasks table
def create_tasks_table(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tasks
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     task TEXT NOT NULL,
                     priority INTEGER,
                     due_date DATE,
                     completed BOOLEAN)''')
    except sqlite3.Error as e:
        st.error(e)

# Function to add a task
def add_task(conn, task, priority, due_date):
    try:
        c = conn.cursor()
        c.execute('''INSERT INTO tasks (task, priority, due_date, completed) 
                     VALUES (?, ?, ?, ?)''', (task, priority, due_date, False))
        conn.commit()
        st.success("Task added successfully!")
    except sqlite3.Error as e:
        st.error(e)

# Function to delete a task
def delete_task(conn, task_id):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        st.success("Task deleted successfully!")
    except sqlite3.Error as e:
        st.error(e)

# Function to mark a task as completed
def mark_completed(conn, task_id):
    try:
        c = conn.cursor()
        c.execute("UPDATE tasks SET completed=True WHERE id=?", (task_id,))
        conn.commit()
        st.success("Task marked as completed!")
    except sqlite3.Error as e:
        st.error(e)

# Function to display tasks
def view_tasks(conn):
    st.write("### Your Tasks:")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    for task in tasks:
        st.write(f"**{task[1]}** - Priority: {task[2]}, Due Date: {task[3]}, Completed: {task[4]}")

# Main function to run the Streamlit app
def main():
    st.title("Advanced Routine Management API")
    
    # Create a database connection
    conn = create_connection("tasks.db")
    if conn is not None:
        # Create tasks table if it doesn't exist
        create_tasks_table(conn)
        
        # Sidebar to perform actions
        st.sidebar.title("Actions")
        action = st.sidebar.selectbox("Select Action", ["Add Task", "Delete Task", "Mark Completed", "View Tasks"])
        
        if action == "Add Task":
            new_task = st.text_input("Enter new task:")
            priority = st.selectbox("Select priority:", ["Low", "Medium", "High"])
            due_date = st.date_input("Select due date:", datetime.today())
            if st.button("Add"):
                priority_map = {"Low": 1, "Medium": 2, "High": 3}
                add_task(conn, new_task, priority_map[priority], due_date)
        
        elif action == "Delete Task":
            task_id = st.selectbox("Select task to delete:", options=[task[1] for task in view_tasks(conn)])
            if st.button("Delete"):
                delete_task(conn, task_id)
        
        elif action == "Mark Completed":
            task_id = st.selectbox("Select task to mark as completed:", options=[task[1] for task in view_tasks(conn)])
            if st.button("Mark Completed"):
                mark_completed(conn, task_id)
        
        elif action == "View Tasks":
            view_tasks(conn)

if __name__ == "__main__":
    main()
