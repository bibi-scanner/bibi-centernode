from classes import Plugin
import json


class PluginsRepository:

    def __init__(self, db):
        self.db = db

    def save(self, plugin):
        conn = self.db.getConn()
        c = conn.cursor()
        c.execute("SELECT * FROM plugins WHERE id=%s", (plugin.id))
        data = c.fetchone()

        if data:
            c.execute("UPDATE plugins SET "
                      "name=%s "
                      "description=%s"
                      "file=%s"
                      " WHERE id=%s", (plugin.name, plugin.description, plugin.file, plugin.id))
        else:
            c.execute("INSERT INTO plugins (id, name, description, file)"
                      "VALUES (%s, %s, %s, %s)", (plugin.id, plugin.name, plugin.description, plugin.file))
        c.close()
        conn.commit()
        conn.close()

        return True
