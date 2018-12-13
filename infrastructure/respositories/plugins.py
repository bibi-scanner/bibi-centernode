from classes import Plugin
import json

class PluginsRepository:

    def __init__(self, db):
        self.db = db

    def save(self, plugin):
        conn = self.db.getConn()
        c = conn.cursor()
        data = c.execute("SELECT * FROM plugins WHERE id=:id", {
            "id": plugin.id
        }).fetchone()

        if data:
            c.execute("UPDATE plugins SET "
                      "name=:name "
                      "description=:description"
                      "file=:file"
                      " WHERE id=:id", {
                          "id": plugin.id,
                          "name": plugin.name,
                          "description": plugin.description,
                          "file": plugin.file,
                      })
        else:
            c.execute("INSERT INTO plugins (id, name, description, file)"
                      "VALUES (:id, :name, :description, :file)", {
                          "id": plugin.id,
                          "name": plugin.name,
                          "description": plugin.description,
                          "file": plugin.file,
                      })
        conn.commit()
        conn.close()

        return True

