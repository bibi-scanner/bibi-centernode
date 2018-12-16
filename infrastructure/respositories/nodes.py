from classes import Node
import json

class NodeRepository:

    def __init__(self, db):
        self.db = db

    def getNodeById(self, id):
        conn = self.db.getConn()
        data = conn.execute("SELECT id, name, active, ip, port, key, last_activetime FROM nodes WHERE id=:id", {
            "id": id
        }).fetchone()

        try:
            node = Node()
            node.id = data[0]
            node.name = data[1]
            node.active = data[2]
            node.ip = data[3]
            node.port = data[4]
            node.key = data[5]
            node.last_activetime = data[6]
        except:
            return None

        return node


    def save(self, node):
        conn = self.db.getConn()
        c = conn.cursor()
        data = c.execute("SELECT * FROM nodes WHERE id=:id", {
            "id": node.id
        }).fetchone()

        if data:
            c.execute("UPDATE nodes SET "
                      "name=:name,"
                      "ip=:ip,"
                      "active=:active,"
                      "port=:port,"
                      "key=:key,"
                      "last_activetime=:lastActiveTime"
                      " WHERE id=:id", {
                          "id": node.id,
                          "name": node.name,
                          "active": node.active,
                          "ip": node.ip,
                          "port": node.port,
                          "key": node.key,
                          "lastActiveTime": node.lastActiveTime
                      })
        else:
            c.execute("INSERT INTO nodes (id, name, active, ip, port, key, last_activetime)"
                      "VALUES (:id, :name, :active, :ip, :port, :key, :lastActiveTime)", {
                          "id": node.id,
                          "name": node.name,
                          "active": node.active,
                          "ip": node.ip,
                          "port": node.port,
                          "key": node.key,
                          "lastActiveTime": node.lastActiveTime
                      })
        conn.commit()
        conn.close()

        return None

