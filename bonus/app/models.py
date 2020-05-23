##
## EPITECH PROJECT, 2020
## WEB_epytodo_2019
## File description:
## models
##

from app import json
import pymysql as sql
from datetime import datetime

class DBConnection():
    def __init__(self, app):
        self.app = app
        self.db = None
        self.connection(app.config)

    def connection(self, app_conf):
        try:
            if app_conf['DATABASE_SOCK'] != None:
                self.db = sql.connect(unix=app_conf['DATABASE_SOCK'],
                    db=app_conf['DATABASE_NAME'],
                    user=app_conf['DATABASE_USER'],
                    password=app_conf['DATABASE_PASS'])
            else:
                self.db = sql.connect(db=app_conf['DATABASE_NAME'],
                    host=app_conf['DATABASE_HOST'],
                    user=app_conf['DATABASE_USER'],
                    password=app_conf['DATABASE_PASS'])
        except:
            print('Error: Database connection impossible')
            exit(84)

    def get_database(self):
        return self.db

class DBUserAuth():
    def __init__(self, app, database):
        self.app = app
        self.db = database

    def user_id(self, username):
        cursor = self.db.db.cursor()
        cursor.execute("SELECT * FROM user")
        result = cursor.fetchall()
        for saved_user in result:
            if saved_user[1] == username:
                cursor.close()
                return saved_user[0]
        return -1

    def check_users(self, username, email):
        cursor = self.db.db.cursor()
        cursor.execute("SELECT * FROM user")
        result = cursor.fetchall()
        for saved_user in result:
            if saved_user[1] == username or saved_user[2] == email:
                cursor.close()
                return 1
        return 0

    def create_new_user(self, username, email, password):
        cursor = self.db.db.cursor()
        cursor.execute("INSERT INTO user (username, email, password) VALUES ('%s', '%s', '%s')" % (username, email, password))
        self.db.db.commit()
        cursor.close()
        return 0

    def login_user(self, username, password):
        cursor = self.db.db.cursor()
        cursor.execute("SELECT * FROM user")
        result = cursor.fetchall()
        for saved_user in result:
            if saved_user[1] == username and saved_user[3] == password:
                cursor.close()
                return 0
        cursor.close()
        return 1

    def get_user_infos(self, username, user_id):
        json_return = {}
        count_user_task = 0

        try:
            cursor = self.db.db.cursor()
            cursor.execute("SELECT * FROM user WHERE user_id = %s" % (user_id))
            result = cursor.fetchall()[0]
            cursor.close()
            if result[0] != None and result[1] != None and result[2] != None:
                json_return['user_id'] = result[0]
                json_return['username'] = result[1]
                json_return['email'] = result[2]
            else:
                return False
            cursor = self.db.db.cursor()
            cursor.execute("SELECT * FROM user_has_task WHERE fk_user_id = %d" % (user_id))
            result = cursor.fetchall()
            cursor.close()
            for _ in result:
                count_user_task += 1
            json_return['nb_tasks'] = count_user_task
        except:
            return False
        return json_return

class DBUserTasks():
    def __init__(self, app, database):
        self.app = app
        self.db = database

    def exists_id_task(self, task_id):
        cursor = self.db.db.cursor()
        cursor.execute("SELECT * FROM task")
        all_task_id = cursor.fetchall()
        for actual_id in all_task_id:
            if actual_id[0] == task_id:
                return 0
        return 1

    def own_user(self, user_id, task_id):
        cursor = self.db.db.cursor()
        cursor.execute("SELECT * FROM user_has_task")
        all_user_task = cursor.fetchall()
        for actual in all_user_task:
            if actual[0] == user_id and actual[1] == task_id:
                return 0
        return 1

    def get_user_tasks(self, user_id):
        result_array = []
        try:
            cursor = self.db.db.cursor()
            cursor.execute("SELECT fk_task_id FROM user_has_task WHERE fk_user_id = %d" % (user_id))
            result = list(cursor.fetchall())
            cursor.close()
            for task_id in result:
                json_ids = {}
                json_elem = {}
                cursor = self.db.db.cursor()
                cursor.execute("SELECT * FROM task WHERE task_id = %d" % (task_id[0]))
                actual_task = list(cursor.fetchall()[0])
                json_elem['title'] = actual_task[1]
                json_elem['begin'] = datetime.strftime(actual_task[2], "%Y-%m-%d %H:%M:%S")
                json_elem['end'] = datetime.strftime(actual_task[3], "%Y-%m-%d %H:%M:%S")
                json_elem['status'] = actual_task[4]
                json_ids[actual_task[0]] = json_elem
                result_array.append(json_ids)
                cursor.close()
        except:
            return False
        return result_array

    def get_id_task(self, user_id, task_id):
        try:
            cursor = self.db.db.cursor()
            cursor.execute("SELECT * FROM task WHERE task_id = %d" % (task_id))
            result = list(cursor.fetchall()[0])
            if result[2] != None:
                result[2] = datetime.strftime(result[2], "%Y-%m-%d %H:%M:%S")
            if result[3] != None:
                result[3] = datetime.strftime(result[3], "%Y-%m-%d %H:%M:%S")
            cursor.close()
        except:
            return False
        return result[1:]

    def update_task(self, user_id, task_id, title, begin, end, status):
        try:
            begin = datetime.strptime(begin, "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            cursor = self.db.db.cursor()
            cursor.execute("UPDATE task SET title = '%s', begin = '%s', end = '%s', status = '%s' WHERE task_id = %d" % (title, begin, end, status, task_id))
            self.db.db.commit()
            cursor.close()
            return 0
        except (Exception) as err:
            print(err)
            return 1

    def create_new_task(self, user_id, title, begin, end, status):
        try:
            # Create new task
            begin = datetime.strptime(begin, "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            cursor = self.db.db.cursor()
            cursor.execute("INSERT INTO task (title, begin, end, status) VALUES ('%s', '%s', '%s', '%s')" % (title, begin, end, status))
            self.db.db.commit()
            task_id = cursor.lastrowid
            cursor.close()
            # Link task_id with user_id
            cursor = self.db.db.cursor()
            cursor.execute("INSERT INTO user_has_task (fk_user_id, fk_task_id) VALUES (%d, %d)" % (user_id, task_id))
            self.db.db.commit()
            cursor.close()
            return 0
        except:
            return 1

    def delete_task(self, user_id, task_id):
        try:
            cursor = self.db.db.cursor()
            cursor.execute("DELETE FROM user_has_task WHERE fk_user_id = %d AND fk_task_id = %d" % (user_id, task_id))
            self.db.db.commit()
            cursor.close()
            # Link task_id with user_id
            cursor = self.db.db.cursor()
            cursor.execute("DELETE FROM task WHERE task_id = %d" % (task_id))
            self.db.db.commit()
            cursor.close()
            return 0
        except:
            return 1