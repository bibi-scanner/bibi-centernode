from flask import request
import json
from classes import Task
from infrastructure.repositories import getDomainRegistry


def crateTask():
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

    getDomainRegistry().TaskRepository().save(task)

    return json.dumps(task.toDict())
