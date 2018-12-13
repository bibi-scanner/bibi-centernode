from flask import request
import json
from classes import Node
from infrastructure.repositories import getDomainRegistry
from infrastructure.db import Database

def systemInfo():
    db = Database()
    conn = db.getConn()

    numberOfTasks = conn.execute("SELECT COUNT(*) as count FROM tasks").fetchone()[0]
    numberOfWaitingTasks = conn.execute("SELECT COUNT(*) as count FROM tasks WHERE status = 0").fetchone()[0]
    numberOfRunningTasks = conn.execute("SELECT COUNT(*) as count FROM tasks WHERE status = 1").fetchone()[0]
    numberOfFinishTasks = conn.execute("SELECT COUNT(*) as count FROM tasks WHERE status = 2").fetchone()[0]
    numberOfNodes = conn.execute("SELECT COUNT(*) as count FROM nodes").fetchone()[0]
    numberOfPlugins = conn.execute("SELECT COUNT(*) as count FROM plugins").fetchone()[0]
    data = {
        "numberOfTasks": numberOfTasks,
        "numberOfWaitingTasks": numberOfWaitingTasks,
        "numberOfRunningTasks": numberOfRunningTasks,
        "numberOfFinishTasks": numberOfFinishTasks,
        "numberOfNodes": numberOfNodes,
        "numberOfPlugins": numberOfPlugins,
    }

    conn.close()

    return json.dumps(data)

