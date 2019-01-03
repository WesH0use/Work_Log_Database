from peewee import *

db = SqliteDatabase('Work_Database.db')

class Entry(Model):
    pass

    def main_menu():
        pass
        # Option to look up previous entry or add new entry

        # new work log option


    def new_entry():
        pass
        # user provide name, task name, number of minutes spent working, additional notes


    def find_entry():
        pass
        # presented with four options: find employee, date, time spent, search item


    def find_employee():
        pass
        # present list of employees with entries and be able to chose one to see entries


    def find_date():
        pass
        # presented with a list of dates with entries and be able to choose one to see entries.


    def fine_time():
        pass
        # search by time spent and presented with list of projects matching time spent


    def find_term():
        pass
        # User enters string and presented with entries containing the string in task name OR notes.

    # As a user of the script, I should be able to choose whether to add a new entry or lookup previous entries.

    # As a user of the script, if I choose to enter a new work log, I should be able to provide my name, a task name,
    # a number of minutes spent working on it, and any additional notes I want to record.

    # As a user of the script, if I choose to find a previous entry, I should be presented with four options:
    # find by employee, find by date, find by time spent, find by search term.

    # As a user of the script, if finding by employee, I should be presented with a list of employees with entries and
    # be able to choose one to see entries from.

    # As a user of the script, if finding by employee, I should be allowed to enter employee name and then be
    # presented with entries with that employee as their creator.

    # As a user of the script, if finding by date, I should be presented with a list of dates with entries and
    # be able to choose one to see entries from.

    # As a user of the script, if finding by time spent, I should be allowed to enter the amount of time spent
    # on the project and then be presented with entries containing that amount of time spent.

    # As a user of the script, if finding by a search term, I should be allowed to enter a string and then be presented
    # with entries containing that string in the task name or notes.

    # As a fellow developer, I should find at least 50% of the code covered by tests. I would use coverage.py
    # to validate this amount of coverage.
