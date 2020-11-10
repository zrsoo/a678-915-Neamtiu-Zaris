"""
    Validators module
"""


class StoreException(Exception):
    pass


class PersonValidatorException(StoreException):
    pass


class PersonValidator:
    # Functions for validating name.

    def has_numbers(self, string):
        """
        Checks if a certain string contains any numbers.
        :param string: The string that is checked
        :return: True if the string contains at least one number, false otherwise.
        """
        return any(char.isdigit() for char in string)

    def capitalize(self, string):
        """
        Capitalizes the first letter of each part of the name
        :param string: The string containing the name
        :return:
        """
        # Capitalizing the first character (if it's not already capitalized).
        if string[0].islower():
            string_upper = string.replace(string[0], string[0].upper())
            string = string_upper

        # Capitalizing the rest of the characters (if they are not already capitalized).
        for index in range(1, len(string)):
            if string[index].islower() and string[index - 1] == " ":
                string_upper = string.replace(string[index], string[index].upper())
                string = string_upper

        print(string_upper)
        return string_upper
    #

    # Functions for validating phone number.

    def has_letters(self, string):
        """
        Checks if there are any non numerical characters in a certain string.
        :param string: The string being checked.
        :return: True if there are any letters in the string, false otherwise.
        """
        return any(not char.isdigit() for char in string)

    #

    def validate(self, person):
        person.name = self.capitalize(person.name)

        if self.has_numbers(person.name):
            raise PersonValidatorException("Name cannot contain any numbers.")

        if self.has_letters(person.phone_number):
            raise PersonValidatorException("Phone number cannot contain any letters or spaces.")


# string1 = "ovidiu zaris neamtiu"
# string2 = "ov1diu zaris neamtiu"
# string3 = "0755328329382632983"
# string4 = "4324252b41232131"
# validator = PersonValidator()
# string1 = validator.capitalize(string1)
# print(string1)
# print(validator.has_numbers(string2))
# print(validator.has_numbers(string1))
# print(validator.has_letters(string3))
# print(validator.has_letters(string4))
