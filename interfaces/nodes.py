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


def queryNodes():
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

    sql = "SELECT id, name, active, ip, port, key, last_activetime FROM nodes ORDER BY last_activetime DESC LIMIT :limit OFFSET :offset"

    nodes = conn.execute(sql, {
        "offset": offset,
        "limit": limit
    }).fetchall()
    totalNumber = conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]

    datas = []
    for node in nodes:
        datas.append({
            "id": node[0],
            "name": node[1],
            "active": node[2],
            "ip": node[3],
            "port": node[4],
            "key": node[5],
            "lastActivetime": node[6],
        })

    conn.close()

    return json.dumps({
        "nodes": datas,
        "totalNumber": totalNumber
    })


def createNode():
    data = request.data
    data = json.loads(data)
    assert data["name"]

    node = Node()
    node.name = data["name"]

    getDomainRegistry().NodeRepository().save(node)

    return json.dumps(node.__dict__)


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
