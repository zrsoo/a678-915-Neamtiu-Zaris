"""
     Handlers module
"""
from service.undo_handlers import delete_person_handler, add_person_handler, update_person_handler, \
    delete_activity_handler, update_activity_handler, add_activity_handler


class RedoHandler:
    ADD_PERSON = add_person_handler
    DELETE_PERSON = delete_person_handler
    UPDATE_PERSON = update_person_handler

    ADD_ACTIVITY = add_activity_handler
    DELETE_ACTIVITY = delete_activity_handler
    UPDATE_ACTIVITY = update_activity_handler
