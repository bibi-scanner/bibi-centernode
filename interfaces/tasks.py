import time
import json
from flask import request
from classes import Task
from infrastructure.repositories import getDomainRegistry
from infrastructure.db import Database


def queryTasks():
    db = Database()
    conn = db.getConn()

    try:
        offset = int(request.args["offset"]) or 0
    except:
        offset = 0

    try:
        limit = int(request.args["limit"]) or 10
    except:
        limit = 10

    sql = "SELECT id, name, status, createtime, completetime, progress FROM tasks ORDER BY createtime DESC LIMIT :limit OFFSET :offset"

    tasks = conn.execute(sql, {
        "offset": offset,
        "limit": limit
    }).fetchall()
    totalNumber = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]

    datas = []
    for task in tasks:
        datas.append({
            "id": task[0],
            "name": task[1],
            "status": task[2],
            "createtime": task[3],
            "completetime": task[4],
            "progress": task[5],
        })

    conn.close()

    return json.dumps({
        "tasks": datas,
        "totalNumber": totalNumber
    })

def queryTaskDetail(taskId):
    db = Database()
    conn = db.getConn()

    task = conn.execute("SELECT id, name, status, createtime, completetime, progress, start_ip, end_ip, plugins, node_id, scan_result FROM tasks WHERE id = :id", {
        "id": taskId
    }).fetchone()

    if not task:
        return ("TASKID_IS_INEXISTENCE", 400)
    else:
        taskData = {
            "id": task[0],
            "name": task[1],
            "status": task[2],
            "createtime": task[3],
            "completetime": task[4],
            "progress": task[5],
            "startIP": task[6],
            "endIP": task[7],
            "plugins": json.loads(task[8]),
            "nodeId": task[9],
            "scan_result": task[10] or None
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
    assert len(data["plugins"]) >= 0
    assert data["nodeId"]

    task = Task()
    task.name = data["name"]
    task.startIP = data["startIP"]
    task.endIP = data["endIP"]
    task.plugins = data["plugins"]
    task.nodeId = data["nodeId"]
    task.createtime = int(round(time.time() * 1000))

    getDomainRegistry().TaskRepository().save(task)

    return json.dumps(task.toDict())
