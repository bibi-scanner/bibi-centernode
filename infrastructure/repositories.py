from infrastructure.db import Database
from infrastructure.respositories.tasks import TaskRepository
from infrastructure.respositories.nodes import NodeRepository


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
