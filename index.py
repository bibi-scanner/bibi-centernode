from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import datetime

import interfaces.tasks as tasksInterfaces
import interfaces.nodes as nodesInterfaces
import interfaces.info as infoInterfaces

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(seconds=30000)

jwt = JWT(app, authenticate, identity)


############################# webapi

# 系统信息查询接口
@app.route('/sysinfo', methods=['GET'])
@jwt_required()
def sysinfo():
    return infoInterfaces.systemInfo()

@app.route('/tasks', methods=['POST'])
@jwt_required()
def createTask():
    return tasksInterfaces.createTask()

@app.route('/nodes', methods=['POST'])
@jwt_required()
def createNode():
    return nodesInterfaces.createNode()


if __name__ == '__main__':
    app.run(port=3000)