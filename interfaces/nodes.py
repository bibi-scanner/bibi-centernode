from flask import request
import json
from classes import Node
from infrastructure.repositories import getDomainRegistry

def createNode():
    data = request.data
    data = json.loads(data)
    assert data["name"]

    node = Node()
    node.name = data["name"]

    getDomainRegistry().NodeRepository().save(node)

    return json.dumps(node.__dict__)