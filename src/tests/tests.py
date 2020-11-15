"""
    Testing module
"""

# Imports
from domain.entity import Activity
from domain.validators import PersonValidator, ActivityValidator, ActivityValidatorException, PersonValidatorException
from repository.inmemoryrepo import Repository
from service.activity_service import ActivityService
from service.person_service import PersonService


#


class Test:
    person_validator = PersonValidator()
    person_repository = Repository()
    person_service = PersonService(person_validator, person_repository)

    activity_validator = ActivityValidator()
    activity_repository = Repository()
    activity_service = ActivityService(activity_validator, activity_repository, person_service)

    def run_tests(self):
        self.test_add_person()
        self.test_add_activity()
        self.test_update()

    # Add functionality

    # Person

    def test_add_person(self):
        assert len(self.person_service.get_all_persons()) == 0

        self.person_service.add_person("neamtiu ovidiu zaris", "0753429584")
        assert len(self.person_service.get_all_persons()) == 1
        self.person_service.add_person("Andrei mocanu")
        assert len(self.person_service.get_all_persons()) == 2
        self.person_service.add_person("gica Ciobanu", "0742529429")
        assert len(self.person_service.get_all_persons()) == 3

        li_persons = self.person_service.get_all_persons()

        assert li_persons[0].name == "Neamtiu Ovidiu Zaris"
        assert li_persons[1].name == "Andrei Mocanu"
        assert li_persons[2].name == "Gica Ciobanu"

        assert li_persons[0].phone_number == "0753429584"
        assert li_persons[1].phone_number == "unknown"
        assert li_persons[2].phone_number == "0742529429"

        try:
            self.person_service.add_person("N3amtiu")
            assert False
        except PersonValidatorException:
            assert True

        try:
            self.person_service.add_person("Zaris", "02432j45")
            assert False
        except PersonValidatorException:
            assert True

    # Activity

    def test_add_activity(self):
        try:
            self.activity_service.add_activity([10], "11/11/2020", "18:13", "Golf")
            assert False
        except ActivityValidatorException:
            assert True

        try:
            self.activity_service.add_activity([20], "11/11/2020", "18:13", "Golf")
            assert False
        except ActivityValidatorException:
            assert True

        try:
            self.activity_service.add_activity([4], "11/11/2020", "18:13", "Bowling")
            assert False
        except ActivityValidatorException:
            assert True

        try:
            self.activity_service.add_activity([6, 7], "asdasd", "13:20", "Karting")
            assert False
        except ActivityValidatorException:
            assert True

        try:
            self.activity_service.add_activity([6], "11/11/2020", "1b3:20", "Karting")
            assert False
        except ActivityValidatorException:
            assert True

    # Update functionality

    # Activity

    def test_update(self):
        self.activity_service.add_activity([1, 2, 3], "2/2/2020", "12:20", "Python")
        a2 = Activity([1, 2], "1/1/2001", "11:10", "Fotbal")
        self.activity_service.update_activity(6, [1, 2], "1/1/2001", "11:10", "Fotbal")
        li_activities = self.activity_service.get_all_activities()
        assert li_activities[0].id == 6
        assert li_activities[0].date == a2.date
        assert li_activities[0].time == a2.time
        assert li_activities[0].person_id_list == a2.person_id_list
        assert li_activities[0].description == a2.description

