def info():
    info = {}
    info["name"] = "mongodb未授权"
    info["description"] = "检测mongodb未授权访问漏洞"
    return info


def poc(ip, port):
    import pymongo
    try:
        conn = pymongo.MongoClient(ip, port)
        dbname = conn.list_database_names()
        print(ip, "存在MongoDB未授权")
        myCol = conn["site"]
        # conn.close()
        return {
            "info": "存在MongoDB未授权",
            "result": True
        }
    except Exception as e:
        print(e)
    finally:
        conn.close()
    return {
        "info": "不存在MongoDB未授权",
        "result": False
    }
