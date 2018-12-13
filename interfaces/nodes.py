from flask import request
import json
from classes import Node
from infrastructure.repositories import getDomainRegistry
from infrastructure.db import Database


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

    sql = "SELECT id, name, ip, port, key, last_activetime FROM nodes ORDER BY last_activetime LIMIT :limit OFFSET :offset"

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
            "ip": node[2],
            "port": node[3],
            "key": node[4],
            "last_activetime": node[5],
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
