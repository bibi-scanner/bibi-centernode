from flask import request
import json
from classes import Node
from infrastructure.repositories import getDomainRegistry
from infrastructure.db import Database

def systemInfo():
    db = Database()
    conn = db.getConn()
    cr = conn.cursor()

    cr.execute("SELECT COUNT(*) as count FROM tasks")
    numberOfTasks = cr.fetchone()["count"]

    cr.execute("SELECT COUNT(*) as count FROM tasks WHERE status = 0")
    numberOfWaitingTasks = cr.fetchone()["count"]

    cr.execute("SELECT COUNT(*) as count FROM tasks WHERE status = 1")
    numberOfRunningTasks = cr.fetchone()["count"]

    cr.execute("SELECT COUNT(*) as count FROM tasks WHERE status = 2")
    numberOfFinishTasks = cr.fetchone()["count"]

    cr.execute("SELECT COUNT(*) as count FROM nodes")
    numberOfNodes = cr.fetchone()["count"]

    cr.execute("SELECT COUNT(*) as count FROM plugins")
    numberOfPlugins = cr.fetchone()["count"]

    data = {
        "numberOfTasks": numberOfTasks,
        "numberOfWaitingTasks": numberOfWaitingTasks,
        "numberOfRunningTasks": numberOfRunningTasks,
        "numberOfFinishTasks": numberOfFinishTasks,
        "numberOfNodes": numberOfNodes,
        "numberOfPlugins": numberOfPlugins,
    }

    cr.close()
    conn.close()

    return json.dumps(data)

