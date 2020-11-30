"""
    Testing module
"""

# Imports
from random import randint

from domain.entity import Activity, Person
from domain.validators import PersonValidator, ActivityValidator, ActivityValidatorException, PersonValidatorException
from repository.inmemoryrepo import Repository
from service.activity_service import ActivityService
from service.person_service import PersonService, PersonServiceException
import unittest


#


class Test(unittest.TestCase):
    person_validator = PersonValidator()
    person_repository = Repository()

    activity_validator = ActivityValidator()
    activity_repository = Repository()

    person_service = PersonService(person_validator, person_repository, activity_repository)
    activity_service = ActivityService(activity_validator, activity_repository, person_service)

    person_service.generate_persons()
    activity_service.generate_activities()

    li_persons = person_service.get_all_persons()
    li_activities = activity_service.get_all_activities()

    # Person

    # Add functionality
    def test_add_person(self):
        self.assertEqual(len(self.li_persons), 5)
        self.person_repository.find_by_id(2)

        self.person_service.add_person("neamtiu ovidiu zaris", "0753429584")
        self.person_service.add_person("phineas norbert")
        self.person_service.add_person("gica Ciobanu", "0742529429")

        self.li_persons = self.person_service.get_all_persons()

        self.assertEqual(len(self.li_persons), 8)

        self.assertEqual(self.li_persons[5].name, "Neamtiu Ovidiu Zaris")
        self.assertEqual(self.li_persons[6].name, "Phineas Norbert")
        self.assertEqual(self.li_persons[7].name, "Gica Ciobanu")

        self.assertEqual(self.li_persons[5].phone_number, "0753429584")
        self.assertEqual(self.li_persons[6].phone_number, "unknown")
        self.assertEqual(self.li_persons[7].phone_number, "0742529429")

        self.assertRaises(PersonValidatorException, self.person_service.add_person, "N3amtiu")
        self.assertRaises(PersonValidatorException, self.person_service.add_person, "Zaris", "02432j45")

    # Remove functionality
    def test_remove_person(self):
        li_activities = self.person_service.delete_person(1)
        self.person_service.delete_person(2)
        self.person_service.delete_person(3)
        self.assertFalse(self.activity_service.person_exists(1), False)
        self.assertFalse(self.activity_service.person_exists(2), False)
        self.assertFalse(self.activity_service.person_exists(3), False)

        self.assertRaises(PersonServiceException, self.person_service.delete_person, 3)

    # Update functionality
    def test_update_person(self):
        self.person_service.update_person(6, "Zaris", "0842578753")
        self.person_service.update_person(7, "Zaris")

        self.li_persons = self.person_service.get_all_persons()

        self.assertEqual(self.li_persons[2].name, "Zaris")
        self.assertEqual(self.li_persons[2].phone_number, "0842578753")
        self.assertEqual(self.li_persons[3].name, "Zaris")
        self.assertEqual(self.li_persons[3].phone_number, "unknown")
        self.assertRaises(PersonServiceException, self.person_service.update_person, 101, "Zaris")

    # Filter by name
    def test_filter_by_name(self):
        li_persons = self.person_service.filter_by_name("Zaris")
        for person in li_persons:
            self.assertIn("Zaris", person.name)

    # Filter by phone number
    def test_filter_by_phone_number(self):
        li_persons = self.person_service.filter_by_phone_number("unknown")
        for person in li_persons:
            self.assertEqual(person.phone_number, "unknown")

    # Activity

    # Add functionality
    def test_add_activity(self):
        self.activity_service.add_activity([1, 2, 3], "1/1/1", "12:20-14:50", "Golf")
        self.assertRaises(ActivityValidatorException, self.activity_service.add_activity, [1], "1/1/1",
                          "13:20-16:00", "a")
        self.activity_service.add_activity([1, 2, 3], "11/11/2011", "11:11-12:11", "asd")
        self.assertRaises(ActivityValidatorException, self.activity_service.add_activity,
                          [10], "11/11/2020", "18:13", "Golf")
        self.assertRaises(ActivityValidatorException, self.activity_service.add_activity,
                          [20], "11/11/2020", "18:13", "Golf")

    # Update functionality
    def test_update_activity(self):
        self.activity_service.add_activity([6, 7, 8], "2/2/2020", "12:20", "Python")
        self.li_activities = self.activity_service.get_all_activities()
        index = len(self.li_activities) - 1
        self.activity_service.update_activity(self.li_activities[index].id, [6, 7],
                                              "1/1/2001", "11:10", "Fotbal")

        self.li_activities = self.activity_service.get_all_activities()

        index = len(self.li_activities) - 1

        self.assertEqual(self.li_activities[index].id, 20)
        self.assertEqual(self.li_activities[index].date, "1/1/2001")
        self.assertEqual(self.li_activities[index].time, "11:10")
        self.assertEqual(self.li_activities[index].person_id_list, [6, 7])
        self.assertEqual(self.li_activities[index].description, "Fotbal")
        self.assertRaises(ActivityValidatorException,
                          self.activity_service.update_activity, 50, [1], "1/1/1", "12:20-13:20", "Running")

    # Validators
    def test_activity_validators(self):
        activity1 = Activity([1], "1/1/1", "131asd", "a")
        activity2 = Activity([1], "1/1a1", "1:1-1:2", "a")
        self.assertRaises(ActivityValidatorException, self.activity_validator.validate, activity1)
        self.assertRaises(ActivityValidatorException, self.activity_validator.validate, activity2)

    # Filter functionality
    def test_filter_by_date_time(self):
        random_index = randint(0, len(self.li_activities) - 1)

        if self.activity_service.activity_exists(self.li_activities[random_index].id):
            random_activity = self.li_activities[random_index]
        else:
            random_activity = self.li_activities[0]

        li_filtered = self.activity_service.filter_by_date_time(random_activity.date, "15:00")

        for activity in li_filtered:
            self.assertEqual(activity.date, random_activity.date)
            self.assertTrue(self.activity_service.time_in_interval("15:00", activity.time))

    def test_filter_by_description(self):
        description = "Reading"
        li_filtered = self.activity_service.filter_by_description(description)

        for activity in li_filtered:
            self.assertEqual(activity.description, description)

    def test_filter_by_date(self):
        random_index = randint(0, len(self.li_activities) - 1)

        date = self.li_activities[random_index].date

        li_filtered = self.activity_service.filter_by_date(date)

        for activity in li_filtered:
            self.assertEqual(activity.date, date)

    def test_filter_by_person(self):
        li_filtered = self.activity_service.filter_by_person(1)

        for activity in li_filtered:
            self.assertIn(1, activity.person_id_list)

    def test_create_busiest_days_list(self):
        list_days = self.activity_service.create_busiest_days_list()

        nr_days = len(list_days)
        for index in range(0, nr_days - 1):
            self.assertLessEqual(list_days[index][1], list_days[index + 1][1])

        self.assertEqual(len(list_days), len(set(list_days)))  # Checking if the list contains duplicates

    # Delete functionality
    def test_delete_activity(self):
        self.activity_service.delete_activity(1)
        self.assertFalse(self.activity_service.activity_exists(1))
        self.assertRaises(ActivityValidatorException, self.activity_service.delete_activity, 50)

    # Add by entity
    def test_add_activity_entity(self):
        a = Activity([1,2,3], "1/1/1", "1:1-1:2", "a")
        self.activity_service.add_activity_entity(a)

    # Entities
    def test_setters_getters(self):
        # Activity
        a1 = Activity([1], "1/1/1", "1:1-1:2", "Golf")
        a1.date = "1/2/1"
        a1.time = "12:20-15:20"
        a1.description = "Reading"
        a1_string = str(a1)

        self.assertEqual(a1.date, "1/2/1")
        self.assertEqual(a1.time, "12:20-15:20")
        self.assertEqual(a1.description, "Reading")

        # Person
        p1 = Person("zaris", "024092234")
        p1.phone_number = "3424212"
        p1_string = str(p1)

        self.assertEqual(p1.phone_number, "3424212")
