"""
    Handlers module
"""


# Person


def add_person_handler(person_service, person_id):
    person = person_service.filter_by_id(person_id)
    person_service.delete_person(person_id)
    return person


def delete_person_handler(person_service, activity_service, li_info):
    li_activities_to_be_removed = li_info[0]
    li_affected_activities = li_info[1]
    person = li_info[2]

    person_service.add_person_entity(person)

    for activity in li_affected_activities:
        if activity in li_activities_to_be_removed:
            activity_service.add_activity_entity(activity)
        else:
            activity_service.update_activity(activity.id, activity.person_id_list, activity.date,
                                             activity.time, activity.description)
    return activity_service, person.id


def update_person_handler(person_service, person):
    person_return = person_service.update_person(person.id, person.name, person.phone_number)
    return person.id, person_return.name, person_return.phone_number


#


# Activity


def add_activity_handler(activity_service, activity_id):
    activity = activity_service.filter_by_id(activity_id)
    activity_service.delete_activity(activity_id)
    return activity


def delete_activity_handler(activity_service, activity):
    activity_service.add_activity_entity(activity)
    return activity.id


def update_activity_handler(activity_service, activity):
    activity_old = activity_service.update_activity(activity.id, activity.person_id_list, activity.date, activity.time,
                                                    activity.description)
    return activity.id, activity_old.person_id_list, activity_old.date, activity_old.time, activity_old.description


#


class UndoHandler:
    ADD_PERSON = add_person_handler
    DELETE_PERSON = delete_person_handler
    UPDATE_PERSON = update_person_handler

    ADD_ACTIVITY = add_activity_handler
    DELETE_ACTIVITY = delete_activity_handler
    UPDATE_ACTIVITY = update_activity_handler
