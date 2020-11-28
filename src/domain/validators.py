"""
    Validators module
"""


# Useful functions


def has_numbers(string):
    """
    Checks if a certain string contains any numbers.
    :param string: The string that is checked
    :return: True if the string contains at least one number, false otherwise.
    """
    return any(char.isdigit() for char in string)


def has_letters(string):
    """
    Checks if there are any non numerical characters in a certain string.
    :param string: The string being checked.
    :return: True if there are any letters in the string, false otherwise.
    """
    return any(not char.isdigit() and char != '+' for char in string)


#

# Person validator


class StoreException(Exception):
    pass


class PersonValidatorException(StoreException):
    pass


class PersonValidator:
    # Functions for validating name.
    @staticmethod
    def capitalize(string):
        """
        Capitalizes the first letter of each part of the name
        :param string: The string containing the name
        :return:
        """
        li_words = string.split()
        li_words = [word.replace(word[0], word[0].upper(), 1) for word in li_words]
        string_upper = ''
        string_upper = string_upper + ''.join(' ' + word for word in li_words)
        string_upper = string_upper[1:]
        return string_upper

    #

    def validate(self, person):
        person.name = self.capitalize(person.name)

        if has_numbers(person.name):
            raise PersonValidatorException("Name cannot contain any numbers.")

        if has_letters(person.phone_number) and not person.phone_number == "unknown":
            raise PersonValidatorException("Phone number cannot contain any letters or spaces.")


# Activity validator


class StoreException(Exception):
    pass


class ActivityValidatorException(StoreException):
    pass


class ActivityValidator:
    @staticmethod
    def validate(activity):
        # Checking if date or time contain any unwanted characters.
        for char in activity.date:
            if not char.isdigit() and not char == '/':
                raise ActivityValidatorException("Date is of incorrect form.")

        for char in activity.time:
            if not char.isdigit() and char not in '-:':
                raise ActivityValidatorException("Time is of incorrect form.")
