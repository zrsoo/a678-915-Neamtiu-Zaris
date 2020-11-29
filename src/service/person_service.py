"""
    Person service module
"""

# Imports
from domain.entity import Person
import random
import string
import copy


#


class StoreException(Exception):
    pass


class PersonServiceException(StoreException):
    pass


class PersonService:

    def __init__(self, validator, person_repository, activity_repository):
        self.__validator = validator
        self.__person_repository = person_repository
        self.__activity_repository = activity_repository

    def add_person(self, name, phone_number="unknown"):
        """
        Adds a person.
        :param name: person's name
        :param phone_number: person's phone number
        :return:
        """
        p = Person(name, phone_number)
        self.__validator.validate(p)
        self.__person_repository.save(p)
        return p.id

    def add_person_entity(self, p):
        self.__validator.validate(p)
        self.__person_repository.save(p)

    def delete_person(self, person_id):
        """
        Deletes a person by an id.
        :param person_id: the person's id
        :return:
        """
        if not self.person_exists(person_id):
            raise PersonServiceException("The person that you are trying to remove does not exist.")
        person = self.__person_repository.find_by_id(person_id)
        self.__person_repository.delete_by_id(person_id)

        li_activities_to_be_removed = []
        li_affected_activities = []
        li_activities = self.__activity_repository.find_all()

        for activity in li_activities:
            if person_id in activity.person_id_list:
                activity_copy = copy.deepcopy(activity)
                li_affected_activities.append(activity_copy)
                activity.person_id_list.remove(person_id)
                if len(activity.person_id_list) == 0:
                    li_activities_to_be_removed.append(activity_copy)

        li_info = [li_activities_to_be_removed, li_affected_activities, person]

        for activity in li_activities_to_be_removed:
            self.__activity_repository.delete_by_id(activity.id)

        return li_info

    def update_person(self, person_id, name, phone_number="unknown"):
        """
        Updates the values of the person situated at "person_id" with the values of "person_update"
        :param phone_number: the new phone number
        :param name: the new name
        :param person_id: the id of the person that is going to be updated
        :return:
        """
        if not self.person_exists(person_id):
            raise PersonServiceException("The person that you are trying to update does not exist.")

        person_update = Person(name, phone_number)
        person_update.id = person_id
        self.__validator.validate(person_update)
        self.__person_repository.update(person_id, person_update)

    def get_all_persons(self):
        """
        Gets all the persons that are currently in the person repository.
        :return: a list of lists containing the information of all the persons in the repository.
        """
        li_persons = []
        for key in self.__person_repository.find_all():
            # li_persons.append([key.id, key.name, key.phone_number])
            li_persons.append(key)
        return li_persons

    def generate_persons(self):
        list_names = ["Ion Pop Glanetasu", "Apolodor", "Kaz Brekker", "Cahir Aep Ceallach",
                      "Dinu Paturica", "Francesca Findabair", "Triss Merigold", "Dijkstra",
                      "Ragnar Lothbrok", "Obi-Wan Kenobi"]

        times = 5
        minus = 0
        while times > 0:
            name_index = random.randint(0, 9 - minus)
            digits = string.digits
            phone_number = ''.join(random.choice(digits) for i in range(10))
            self.add_person(list_names[name_index], phone_number)
            list_names.pop(name_index)
            minus = minus + 1
            times = times - 1

    def filter_by_name(self, name):
        return [person for person in self.get_all_persons() if name.lower() in person.name.lower()]

    def filter_by_phone_number(self, phone_number):
        return [person for person in self.get_all_persons() if phone_number in person.phone_number]

    def person_exists(self, person_id):
        """
        Checks if the person id that is assigned to the activity exists in the person repository.
        :param person_id: the id that is checked
        :return: true if the person exists, false otherwise
        """
        li_persons = self.__person_repository.find_all()
        # print(person_from_list for person_from_list in li_persons)
        return any(person_id == person_from_list.id for person_from_list in li_persons)

    def filter_by_id(self, person_id):
        return self.__person_repository.find_by_id(person_id)
