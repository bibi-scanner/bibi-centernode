from infrastructure.db import Database
from infrastructure.respositories.task import TaskRepository
from infrastructure.respositories.node import NodeRepository


class DomainRegistry:

    def __init__(self):
        self.db = Database()

    def TaskRepository(self):
        return TaskRepository(db=self.db)

    def NodeRepository(self):
        return NodeRepository(db=self.db)


domainRegistry = DomainRegistry()


def getDomainRegistry():
    return domainRegistry
