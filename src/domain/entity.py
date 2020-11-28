"""
Entities package
"""

# Imports
import itertools
#


class Person:
    """
        The person class
    """

    # id - unique
    identification = itertools.count(1)
    #

    def __init__(self, name, phone_number):
        self.__name = name
        self.__phone_number = phone_number
        self.__id = next(self.identification)

    # Getters, setters

    @property
    def name(self):
        return self.__name

    @property
    def phone_number(self):
        return self.__phone_number

    @property
    def id(self):
        return self.__id

    @name.setter
    def name(self, name):
        self.__name = name

    @phone_number.setter
    def phone_number(self, phone_number):
        self.__phone_number = phone_number

    @id.setter
    def id(self, id):
        self.__id = id

    # To str overload

    def __str__(self) -> str:
        return str(self.__id) + ".) " + self.name + "; " + self.phone_number


class Activity:
    """
        The activity class
    """

    # id - unique
    identification = itertools.count(1)
    #

    # List of person id's (contains the list of persons that perform the activity)
    # __li_persons = []

    def __init__(self, person_id, date, time, description):
        # self.__li_persons = []
        self.__id = next(self.identification)

        self.__li_persons = person_id
        self.__date = date
        self.__time = time
        self.__description = description

    # Getters, setters

    @property
    def id(self):
        return self.__id

    @property
    def person_id_list(self):
        return self.__li_persons

    @property
    def date(self):
        return self.__date

    @property
    def time(self):
        return self.__time

    @property
    def description(self):
        return self.__description

    @date.setter
    def date(self, date):
        self.__date = date

    @time.setter
    def time(self, time):
        self.__time = time

    @description.setter
    def description(self, description):
        self.__description = description

    @id.setter
    def id(self, id):
        self.__id = id

    # To str overload

    def __str__(self) -> str:
        return str(self.__id) + ".) " + "Personal Id's: " + str(self.person_id_list) + "; "\
               + self.date + "; " + self.time + "; " + self.description


# class Date:
#     def __init__(self, date, num_activities):
#         self.__date = date
#         self.__num_activities = num_activities
#
#     @property
#     def date(self):
#         return self.__date
#
#     @property
#     def num_activities(self):
#         return self.num_activities
