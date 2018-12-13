from flask import request
import json
from classes import Plugin
from infrastructure.db import Database
from infrastructure.repositories import getDomainRegistry
from os import path
import os
import importlib

pluginsdir = path.abspath(path.join(path.dirname(__file__), "../plugins"))


def queryPlugins():
    db = Database()
    conn = db.getConn()

    try:
        offset = int(request.args["offset"]) or 0
    except:
        offset = 0

    try:
        limit = int(request.args["limit"]) or 10
    except:
        limit = 10

    sql = "SELECT id, name, description FROM plugins LIMIT :limit OFFSET :offset"

    plugins = conn.execute(sql, {
        "offset": offset,
        "limit": limit
    }).fetchall()
    totalNumber = conn.execute("SELECT COUNT(*) FROM plugins").fetchone()[0]

    datas = []
    for plugin in plugins:
        datas.append({
            "id": plugin[0],
            "name": plugin[1],
            "description": plugin[2]
        })

    conn.close()

    return json.dumps({
        "plugins": datas,
        "totalNumber": totalNumber
    })


def uploadPlugin():
    pluginfile = request.files["plugin"]
    data = pluginfile.read()

    plugin = Plugin()

    pluginfile.save(path.join(pluginsdir, plugin.id + ".py"))
    f = open(path.join(pluginsdir, plugin.id + ".py"), "w", encoding="utf-8")
    f.write(data.decode())
    f.close()

    error = 0
    try:
        moudle = importlib.import_module("plugins." + plugin.id)
        info = moudle.info()
        plugin.name = info["name"]
        plugin.description = info["description"]
        plugin.file = data
    except:
        error = 1
    finally:
        os.remove(path.join(pluginsdir, plugin.id + ".py"))

    if error:
        return ("UPLOAD_ERROR", 400)

    getDomainRegistry().PluginsRepository().save(plugin)

    return json.dumps({
        "plugin": {
            "id": plugin.id,
            "name": plugin.name,
            "description": plugin.description
        }
    })
