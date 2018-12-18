from classes import Node
import json


class NodeRepository:

    def __init__(self, db):
        self.db = db

    def getNodeById(self, id):
        conn = self.db.getConn()
        c = conn.cursor()

        c.execute("SELECT id, name, active, ip, port, `key`, last_activetime as lastActiveTime FROM nodes WHERE id=%s", (id))
        data = c.fetchone()

        c.close()
        conn.close()

        try:
            node = Node()
            node.id = data["id"]
            node.name = data["name"]
            node.active = data["active"]
            node.ip = data["ip"]
            node.port = data["port"]
            node.key = data["key"]
            node.lastActiveTime = data["lastActiveTime"]
        except:
            return None

        return node

    def save(self, node):
        conn = self.db.getConn()
        c = conn.cursor()
        c.execute("SELECT * FROM nodes WHERE id=%s", (node.id))
        data = c.fetchone()

        if data:
            c.execute("UPDATE nodes SET "
                      "name=%s,"
                      "active=%s,"
                      "ip=%s,"
                      "port=%s,"
                      "`key`=%s,"
                      "last_activetime=%s"
                      " WHERE id=%s",
                      (node.name, node.active, node.ip, node.port, node.key, node.lastActiveTime, node.id))
        else:
            c.execute("INSERT INTO nodes (id, name, active, ip, port, `key`, last_activetime) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                      (node.id, node.name, node.active, node.ip, node.port, node.key ,node.lastActiveTime))

        conn.commit()
        c.close()
        conn.close()

        return None
