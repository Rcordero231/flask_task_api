from app import app
from fake_data.tasks import tasks_list
from flask import request
from datetime import datetime



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

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    data = request.is_json
    required_fields = ['title', 'description']
    missing_fields = []
    for fields in required_fields:
        if fields not in data:
            missing_fields.append(fields)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400

    title = data.get('title')
    description = data.get('description')
    new_tasks = {
        "id": len(tasks_list) +1,
        'title': title,
        "description": description,
        'completed': False,
        "createdAt": datetime.utcnow()
    }
    tasks_list.append(new_tasks)
    return new_tasks, 201