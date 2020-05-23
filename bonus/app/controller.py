##
## EPITECH PROJECT, 2020
## WEB_epytodo_2019
## File description:
## controller
##

from app import render_template, json, session
from app.models import DBUserAuth, DBUserTasks

class Controller():
    def __init__(self, app, database):
        self.app = app
        self.db = database
        self.user = DBUserAuth(app, database)

    def get_index_template(self):
        return render_template("index.html")

class Authentification():
    def __init__(self, app, database):
        self.app = app
        self.db = database
        self.user = DBUserAuth(app, database)

    def register_user(self, request):
        json_return = {}
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        if username == None or email == None or password == None:
            json_return['error'] = 'internal error'
        else:
            if self.user.check_users(username, email) == 1:
                json_return['error'] = 'account already exists'
            else:
                self.user.create_new_user(username, email, password)
                json_return['result'] = 'account created'
        return json_return
    
    def signin_user(self, request):
        json_return = {}
        username = request.json['username']
        password = request.json['password']
        if username == None or password == None:
            json_return['error'] = 'internal error'
        else:
            if self.user.login_user(username, password) == 1:
                json_return['error'] = 'login or password does not match'
            else:
                session['username'] = username
                json_return['result'] = 'signin successful'
        return json_return

    def signout_user(self):
        json_return = {}
        session.pop('username', None)
        json_return['result'] = 'signout successful'
        return json_return

class UserTasks():
    def __init__(self, app, database):
        self.app = app
        self.db = database
        self.user = DBUserAuth(app, database)
        self.task = DBUserTasks(app, database)        
    
    def user_informations(self):
        json_return = {}
        if session and session['username']:
            user_id = self.user.user_id(session['username'])
            result = self.user.get_user_infos(session['username'], user_id)
            if result == False:
                json_return['error'] = 'internal error'
            else:
                json_return['result'] = result
        else:
            json_return['error'] = 'you must be logged in'
        return json_return

    def get_user_tasks(self):
        json_return = {}
        json_tasks = {}
        if session and session['username']:
            user_id = self.user.user_id(session['username'])
            result = self.task.get_user_tasks(user_id)
            if result == False:
                json_return['error'] = 'internal error'
            else:
                json_tasks['tasks'] = result
                json_return['result'] = json_tasks
        else:
            json_return['error'] = 'you must be logged in'
        return json_return

    def get_id_task(self, task_id):
        json_return = {}
        if session and session['username']:
            user_id = self.user.user_id(session['username'])
            if self.task.own_user(user_id, task_id) == 0:
                result = self.task.get_id_task(user_id, task_id)
                if result == False:
                    json_return['error'] = 'internal error'
                else:
                    json_return['result'] = result
            else:
                json_return['error'] = 'task id does not exist'
        else:
            json_return['error'] = 'you must be logged in'
        return json_return

    def update_task(self, task_id, request):
        json_return = {}
        title = request.json['title']
        begin = request.json['begin']
        end = request.json['end']
        status = request.json['status']
        if session and session['username']:
            if self.task.exists_id_task(task_id) == 0:
                user_id = self.user.user_id(session['username'])
                if self.task.own_user(user_id, task_id) == 1:
                    json_return['error'] = 'internal error'
                else:
                    if self.task.update_task(user_id, task_id, title, begin, end, status) == 0:
                        json_return['result'] = 'update done'
                    else:
                        json_return['error'] = 'internal error'
            else:
                json_return['error'] = 'task id does not exist'
        else:
            json_return['error'] = 'you must be logged in'
        return json_return

    def new_task(self, request):
        json_return = {}
        title = request.json['title']
        begin = request.json['begin']
        end = request.json['end']
        status = request.json['status']
        if session and session['username']:
            user_id = self.user.user_id(session['username'])
            if self.task.create_new_task(user_id, title, begin, end, status) == 1:
                json_return['error'] = 'internal error'
            else:
                json_return['result'] = 'new task added'
        else:
            json_return['error'] = 'you must be logged in'
        return json_return

    def del_task(self, task_id):
        json_return = {}
        if session and session['username']:
            if self.task.exists_id_task(task_id) == 0:
                user_id = self.user.user_id(session['username'])
                if self.task.own_user(user_id, task_id) == 1:
                    json_return['error'] = 'internal error'
                else:
                    if self.task.delete_task(user_id, task_id) == 0:
                        json_return['result'] = 'task deleted'
                    else:
                        json_return['error'] = 'internal error'
            else:
                json_return['error'] = 'task id does not exist'
        else:
            json_return['error'] = 'you must be logged in'
        return json_return