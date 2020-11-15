"""
    Person service module
"""

# Imports
from domain.entity import Person
import random

#


class PersonService:

    def __init__(self, validator, person_repository):
        self.__validator = validator
        self.__person_repository = person_repository

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

    def delete_person(self, person_id):
        """
        Deletes a person by an id.
        :param person_id: the person's id
        :return:
        """
        self.__person_repository.delete_by_id(person_id)

    def update_person(self, person_id, name, phone_number="unkown"):
        """
        Updates the values of the person situated at "person_id" with the values of "person_update"
        :param phone_number: the new phone number
        :param name: the new name
        :param person_id: the id of the person that is going to be updated
        :return:
        """
        person_update = Person(name, phone_number)
        person_update.id = person_id
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
        list_phone_numbers = ["unknown", "+40257936226", "+40257456245", "+40257474812",
                              "+48425456245", "+40257452893", "+40257456762", "+4027816952",
                              "+40257461458", "+40257821654"]
        times = 5
        minus = 0
        while times > 0:
            name_index = random.randint(0, 9 - minus)
            phone_number_index = random.randint(0, 9 - minus)
            self.add_person(list_names[name_index], list_phone_numbers[phone_number_index])
            list_names.pop(name_index)
            list_phone_numbers.pop(phone_number_index)
            minus = minus + 1
            times = times - 1
