from uuid import uuid4 as uuid
from enum import Enum
from classes.aescrpyto import AESCrpyto

class Node(object):

    def __init__(self):
        c = AESCrpyto()

        self.id = str(uuid())  # 节点ID
        self.name = ""  # 节点名称
        self.ip = 0  # 节点IP
        self.port = 0  # 节点端口
        self.key = c.getKeyAndNonce()  # 节点的秘钥
        self.lastActiveTime = 0  # 上次活跃时间


class Plugin(object):

    def __init__(self):
        self.id = str(uuid())
        self.name = ""
        self.description = ""
        self.file = b""


class TaskStatus(Enum):
    WAITING = 0
    RUNNING = 1
    COMPLETE = 2


class Task:

    def __init__(self):
        self.id = str(uuid())
        self.name = ""
        self.status = TaskStatus.WAITING
        self.createtime = 0
        self.completetime = 0
        self.progress = 0
        self.startIP = 0
        self.endIP = 0
        self.nodeId = ""
        self.plugins = []
        self.scanResult = None

    def toDict(self):
        data = {}
        data["id"] = self.id
        data["name"] = self.name
        data["status"] = self.status.name
        data["createtime"] = self.createtime
        data["completetime"] = self.completetime
        data["progress"] = self.progress
        data["startIP"] = self.startIP
        data["endIP"] = self.endIP
        data["nodeId"] = self.nodeId
        data["plugins"] = self.nodeId
        if self.scanResult:
            data["scanResult"] = self.scanResult.__dict__

        return data


class ScanResult:

    def __init__(self):
        self.numberOfIPs = 0
        self.numberOfPorts = 0
        self.numberOfWarnings = 0
        self.scanIPResults = []


class ScanIPResult:

    def __init__(self):
        self.ip = 0
        self.numberOfPorts = 0
        self.numberOfWarnings = 0
        self.scanPortResults = []


class ScanPortResult:

    def __init__(self):
        self.port = 0
        self.numberOfWarnings = 0
        self.warnings = []


class ScanWarning:

    def __init__(self):
        self.ip = 0
        self.port = 0
        self.plugin = None
        self.description = ""
