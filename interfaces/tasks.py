import time, datetime
import json
from flask import request
from classes import Task, TaskStatus
from infrastructure.repositories import getDomainRegistry
from infrastructure.db import Database
import requests
import classes.ip2address
import threading


def queryTasks():
    db = Database()
    conn = db.getConn()
    cr = conn.cursor()

    try:
        offset = int(request.args["offset"]) or 0
    except:
        offset = 0

    try:
        limit = int(request.args["limit"]) or 10
    except:
        limit = 10

    cr.execute("SELECT id, name, status, createtime, completetime, progress FROM tasks ORDER BY createtime DESC LIMIT %s OFFSET %s", (limit, offset))
    tasks = cr.fetchall()

    cr.execute("SELECT COUNT(*) as count FROM tasks")
    totalNumber = cr.fetchone()["count"]

    cr.close()
    conn.close()

    return json.dumps({
        "tasks": tasks,
        "totalNumber": totalNumber
    })

def queryTaskDetail(taskId):
    db = Database()
    conn = db.getConn()
    c = conn.cursor()

    c.execute(
        "SELECT id, name, status, createtime, completetime, progress, start_ip, end_ip, start_port, end_port, plugins, node_id, scan_result FROM tasks WHERE id = %s",
        (taskId))

    task = c.fetchone()

    if not task:
        return ("TASKID_IS_INEXISTENCE", 400)
    else:
        taskData = {
            "id": task["id"],
            "name": task["name"],
            "status": task["status"],
            "createtime": task["createtime"],
            "completetime": task["completetime"],
            "progress": task["progress"],
            "startIP": task["start_ip"],
            "endIP": task["end_ip"],
            "startPort": task["start_port"],
            "endPort": task["end_port"],
            "plugins": json.loads(task["plugins"]),
            "nodeId": task["node_id"],
            "scanResult": json.loads(task["scan_result"] or None)
        }
    conn.close()

    return json.dumps({
        "task": taskData
    })

def createTask():
    data = request.data
    data = json.loads(data)
    assert data["name"]
    assert data["startIP"]
    assert data["endIP"]
    assert data["startPort"] >= 0
    assert data["endPort"] >= 0
    assert len(data["plugins"]) >= 0
    assert data["nodeId"]

    task = Task()
    task.name = data["name"]
    task.startIP = data["startIP"]
    task.endIP = data["endIP"]
    task.startPort = data["startPort"]
    task.endPort = data["endPort"]
    task.plugins = data["plugins"]
    task.nodeId = data["nodeId"]
    task.createtime = int(round(time.time() * 1000))

    getDomainRegistry().TaskRepository().save(task)
    threading.Thread(target=sendTask, args=[task.id]).start()

    return json.dumps(task.toDict())

def sendTask(id):
    task = getDomainRegistry().TaskRepository().getTaskById(id)
    nodeId = task.nodeId
    node = getDomainRegistry().NodeRepository().getNodeById(nodeId)

    if node:
        r = requests.post("http://" + classes.ip2address.long2ip(node.ip) + ":" + str(node.port) + "/tasks")


def updateTaskInfo(id, progress, result):
    task = getDomainRegistry().TaskRepository().getTaskById(id)

    if task.status == TaskStatus(2):
        closeTask(id)
        return

    task.progress = progress

    if progress == 0:
        task.status = TaskStatus(0)
    elif progress == 1 and result:
        closeTask(id)
        task.status = TaskStatus(2)
        task.scanResult = result
        task.completetime = int(round(time.time() * 1000))
    else:
        task.status = TaskStatus(1)

    getDomainRegistry().TaskRepository().save(task)

def closeTask(id):
    task = getDomainRegistry().TaskRepository().getTaskById(id)
    nodeId = task.nodeId
    node = getDomainRegistry().NodeRepository().getNodeById(nodeId)

    if node:
        r = requests.post("http://" + classes.ip2address.long2ip(node.ip) + ":" + str(node.port) + "/tasks/"+ task.id +"/complete")

# 更新节点信息
def autoUpdateTasksInfo():
    def updateInfos():
        db = Database()
        conn = db.getConn()
        while 1:
            try:
                cr = conn.cursor()
                cr.execute("SELECT id, active, ip, port FROM nodes WHERE active = 1")
                nodes = cr.fetchall()
                cr.close()
                for node in nodes:
                    node = getDomainRegistry().NodeRepository().getNodeById(node["id"])
                    node.updateNodeTasks()
            finally:
                time.sleep(5)

    threading.Thread(target=updateInfos).start()



