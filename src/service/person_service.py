"""
    Services module
"""

# Imports
from domain.entity import Person
#


class PersonService:

    def __init__(self, validator, person_repository):
        self.__validator = validator
        self.__person_repository = person_repository

    def add_person(self, name, phone_number):
        """
        Adds a person.
        :param name: person's name
        :param phone_number: person's phone number
        :return:
        """
        p = Person(name, phone_number)
        self.__validator.validate(p)
        self.__person_repository.save(p)

    def delete_person(self, person_id):
        """
        Deletes a person by an id.
        :param person_id: the person's id
        :return:
        """
        self.__person_repository.delete_by_id(person_id)

    def update_person(self, person_id, person_update):
        """
        Updates the values of the person situated at "person_id" with the values of "person_update"
        :param person_id: the id of the person that is going to be updated
        :param person_update: the object containing the updates
        :return:
        """
        self.__person_repository.update(person_id, person_update)

    def get_all_persons(self):
        """
        Gets all the persons that are currently in the person repository.
        :return: a list of lists containing the information of all the persons in the repository.
        """
        li_persons = []
        for key in self.__person_repository.find_all():
            li_persons.append([key.id, key.name, key.phone_number])
        return li_persons
