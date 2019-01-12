#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import os

from peewee import *

db = SqliteDatabase('Work_Database.db')


class Entry(Model):
    employee_name = CharField(max_length=255, unique=False)
    task_minutes = CharField(max_length=255, unique=False)
    task_name = CCharField(max_length=255, unique=False)
    task_date = DateTimeField(default=datetime.datetime.now)
    notes = CharField(max_length=255, unique=False)

    class Meta:
        database = db



def initialize():
    """Create the database and the table if they don't already exist"""
    db.connect()
    db.create_tables([Entry], safe=True)


def clear():
    """Clear the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
    """Show the menu"""
    choice = None

    clear()
    while choice != 'q':
        print("Welcome to the Worklog database. Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('\n> ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()

        if choice not in menu:
            clear()
            print("That is not a valid selection.")
        clear()
        print("Please select from one of the following options:\n")


def find_entry():
    """Search for an existing entry"""
    choice = None
    clear()

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in sub_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('\n> ').lower().strip()

        if choice in sub_menu:
            clear()
            entries = sub_menu[choice]()
            view_entry(entries)

        if choice not in sub_menu:
            clear()
            print("Please select from one of the following options:\n")

def view_entry(entries):
    """Return the entries"""
    for entry in entries:
        clear()
        print("Below are your selected entries: ")
        print("""
        Name: {}
        Date: {}
        Task: {}
        Length: {}
        Notes: {}
        """.format(entry.employee_name,
                entry.task_date,
                entry.task_name
                entry.task_minutes,
                entry.notes
                ))

        print('n) next entry')
        print('d) delete entry')

        next_action = None

        while next_action is None:
            next_action = input(">: ").lower().strip()

            if next_action == 'd':
                delete_entry(entry)

            elif next_action != 'n':
                next_action = None

def add_entry():
    """Add a new entry"""
    print("Add a new entry: ")
    info1 = get_employee_name()
    clear()

    print("Add a new entry: ")
    info2 = get_task_name()
    clear()

    print("Add a new entry: ")
    info3 = get_time_spent()
    clear()

    print("Add a new entry: ")
    info4 = get_notes()
    clear()

    Entry.create(employee_name=info1, task_name=info2, task_minutes=info3, notes=info4)

    print("Saved successfully!")
    input("Press ENTER to continue.")


def get_employee_name():
    """Get the name of the employee"""
    while True:
        employee = input("Enter the employee's name: ")
        if len(employee) == 0:
            print("\n You must enter a name")
            continue
        else:
            return employee


def get_task_name():
    """Get the name of the task"""
    while True:
        task_name=input("Enter the name of the task: ")
        if len(task_name) == 0:
            print("\nPlease enter a valid task name\n")
            continue
        else:
            return task_name

def get_time_spent():
    """Get the amount of time spent on a specific task"""
    while True:
        duration = input("Enter the time for the task (in minutes): ")
        try:
            int(duration)
        except ValueError:
            print("\nInvalid number. Please enter whole integers only\n")
            continue
        else:
            return duration

def get_notes():
    """Get the optional notes from the task"""
    notes = input("Please enter any additional notes for this entry (OPTIONAL): ")
    return notes





######




def input_info():
    """Add and create a new entry"""
    employee_name = get_employee("Please enter the employee's name: ")
    clear()
    task_date = get_date("What is the date of the task? Please use the MM/DD/YYYY format: ")
    clear()
    task_name = input("Title of the task: ")
    clear()
    task_minutes = get_minutes("Time spent, rounded in minutes: ")
    clear()
    task_notes = input("Notes (optional, you may leave this blank): ")
    return employee_name, task_date, task_name, task_minutes, task_notes


def get_employee(name_input):
    """Employee name input"""
    employee_name = input(name_input)
    return employee_name


def get_date(question):
    while True:
        try:
            date_input = input(question)
            datetime.datetime.strptime(date_input, "%m/%d/%Y")
            break
        except ValueError:
            print("Invalid date")
            continue
    return date_input


def get_minutes(minute_input):
    while True:
        try:
            minutes = int(input(minute_input))
        except ValueError:
            clear()
            print("Please provide a valid number")
            continue
        else:
            break
    return minutes


def write_entry(employee_name, task_date, task_name, task_minutes, task_notes):
    """Write the work log to the database."""
    Entry.create(employee_name=employee_name,
                 task_date=task_date,
                 task_name=task_name,
                 task_minutes=task_minutes,
                 notes=task_notes)


def add_new_entry():
    """Add new entry"""
    log = input_info()
    write_entry(log[0], log[1], log[2], log[3], log[4])
    clear()
    __ = input("The entry has been added. Press 'Enter'" +
               "to return to the main menu.")
    clear()
    return True


def find_employee(name_search):
    """Search using name of employee"""
    query = list(Entry.select().where(Entry.employee_name.contains(name_search))
    return query


def find_date(date_input):
    """Search by date"""
    pass


def find_time(time_input):
    """Search by time spent"""
    if Entry.select().where(Entry.task_minutes == time_input):
        print(Entry.task_minutes)
        print('=' * 5)
    else:
        print("Sorry, that time length is not in the database.")


def find_note(string_search):
    """Search through the notes"""
    if Entry.select().where(Entry.notes.contains(string_search)):
        print(Entry.notes)
        print('=' * len(string_search))
    else:
        print("Sorry, that note is not in the database.")


def find_task(string_search):
    """Search by term"""
    return Entry.select().where(Entry.notes == string_search)


menu = OrderedDict([
    ('a', add_new_entry),
    ('b', find_entry)
])

sub_menu = OrderedDict([
    ('a', find_employee),
    ('b', find_time),
    ('c', find_note),
    ('d', find_date)
])


if __name__ == '__main__':
    initialize()
    main_menu()