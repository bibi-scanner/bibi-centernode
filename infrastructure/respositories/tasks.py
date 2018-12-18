from classes import Task, TaskStatus
import json


class TaskRepository:

    def __init__(self, db):
        self.db = db

    def getTaskById(self, id):
        conn = self.db.getConn()
        cr = conn.cursor()
        cr.execute(
            "SELECT id, name, status, createtime, completetime, progress, start_ip, end_ip, node_id, plugins, scan_result FROM tasks WHERE id=%s",
            (id))
        data = cr.fetchone()
        cr.close()
        conn.close()

        try:
            task = Task()
            task.id = data["id"]
            task.name = data["name"]
            task.status = TaskStatus(data["status"])
            task.createtime = data["createtime"]
            task.completetime = data["completetime"]
            task.progress = data["progress"]
            task.startIP = data["start_ip"]
            task.endIP = data["end_ip"]
            task.nodeId = data["node_id"]
            task.plugins = json.loads(data["plugins"] or "[]")
            task.scanResult = json.loads(data["scan_result"] or '""')
        except:
            return None

        return task

    def save(self, task):
        conn = self.db.getConn()
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id=%s", (task.id))
        data = c.fetchone()

        if data:
            c.execute("UPDATE tasks SET "
                      "name=%s,"
                      "status=%s,"
                      "createtime=%s,"
                      "completetime=%s,"
                      "progress=%s,"
                      "start_ip=%s,"
                      "end_ip=%s,"
                      "plugins=%s,"
                      "node_id=%s,"
                      "scan_result=%s"
                      " WHERE id=%s",
                      (task.name, task.status.value, task.createtime, task.completetime, task.progress, task.startIP,
                       task.endIP, json.dumps(task.plugins or []), task.nodeId, json.dumps(task.scanResult or ""), task.id))
        else:
            c.execute(
                "INSERT INTO tasks (id, name, status, createtime, completetime, progress, start_ip, end_ip, node_id, plugins, scan_result)"
                "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)",
                (task.id, task.name, task.status.value, task.createtime, task.completetime, task.progress, task.startIP,
                 task.endIP, task.nodeId, json.dumps(task.plugins), json.dumps(task.scanResult or "")))
        c.close()
        conn.commit()
        conn.close()

        return None
