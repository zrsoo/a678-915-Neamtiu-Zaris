"""
### For week 8 (25% of grade)
- Implement features 1 and 2 -> DONE
- Have at least 10 procedurally generated items in your application at startup -> DONE
- Provide specification and tests for all non-UI classes and methods for the first functionality -> DONE
- Implement and use your own exception classes. -> DONE


### For week 9 (25% of grade)
- Implement features 3 and 4.
- Implement PyUnit test cases. -> DONE


### 5. Activity Planner
The following information is stored in domain personal activity planner:
- **Person**: `person_id`, `name`, `phone_number`
- **Activity**: `activity_id`, `person_id` - list, `date`, `time`, `description`

Create an application to:
1. Manage persons and activities. The user can add, remove, update, and list both persons and activities.
2. Add/remove activities. Each activity can be performed together with one or several other persons,
    who are already in the user’s planner. Activities must not overlap
    (user cannot have more than one activity at any given time).
3. Search for persons or activities. Persons can be searched for using name or phone number. Activities can be searched
    for using date/time or description. The search must work using case-insensitive, partial string matching,
    and must return all matching items.
4. Create statistics:
    - Activities for a given date. List the activities for a given date, in the order of their start time.
    - Busiest days. This will provide the list of upcoming dates with activities, sorted in descending order of the
    free time in that day (all intervals with no activities).
    - Activities with domain given person. List all upcoming activities to which domain given person will participate.
5. Unlimited undo/redo functionality. Each step will undo/redo the previous operation performed by the user.
    Undo/redo operations must cascade and have domain memory-efficient implementation (no superfluous list copying).



## Bonus possibility (0.1p, deadline week 10)
- 95% unit test code coverage for all modules except the UI (use *PyCharm Professional*, the *[coverage]
(https://coverage.readthedocs.io/en/coverage-5.3/)* or other modules)

## Bonus possibility (0.2p, deadline week 10)
- Implement domain graphical user interface, in addition to the required menu-driven UI.
 Program can be started with either UI,
 without changes to source code.
"""


# Start

# Imports
import traceback
from domain.validators import PersonValidator, ActivityValidator
from repository.inmemoryrepo import Repository
from service.activity_service import ActivityService
from service.person_service import PersonService
from ui.console import Console
#


if __name__ == "__main__":

    # test = Test()
    # test.run_tests()

    try:
        person_validator = PersonValidator()
        person_repository = Repository()

        activity_repository = Repository()
        activity_validator = ActivityValidator()

        person_service = PersonService(person_validator, person_repository, activity_repository)
        activity_service = ActivityService(activity_validator, activity_repository, person_service)

        console = Console(person_service, activity_service)
        console.run_console()
    except Exception as ex:
        print("Error, " + str(ex))
        # traceback.print_exc()
