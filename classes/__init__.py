from uuid import uuid4 as uuid


class Node(object):

    def __init__(self):
        self.id = uuid()
        self.ip = 0
        self.port = 0
        self.key = "123"
        self.lastActiveTime = 0


class Plugin(object):

    def __init__(self):
        self.id = uuid()
