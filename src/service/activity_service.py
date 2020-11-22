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
        if not self.activity_exists(activity_id):
            raise ActivityValidatorException("The activity that you are trying to update does not exist.")

        activity_update = Activity(person_id, date, time, description)
        activity_update.id = int(activity_id)
        self.__validator.validate(activity_update)
        self.validate_activity(activity_update)
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
                # index = activity.person_id_list.index(person_id)
                if date == activity.date and time == activity.time and person_id in activity.person_id_list:
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

    def activity_exists(self, activity_id):
        li_activities = self.get_all_activities()
        for activity in li_activities:
            if int(activity_id) == activity.id:
                return True
        return False

    def generate_activities(self):
        # Getting ids
        list_persons = self.__person_service.get_all_persons()
        list_ids = [person.id for person in list_persons]
        length_ids = len(list_ids)
        #
        # Getting descriptions
        li_description = ["Footbal", "Golf", "Swimming", "Running", "Writing", "Reading",
                          "Biking", "Driving", "Exercising", "Walking"]
        #

        # # Generating date
        # day = random.randint(1, 28)
        # month = random.randint(1, 12)
        # year = random.randint(1850, 2020)
        # string_date = str(day) + '/' + str(month) + '/' + str(year)

        times = 10
        while times > 0:
            # Generating id
            id_index = random.randint(0, length_ids - 1)

            #
            # Generating time
            hour = random.randint(1, 23)
            minute = random.randint(1, 58)
            hour2 = random.randint(hour, 23)
            minute2 = random.randint(minute + 1, 59)
            string_time = str(hour) + ':' + str(minute) + '-' + str(hour2) + ':' + str(minute2)
            #
            # Generating date
            day = random.randint(1, 28)
            month = random.randint(1, 12)
            year = random.randint(1850, 2020)
            string_date = str(day) + '/' + str(month) + '/' + str(year)
            # Generating description
            index_description = random.randint(0, 9)

            try:
                self.add_activity([list_ids[id_index]], string_date, string_time, li_description[index_description])
                times = times - 1
            except ActivityValidatorException as ex:
                print("Error, " + str(ex))

    def filter_by_date_time(self, date, time):
        # return [activity for activity in self.get_all_activities() if activity.date == date and time in activity.time]
        # print(self.time_in_interval(date, time))
        return [activity for activity in self.get_all_activities() if activity.date == date
                and self.time_in_interval(time, activity.time)]

    def filter_by_description(self, description):
        return [activity for activity in self.get_all_activities()
                if activity.description.lower() == description.lower()]

    def filter_by_date(self, date):
        li_activities = [activity for activity in self.get_all_activities() if activity.date == date]
        li_activities.sort(key=self.my_key)
        return li_activities

    @staticmethod
    def my_key(activity):
        string_time = activity.time.split('-')
        li_words = [int(word) for word in string_time[0].split(':')]
        return li_words

    def filter_by_person(self, person_id):
        li_activities = [activity for activity in self.get_all_activities() if
                         int(person_id) in activity.person_id_list]
        return li_activities

    def create_date_dict(self):
        """
        Creates a dictionary of the type [date]=num_activities, where num_activities = the number
                                                        of activities taking place at a certain date
        :return: the dictionary
        """
        li_activities = self.get_all_activities()
        li_dates = self.create_date_list()
        date_dict = {}

        for date in li_dates:
            num_activities = 0
            for activity in li_activities:
                if activity.date == date:
                    num_activities = self.interval_duration(activity.time)
            date_dict[date] = num_activities

        sorted_dict = sorted(date_dict.items(), key=lambda item: item[1])

        return sorted_dict

    def create_date_list(self):
        """
        Creates a list of all the dates.
        :return: the list
        """
        li_activities = self.get_all_activities()
        li_dates = [activity.date for activity in li_activities]
        li_dates = list(dict.fromkeys(li_dates))  # Removing duplicates
        return li_dates

    @staticmethod
    def interval_duration(interval):
        """
        Returns the number of minutes contained in an interval of the form "11:10-23:15"
        :param interval: the interval
        :return: the nr of minutes
        """
        # 11:10-23:14
        start, end = interval.split('-')  # start = 11:10, end = 23:14
        start_hour, start_minute = [int(word) for word in start.split(':')]
        end_hour, end_minute = [int(word) for word in end.split(':')]

        # print(start_hour, start_minute)
        # print(end_hour, end_minute)
        return (end_hour-start_hour) * 60 + end_minute - start_minute

    @staticmethod
    def time_in_interval(time, interval):
        """
        Checks if a certain time is included within a time interval of the form "11:11-22:22"
        :param time: the time to be checked
        :param interval: the interval
        :return: True if it is included, False otherwise
        """
        # 11:20 <-> 10:10-15:40
        # 11:20 <-> 11:20-20:40
        # 11:20 <-> 10:10-11:20
        # 11:20 <-> 11:19-11:21

        li_time = [int(word) for word in time.split(':')]  # li_time[0] = 11, li_time[1] = 20

        li_interval = interval.split('-')  # li_interval[0] = 10:10, li_interval[1] = 15:40
        li_start = [int(word) for word in li_interval[0].split(':')]  # li_start[0] = 10, li_start[1] = 10
        li_end = [int(word) for word in li_interval[1].split(':')]  # li_end[0] = 15, li_end[1] = 40

        if li_start <= li_time <= li_end:
            return True

        return False

#  TODO list busiest days
