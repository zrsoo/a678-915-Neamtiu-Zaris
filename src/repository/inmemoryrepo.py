"""
    Repository module
"""


class Repository:
    def __init__(self):
        self.__entities = {}

    def find_by_id(self, entity_id):
        pass

    def save(self, entity):
        self.__entities[entity.id] = entity

    def delete_by_id(self, entity_id):
        self.__entities.pop(entity_id)

    def update(self, entity_id, entity):
        self.__entities[entity_id] = entity

    def find_all(self):
        return self.__entities.values()
