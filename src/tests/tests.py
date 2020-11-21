"""
    Testing module
"""

# Imports
from domain.entity import Activity
from domain.validators import PersonValidator, ActivityValidator, ActivityValidatorException, PersonValidatorException
from repository.inmemoryrepo import Repository
from service.activity_service import ActivityService
from service.person_service import PersonService
import unittest

#


class Test(unittest.TestCase):
    person_validator = PersonValidator()
    person_repository = Repository()

    activity_validator = ActivityValidator()
    activity_repository = Repository()

    person_service = PersonService(person_validator, person_repository, activity_repository)
    activity_service = ActivityService(activity_validator, activity_repository, person_service)

    def run_tests(self):
        self.test_add_person()
        self.test_add_activity()
        self.test_update()

    # Add functionality

    # Person

    def test_add_person(self):
        self.assertEqual(len(self.person_service.get_all_persons()), 0)

        self.person_service.add_person("neamtiu ovidiu zaris", "0753429584")
        self.assertEqual(len(self.person_service.get_all_persons()), 1)

        self.person_service.add_person("Andrei mocanu")
        self.assertEqual(len(self.person_service.get_all_persons()), 2)

        self.person_service.add_person("gica Ciobanu", "0742529429")
        self.assertEqual(len(self.person_service.get_all_persons()), 3)

        li_persons = self.person_service.get_all_persons()

        self.assertEqual(li_persons[0].name, "Neamtiu Ovidiu Zaris")
        self.assertEqual(li_persons[1].name, "Andrei Mocanu")
        self.assertEqual(li_persons[2].name, "Gica Ciobanu")

        self.assertEqual(li_persons[0].phone_number, "0753429584")
        self.assertEqual(li_persons[1].phone_number, "unknown")
        self.assertEqual(li_persons[2].phone_number, "0742529429")

        self.assertRaises(PersonValidatorException, self.person_service.add_person, "N3amtiu")
        self.assertRaises(PersonValidatorException, self.person_service.add_person, "Zaris", "02432j45")

    # Activity

    def test_add_activity(self):
        self.assertRaises(ActivityValidatorException, self.activity_service.add_activity,
                          [10], "11/11/2020", "18:13", "Golf")
        self.assertRaises(ActivityValidatorException, self.activity_service.add_activity,
                          [20], "11/11/2020", "18:13", "Golf")
        self.assertRaises(ActivityValidatorException, self.activity_service.add_activity,
                          [4], "11/11/2020", "18:13", "Bowling")
        self.assertRaises(ActivityValidatorException, self.activity_service.add_activity,
                          [6, 7], "asdasd", "13:20", "Karting")
        self.assertRaises(ActivityValidatorException, self.activity_service.add_activity,
                          [6], "11/11/2020", "1b3:20", "Karting")

    # Update functionality

    # Activity

    def test_update(self):
        self.activity_service.add_activity([1, 2, 3], "2/2/2020", "12:20", "Python")
        a2 = Activity([1, 2], "1/1/2001", "11:10", "Fotbal")
        self.activity_service.update_activity(6, [1, 2], "1/1/2001", "11:10", "Fotbal")
        li_activities = self.activity_service.get_all_activities()

        self.assertEqual(li_activities[0].id, 6)
        self.assertEqual(li_activities[0].date, a2.date)
        self.assertEqual(li_activities[0].time, a2.time)
        self.assertEqual(li_activities[0].person_id_list, a2.person_id_list)
        self.assertEqual(li_activities[0].description, a2.description)

