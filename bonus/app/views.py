##
## EPITECH PROJECT, 2020
## WEB_epytodo_2019
## File description:
## views
##

from app import *

@app.route('/', methods=['GET'])
def route_home():
    controller = Controller(app, database)
    return controller.get_index_template()

@app.route('/register', methods=['POST'])
def route_register_user():
    auth = Authentification(app, database)
    return jsonify(auth.register_user(request))

@app.route('/signin', methods=['POST'])
def route_signin_user():
    auth = Authentification(app, database)
    return jsonify(auth.signin_user(request))

@app.route('/signout', methods=['POST'])
def route_signout_user():
    auth = Authentification(app, database)
    return jsonify(auth.signout_user())

@app.route('/user', methods=['GET'])
def route_user():
    user = UserTasks(app, database)
    return jsonify(user.user_informations())

@app.route('/user/task', methods=['GET'])
def route_user_task():
    user_tasks = UserTasks(app, database)
    return jsonify(user_tasks.get_user_tasks())

@app.route('/user/task/<int:task_id>', methods=['GET', 'POST'])
def route_id_task(task_id):
    user_tasks = UserTasks(app, database)
    if request.method == 'GET':
        return jsonify(user_tasks.get_id_task(task_id))
    if request.method == 'POST':
        return jsonify(user_tasks.update_task(task_id, request))

@app.route('/user/task/add', methods=['POST'])
def route_task_add():
    user_tasks = UserTasks(app, database)
    return jsonify(user_tasks.new_task(request))

@app.route('/user/task/del/<int:task_id>', methods=['POST'])
def route_task_del(task_id):
    user_tasks = UserTasks(app, database)
    return jsonify(user_tasks.del_task(task_id))