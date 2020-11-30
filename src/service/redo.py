"""
    Redo module
"""

from dataclasses import dataclass


class StoreException(Exception):
    pass


class RedoManagerException(StoreException):
    pass


@dataclass()
class RedoOperation:
    target_object: object
    handler: object
    args: tuple


class RedoManager:
    __redo_operations = []

    @staticmethod
    def register_operation(target_object, handler, *args):
        RedoManager.__redo_operations.append(RedoOperation(target_object, handler, args))

    @staticmethod
    def redo():
        if len(RedoManager.__redo_operations) == 0:
            raise RedoManagerException("There are no more operations left to redo.")

        redo_operation = RedoManager.__redo_operations.pop()
        redo_operation.handler(redo_operation.target_object, *redo_operation.args)
