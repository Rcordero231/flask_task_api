from app import app
from fake_data.tasks import tasks_list




app.route('/')
def hello_world():
    return 'Hello World!!'

@app.route('/tasks')
def get_tasks():
    tasks = tasks_list
    return tasks


@app.route('/tasks/<int:task_id>')
def get_task_id(task_id):
    tasks = tasks_list
    for task in tasks:
        if task['id'] == task_id:
            return task
    return {'Error': f"Task with ID {task_id} does NOT exist"}, 404