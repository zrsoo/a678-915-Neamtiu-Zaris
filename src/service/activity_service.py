"""
    Activity service module
"""

# Imports
from domain.entity import Activity
from domain.validators import ActivityValidatorException
import random


#


class ActivityService:
    def __init__(self, validator, activity_repository, person_service):
        self.__validator = validator
        self.__activity_repository = activity_repository
        self.__person_service = person_service

    def add_activity(self, person_id, date, time, description):
        """
        Adds an activity.
        :param person_id: the id of the person performing the activity
        :param date: the date when the activity is performed
        :param time: the time when the activity is performed
        :param description: description of the activity
        :return:
        """
        a = Activity(person_id, date, time, description)
        self.__validator.validate(a)
        self.validate_activity(a)
        self.__activity_repository.save(a)

    def delete_activity(self, activity_id):
        """
        Deletes the activity by id.
        :param activity_id: the id of the activity that is to be deleted
        :return:
        """
        self.__activity_repository.delete_by_id(activity_id)

    def update_activity(self, activity_id, person_id, date, time, description):
        """
        Updates the activity with the provided id with the new values.
        :param description: the new description
        :param time: the new time
        :param date: the new date
        :param person_id: the new list of person_id's
        :param activity_id: the id of the activity that is going to be updated
        :return:
        """
        activity_update = Activity(person_id, date, time, description)
        activity_update.id = activity_id
        self.__activity_repository.update(activity_id, activity_update)

    def get_all_activities(self):
        """
        Gets all the activities that are currently in the activity repository.
        :return: a list of lists containing the information of all the activities
        """
        li_activities = []
        for key in self.__activity_repository.find_all():
            li_activities.append(key)
        return li_activities

    def person_exists(self, person_id):
        """
        Checks if the person id that is assigned to the activity exists in the person repository.
        :param person_id: the id that is checked
        :return: true if the person exists, false otherwise
        """
        li_persons = self.__person_service.get_all_persons()
        # print(person_from_list for person_from_list in li_persons)
        return any(person_id == person_from_list.id for person_from_list in li_persons)

    def person_busy(self, person_id, date, time):
        """
        Checks if the person with the corresponding id is busy at a certain date and time.
        :param person_id: the person's id
        :param date: the date that is being checked
        :param time: the time that is being checked
        :return: true if the person is busy, false otherwise
        """
        li_activities = self.get_all_activities()
        for activity in li_activities:
            try:
                index = activity.person_id_list.index(person_id)
                if date == activity.date and time == activity.time:
                    return True
            except ValueError:
                pass
        return False

    def validate_activity(self, activity):
        # Checking if the persons performing the activities exist.
        for person_id in activity.person_id_list:
            if not self.person_exists(person_id):
                raise ActivityValidatorException("The person with id " + str(person_id) +
                                                 " that you are trying to assign "
                                                 "to the activity with id " + str(activity.id) + " does not exist.")

        # Checking if the persons performing the activities are busy.
        for person_id in activity.person_id_list:
            if self.person_busy(person_id, activity.date, activity.time):
                raise ActivityValidatorException("The person with id " + str(person_id) +
                                                 " that you are trying to assign "
                                                 "to the activity with id " + str(activity.id) + " is busy.")

    def generate_activities(self):
        # Getting ids
        list_persons = self.__person_service.get_all_persons()
        list_ids = [person.id for person in list_persons]
        length_ids = len(list_ids)
        id_index = random.randint(0, length_ids - 1)
        #
        # Getting descriptions
        li_description = ["Footbal", "Golf", "Swimming", "Running", "Writing", "Reading",
                          "Biking", "Driving", "Exercising", "Walking"]
        #

        times = 5
        while times > 0:
            # Generating id
            id_index = random.randint(0, length_ids - 1)
            # Generating date
            day = random.randint(1, 28)
            month = random.randint(1, 12)
            year = random.randint(1850, 2020)
            string_date = str(day) + '/' + str(month) + '/' + str(year)
            #
            # Generating time
            hour = random.randint(1, 23)
            minute = random.randint(1, 59)
            string_time = str(hour) + ':' + str(minute)
            #
            # Generating description
            index_description = random.randint(0, 9)

            try:
                self.add_activity([list_ids[id_index]], string_date, string_time, li_description[index_description])
                times = times - 1
            except ActivityValidatorException as ex:
                print("Error, " + str(ex))
