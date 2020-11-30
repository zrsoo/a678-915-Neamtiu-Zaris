"""
    Undo module
"""

from dataclasses import dataclass

from service.redo_handlers import RedoHandler
from service.undo_handlers import UndoHandler


class StoreException(Exception):
    pass


class CommandManagerException(StoreException):
    pass


@dataclass()
class Operation:
    target_object: object
    handler: object
    args: tuple


class CommandManager:
    __undo_operations = []
    __redo_operations = []

    @staticmethod
    def register_undo_operation(target_object, handler, *args):
        CommandManager.__undo_operations.append(Operation(target_object, handler, args))

    @staticmethod
    def register_redo_operation(target_object, handler, *args):
        CommandManager.__redo_operations.append(Operation(target_object, handler, args))

    @staticmethod
    def undo():
        if len(CommandManager.__undo_operations) == 0:
            raise CommandManagerException("There are no more operations left to undo.")

        undo_operation = CommandManager.__undo_operations.pop()
        redo_args = undo_operation.handler(undo_operation.target_object, *undo_operation.args)

        if undo_operation.handler == UndoHandler.ADD_PERSON:
            CommandManager.register_redo_operation(undo_operation.target_object, RedoHandler.ADD_PERSON, redo_args)
        elif undo_operation.handler == UndoHandler.DELETE_PERSON:
            CommandManager.register_redo_operation(undo_operation.target_object, RedoHandler.DELETE_PERSON, *redo_args)
        elif undo_operation.handler == UndoHandler.UPDATE_PERSON:
            CommandManager.register_redo_operation(undo_operation.target_object, RedoHandler.UPDATE_PERSON, *redo_args)
        elif undo_operation.handler == UndoHandler.ADD_ACTIVITY:
            CommandManager.register_redo_operation(undo_operation.target_object, RedoHandler.ADD_ACTIVITY, redo_args)
        elif undo_operation.handler == UndoHandler.DELETE_ACTIVITY:
            CommandManager.register_redo_operation(undo_operation.target_object, RedoHandler.DELETE_ACTIVITY, redo_args)
        elif undo_operation.handler == UndoHandler.UPDATE_ACTIVITY:
            CommandManager.register_redo_operation(undo_operation.target_object, RedoHandler.UPDATE_ACTIVITY, *redo_args)

    @staticmethod
    def redo():
        if len(CommandManager.__redo_operations) == 0:
            raise CommandManagerException("There are no more operations left to redo.")

        redo_operation = CommandManager.__redo_operations.pop()
        undo_args = redo_operation.handler(redo_operation.target_object, *redo_operation.args)

        if redo_operation.handler == RedoHandler.ADD_PERSON:
            CommandManager.register_undo_operation(redo_operation.target_object, UndoHandler.ADD_PERSON, undo_args)
        elif redo_operation.handler == RedoHandler.DELETE_PERSON:
            CommandManager.register_undo_operation(redo_operation.target_object, UndoHandler.DELETE_PERSON, *undo_args)
        elif redo_operation.handler == RedoHandler.UPDATE_PERSON:
            CommandManager.register_undo_operation(redo_operation.target_object, UndoHandler.UPDATE_PERSON, undo_args)
        elif redo_operation.handler == RedoHandler.ADD_ACTIVITY:
            CommandManager.register_undo_operation(redo_operation.target_object, UndoHandler.ADD_ACTIVITY, undo_args)
        elif redo_operation.handler == RedoHandler.DELETE_ACTIVITY:
            CommandManager.register_undo_operation(redo_operation.target_object, UndoHandler.DELETE_ACTIVITY, undo_args)
        elif redo_operation.handler == RedoHandler.UPDATE_ACTIVITY:
            CommandManager.register_undo_operation(redo_operation.target_object, UndoHandler.UPDATE_ACTIVITY, undo_args)

