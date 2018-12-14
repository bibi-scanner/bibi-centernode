from classes import Node
import json

class NodeRepository:

    def __init__(self, db):
        self.db = db

    def getNodeById(self, id):
        conn = self.db.getConn()
        data = conn.execute("SELECT id, name, ip, port, key, last_activetime FROM nodes WHERE id=:id", {
            "id": id
        }).fetchone()

        try:
            node = Node()
            node.id = data[0]
            node.name = data[1]
            node.ip = data[2]
            node.port = data[3]
            node.key = data[4]
            node.last_activetime = data[5]
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
                      "port=:port,"
                      "key=:key,"
                      "last_activetime=:lastActiveTime"
                      " WHERE id=:id", {
                          "id": node.id,
                          "name": node.name,
                          "ip": node.ip,
                          "port": node.port,
                          "key": node.key,
                          "lastActiveTime": node.lastActiveTime
                      })
        else:
            c.execute("INSERT INTO nodes (id, name, ip, port, key, last_activetime)"
                      "VALUES (:id, :name, :ip, :port, :key, :lastActiveTime)", {
                          "id": node.id,
                          "name": node.name,
                          "ip": node.ip,
                          "port": node.port,
                          "key": node.key,
                          "lastActiveTime": node.lastActiveTime
                      })
        conn.commit()
        conn.close()

        return None

