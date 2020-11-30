"""
     Handlers module
"""

from service.activity_service import ActivityService
from service.person_service import PersonService


def delete_person_handler(person_service, activity_service, person_id):
    li_info = person_service.delete_person(person_id)
    return activity_service, li_info


class RedoHandler:
    ADD_PERSON = PersonService.add_person_entity
    DELETE_PERSON = delete_person_handler
    UPDATE_PERSON = PersonService.update_person

    ADD_ACTIVITY = ActivityService.add_activity_entity
    DELETE_ACTIVITY = ActivityService.delete_activity
    UPDATE_ACTIVITY = ActivityService.update_activity
