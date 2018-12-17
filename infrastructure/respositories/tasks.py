from classes import Task, TaskStatus
import json

class TaskRepository:

    def __init__(self, db):
        self.db = db

    def getTaskById(self, id):
        conn = self.db.getConn()
        data = conn.execute("SELECT id, name, status, createtime, completetime, progress, start_ip, end_ip, node_id, plugins, scan_result FROM tasks WHERE id=:id", {
            "id": id
        }).fetchone()
        conn.close()

        try:
            task = Task()
            task.id = data[0]
            task.name = data[1]
            task.status = TaskStatus(data[2])
            task.createtime = data[3]
            task.completetime = data[4]
            task.progress = data[5]
            task.startIP = data[6]
            task.endIP = data[7]
            task.nodeId = data[8]
            task.plugins = data[9]
            task.scanResult = json.loads(data[10] or '""')
        except:
            return None

        return task

    def save(self, task):
        conn = self.db.getConn()
        c = conn.cursor()
        data = c.execute("SELECT * FROM tasks WHERE id=:id", {
            "id": task.id
        }).fetchone()

        if data:
            c.execute("UPDATE tasks SET "
                      "name=:name,"
                      "status=:status,"
                      "createtime=:createtime,"
                      "completetime=:completetime,"
                      "progress=:progress,"
                      "start_ip=:startIP,"
                      "end_ip=:endIP,"
                      "plugins=:plugins,"
                      "node_id=:nodeId,"
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
                          "scanResult": json.dumps(task.scanResult or ""),
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
                          "scanResult": json.dumps(task.scanResult or ""),
                      })
        conn.commit()
        conn.close()

        return None

