from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import datetime
from flask_cors import CORS
import threading

import interfaces.tasks as tasksInterfaces
import interfaces.nodes as nodesInterfaces
import interfaces.info as infoInterfaces
import interfaces.plugins as pluginsInterfaces


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


users = [
    User(1, 'admin', '123456a'),
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
CORS(app)

jwt = JWT(app, authenticate, identity)


############################# webapi

# 登录检测接口
@app.route('/authcheck', methods=['GET'])
@jwt_required()
def authcheck():
    return "ok"

# 系统信息查询接口
@app.route('/sysinfo', methods=['GET'])
@jwt_required()
def sysinfo():
    return infoInterfaces.systemInfo()


# 任务列表查询接口
@app.route('/tasks', methods=['GET'])
@jwt_required()
def queryTasks():
    return tasksInterfaces.queryTasks()


# 创建任务
@app.route('/tasks', methods=['POST'])
@jwt_required()
def createTask():
    return tasksInterfaces.createTask()


# 获取指定任务详情
@app.route('/tasks/<taskId>', methods=['GET'])
@jwt_required()
def queryTaskDetail(taskId):
    return tasksInterfaces.queryTaskDetail(taskId)

#TODO 删除任务

# 查询节点列表
@app.route('/nodes', methods=['GET'])
@jwt_required()
def queryNodes():
    return nodesInterfaces.queryNodes()

# 创建节点
@app.route('/nodes', methods=['POST'])
@jwt_required()
def createNode():
    return nodesInterfaces.createNode()

# ping节点
@app.route('/nodes/<nodeId>/ping', methods=['POST'])
@jwt_required()
def pingNode(nodeId):
    return nodesInterfaces.pingNode(nodeId)

# 节点注册
@app.route('/nodes/registry', methods=['POST'])
def registryNode():
    return nodesInterfaces.registryNode()

# 节点获取任务
@app.route('/nodes/<nodeId>/tasks', methods=['GET'])
def getNodeTasks(nodeId):
    return nodesInterfaces.getNodeTasks(nodeId)

# 节点任务状态更新
@app.route('/nodes/<nodeId>/tasks/update', methods=['POST'])
def updateNodeTasks(nodeId):
    return nodesInterfaces.updateNodeTasks(nodeId)

# 获取插件列表
@app.route('/plugins', methods=['GET'])
@jwt_required()
def queryPlugins():
    return pluginsInterfaces.queryPlugins()

# 上传插件
@app.route('/plugins', methods=['POST'])
@jwt_required()
def uploadPlugin():
    return pluginsInterfaces.uploadPlugin()

# 下载插件
@app.route('/plugins/<pluginId>', methods=['GET'])
def downloadPluginById(pluginId):
    return pluginsInterfaces.downloadPluginById(pluginId)





if __name__ == '__main__':
    from interfaces.tasks import autoUpdateTasksInfo
    autoUpdateTasksInfo()
    app.run(port=3000, host="0.0.0.0")
