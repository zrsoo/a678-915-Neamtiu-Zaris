"""
    UI class.

    Calls between program modules
    ui -> service -> entity
    ui -> entity
"""
# Imports
import re
#

# Font formatting


underline = '\u001b[4m'
default = '\u001b[0m'
bold = '\u001b[1m'
green = '\u001b[32m'
red = '\u001b[31m'
blue = '\033[94m'

#


class Console:
    def __init__(self, person_service, activity_service):
        self.__person_service = person_service
        self.__activity_service = activity_service

    def run_console(self):
        try:
            self.__person_service.generate_persons()
            self.__activity_service.generate_activities()
        except Exception as ex:
            print("Error, " + str(ex))

        while True:
            try:
                self.print_menu()
                user_command = input("Please type your command: ")
                li_words = self.format_input(user_command)

                if user_command == "exit":
                    return
                elif li_words[0] == "add":
                    if li_words[1] == "person":
                        li_info = self.format_person_add(user_command)
                        if len(li_info) == 2:
                            name, phone_number = li_info
                        else:
                            name = li_info
                            phone_number = "unknown"
                        self.__person_service.add_person(name, phone_number)
                    if li_words[1] == "activity":
                        person_id = self.format_id_list(li_words[2])
                        date = li_words[3]
                        time = li_words[4]
                        description = li_words[5]
                        self.__activity_service.add_activity(person_id, date, time, description)
                elif li_words[0] == "list":
                    if li_words[1] == "persons":
                        self.print_all_persons()
                    elif li_words[1] == "activities":
                        self.print_all_activities()
                elif li_words[0] == "remove":
                    if li_words[1] == "person":
                        self.__person_service.delete_person(int(li_words[2]))
                    elif li_words[1] == "activity":
                        self.__activity_service.delete_activity(int(li_words[2]))
                elif li_words[0] == "update":
                    if li_words[1] == "person":
                        id_person = li_words[2]
                        li_info = self.format_person_update(user_command)
                        print(li_info)
                        new_name, new_phone_number = li_info
                        self.__person_service.update_person(id_person, new_name, new_phone_number)
                    elif li_words[1] == "activity":
                        id_activity = li_words[2]
                        new_person_id = self.format_id_list(li_words[3])
                        new_date = li_words[4]
                        new_time = li_words[5]
                        new_description = li_words[6]
                        self.__activity_service.update_activity(id_activity, new_person_id, new_date, new_time,
                                                                new_description)
                else:
                    print("The command you have typed is of incorrect form.")
            except Exception as ex:
                print("Error, " + str(ex))

    def print_all_persons(self):
        print(green + "The list of persons is:\nFormat: *id*.) *name*; *phone number*" + default)
        li_persons = self.__person_service.get_all_persons()
        for person in li_persons:
            print(str(person))
        print()

    def print_all_activities(self):
        print(green + "The list of activities is:\nFormat: *id*.) Personal Id's: *person id list*"
                      "; *date*; *time*; *description*" + default)
        li_activities = self.__activity_service.get_all_activities()
        for activity in li_activities:
            print(str(activity))
        print()

    @staticmethod
    def print_menu():
        print()
        print(green + bold + underline + "List of commands:" + default)
        print("1.) " + blue + "add person *name* *phone number*" + default + " - Adds a person\n"
              "2.) " + blue + "remove person *id*" + default + " - Removes a person\n"
              "3.) " + blue + "update person *id* *new_name* *new_phone_number*" + default + " - Updates a person\n"
              "4.) " + blue + "list persons" + default + " - Displays all persons\n"
              "5.) " + blue + "add activity *[person_id's]*, *date*, *time*, *description*" + default + " - Adds"
                                                                                                        " an activity\n"
              "6.) " + blue + "remove activity *id*" + default + " - Removes an activity\n"
              "7.) " + blue + "update activity *id* *[person_id's]* *date* *time* *description*"
              + default + " - ""Updates an activity\n"
              "8.) " + blue + "list activities" + default + " - Displays all activities\n"
              "9.) " + red + "exit" + default)

    @staticmethod
    def format_input(input_str):
        """
        Receives the string that was typed by the user in the console.
        :return: A list containing each word separately
        """
        li_words = input_str.split()
        return li_words

    @staticmethod
    def format_id_list(string):
        """
        Receives a string containing the list of id's of persons performing an activity
        :return: A list containing the id's
        """
        string = string[1:-1]
        li_ids = []
        for word in string.split(","):
            li_ids.append(int(word))
        # print(li_ids)
        return li_ids

    @staticmethod
    def format_person_add(string):
        """
        Receives a string containing a command used to add a person.
        :param string: the string
        :return: A list containing the name on the first position, and the phone number
        on the second one (if it is specified).
        """
        m = re.search(r"\d", string)

        if m is None:  # if the phone number is not specified
            return string[11:]
        else:
            li_info = [string[11:m.start()-1], string[m.start():]]
        return li_info

    @staticmethod
    def format_person_update(string):
        """
        Receives a string containing a command used to add a person.
        :param string: the string
        :return: A list containing the name on the first position, and the phone number
        on the second one (if it is specified).
        """
        last_space_pos = string.rfind(' ')
        phone_number = string[last_space_pos + 1:]
        pos1 = string.find(' ')
        pos2 = string.find(' ', pos1 + 1)
        pos3 = string.find(' ', pos2 + 1)
        if last_space_pos == pos3:
            name = string[pos3+1:]
            phone_number = "unknown"
        else:
            name = string[pos3 + 1:last_space_pos]
        li_info = [name, phone_number]
        return li_info
