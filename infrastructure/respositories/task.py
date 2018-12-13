from classes import Task
import json

class TaskRepository:

    def __init__(self, db):
        self.db = db

    def getTaskByTaskId(self, id):
        return Task()

    def save(self, task):
        conn = self.db.getConn()
        c = conn.cursor()
        data = c.execute("SELECT * FROM tasks WHERE id=:id", {
            "id": task.id
        }).fetchone()

        if data:
            c.execute("UPDATE tasks SET "
                      "name=:name "
                      "status=:status"
                      "createtime=:createtime"
                      "completetime=:completetime"
                      "progress=:progress"
                      "start_ip=:startIP"
                      "end_ip=:endIP"
                      "plugins=:plugins"
                      "node_id=:nodeId"
                      "scan_result=:scanResult"
                      " WHERE id=:id", {
                          "id": task.id,
                          "name": task.name,
                          "status": task.status.value,
                          "createtime": task.createtime,
                          "completetime": task.completetime,
                          "progress": task.progress,
                          "startIP": task.startIP,
                          "endIP": task.endIP,
                          "plugins": json.dumps(task.plugins),
                          "nodeId": task.nodeId,
                          "scanResult": "",
                      })
        else:
            c.execute("INSERT INTO tasks (id, name, status, createtime, completetime, progress, start_ip, end_ip, node_id, plugins, scan_result)"
                      "VALUES (:id, :name, :status, :createtime, :completetime, :progress, :startIP, :endIP, :nodeId, :plugins, :scanResult)", {
                          "id": task.id,
                          "name": task.name,
                          "status": task.status.value,
                          "createtime": task.createtime,
                          "completetime": task.completetime,
                          "progress": task.progress,
                          "startIP": task.startIP,
                          "endIP": task.endIP,
                          "plugins": json.dumps(task.plugins),
                          "nodeId": task.nodeId,
                          "scanResult": "",
                      })
        conn.commit()
        conn.close()

        return None

