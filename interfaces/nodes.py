from flask import request
import requests
import json
from classes import Node
from infrastructure.repositories import getDomainRegistry
from infrastructure.db import Database
from classes.aescrpyto import AESCrpyto
import classes.ip2address
import socket
import time

def createNode():
    data = request.data
    data = json.loads(data)
    assert data["name"]

    node = Node()
    node.name = data["name"]

    getDomainRegistry().NodeRepository().save(node)

    return json.dumps(node.__dict__)

def queryNodes():
    try:
        offset = int(request.args["offset"]) or 0
    except:
        offset = 0

    try:
        limit = int(request.args["limit"]) or 10
    except:
        limit = 10

    db = Database()
    conn = db.getConn()
    c = conn.cursor()

    c.execute(
        "SELECT id, name, active, ip, port, `key`, last_activetime as lastActivetime FROM nodes ORDER BY last_activetime DESC LIMIT %s OFFSET %s",
        (limit, offset))
    nodes = c.fetchall()

    c.execute("SELECT COUNT(*) as count FROM nodes")
    totalNumber = c.fetchone()["count"]

    c.close()
    conn.close()

    return json.dumps({
        "nodes": nodes,
        "totalNumber": totalNumber
    })

def getNodeTasks(nodeId):
    db = Database()
    conn = db.getConn()
    cr = conn.cursor()

    cr.execute("SELECT id, status, start_ip as startIP, end_ip as endIP, start_port as startPort, end_port as endPort, plugins FROM tasks WHERE node_id = %s", (nodeId))
    tasks = cr.fetchall()

    cr.close()
    conn.close()

    for task in tasks:
        task["plugins"] = json.loads(task["plugins"])

    return json.dumps({
        "tasks": tasks
    })

def updateNodeTasks(nodeId):
    node = getDomainRegistry().NodeRepository().getNodeById(nodeId)

    if not node:
        return "NULL_NODE", 400

    node.updateNodeTasks()

    return "123"

def registryNode():
    data = request.data
    data = json.loads(data)

    node = getDomainRegistry().NodeRepository().getNodeById(data["id"])

    if not node:
        return "NULL NODE", 400

    try:
        r = requests.post("http://" + data["ip"] + ":" + str(data["port"]) + "/ping")
        node.active = 1
        node.ip = classes.ip2address.ip2long(data["ip"])
        node.port = data["port"]
        node.lastActiveTime = int(round(time.time() * 1000))
    except:
        node.active = 0


    getDomainRegistry().NodeRepository().save(node)

    return "ok"


def pingNode(nodeId):
    node = getDomainRegistry().NodeRepository().getNodeById(nodeId)

    if not node:
        return "NULL NODE", 400

    if not node.ip:
        return "NULL IP", 400

    try:
        r = requests.post("http://" + classes.ip2address.long2ip(node.ip) + ":" + str(node.port) + "/ping")
        node.lastActiveTime = int(round(time.time() * 1000))
        node.active = 1
    except:
        node.active = 0

    getDomainRegistry().NodeRepository().save(node)

    if node.active:
        return json.dumps({
            "active": node.active,
            "lastActivetime": node.lastActiveTime
        })
    else:
        return "NOT_ACTIVE", 400
