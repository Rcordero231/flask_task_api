from app import app, db
from fake_data.tasks import tasks_list
from flask import request
from datetime import datetime
from app.models import Task, User
from app.auth import basic_auth, token_auth



app.route('/')
def hello_world():
    return 'Hello World!!'

# --TASKS START --
@app.route('/tasks')
def get_tasks():
    tasks = db.session.execute(db.select(Task)).scalars().all()
    return [t.to_dict() for t in tasks]

@app.route('/tasks/<int:task_id>')
def get_task_id(task_id):
    task = db.session.get(Task, task_id)
    if task:
        return task.to_dict()
    else:
        return {'Error': f"Task with ID {task_id} does NOT exist"}, 404

@app.route('/tasks', methods=['POST'])
@token_auth.login_required
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

    user = token_auth.current_user()

    new_tasks = Task(title=title, description=description, user_id=user.id)
    return new_tasks.to_dict(), 201


@app.route('/tasks/<int:task_id>', methods=["PUT"])
@token_auth.login_required
def edit_task(task_id):
    if not request.is_json:
        return {"error":"Your content-type is not application/json"}, 400
    task = db.session.get(Task, task_id)
    if task is None:
        return {"error":f"task with the id of {task_id} does not exist!"}, 404

    current_user = token_auth.current_user()

    if task.author is not current_user:
        return {"error":"This is not your task, knock it off ya hacker"}, 403
    data = request.json
    task.update(**data)
    return task.to_dict()



@app.route('/tasks/<int:task_id>', methods=["DELETE"])
@token_auth.login_required
def delete_task(task_id):
    task = db.session.get(Task,task_id)
    if task is None:
        return {"error":f"We cannot locate tasks with the id of {task_id}"}, 404

    current_user = token_auth.current_user()

    if task.author is not current_user:
        return {"error":"You can do that, this sint your task! Get outta here!"}, 403

    task.delete()
    return {"success":f"{task.title} has been deleted!"}
# --TASK END--


# --USER START--
@app.route("/token")
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return {"token":token,
            "tokenExpiration":user.token_expiration}


@app.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    data = request.json
    required_fields = ['username', 'password', 'email']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    check_users = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalars().all()
    if check_users:
        return {'error': 'A user with that username and/or email already exists'}, 400
    new_user = User(username=username, password=password, email=email)
    return new_user.to_dict(), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
@token_auth.login_required
def update_user(user_id):
    if not request.is_json:
        return {"error": "your content type must be application/json !"}, 400
    user = db.session.get(User, user_id)
    if user is None:
        return {"error": f"User with {user_id} does not exist"},404

    current_user = token_auth.current_user()
    if user is not current_user:
        return {"error":"You cannot change this user as you are not them!"} ,403
    data = request.json
    user.update(**data)
    return user.to_dict()


@app.route("/users/<int:user_id>", methods=["DELETE"])
@token_auth.login_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    current_user = token_auth.current_user()
    if user is None:
        return {"error":f"User with {user_id} not found!"},404
    if user is not current_user:
        return {"error":"You cant do that, delete yourself only"}, 403
    user.delete()
    return{"success":f"{user.username} has been deleted!"}



@app.get("/users/<int:user_id>")
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        return user.to_dict()
    else:
        return {"error":f" user with id:{user_id} not found"}, 404
# --USER END--