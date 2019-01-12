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
        for key, value in directory_main.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('\n> ').lower().strip()

        if choice in directory_main:
            clear()
            directory_main[choice]()

        if choice not in directory_main:
            clear()
            print("That is not a valid selection.")
        clear()
        print("Please select from one of the following options:\n")


def view_loop():
    """Search for an existing entry"""
    choice = None
    clear()

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in directory_view.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('\n> ').lower().strip()

        if choice in directory_view:
            clear()
            entries = directory_view[choice]()
            view_entry(entries)

        if choice not in directory_view:
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
                entry.task_name,
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


def find_by_employee():
    """Find employee based on entry"""
    entries = Entry.select().order_by(Entry.employee_name.desc())
    print("Find by employee:\nSelect an employee from the list below:")
    employees = []

    for entry in entries:
        if entry.employee_name not in employees:
            employees.append(entry.employee_name)

    for entry in employees:
        print("{}) {}".format(employees.index(entry), str(entry)))

    selection = test_input(len(employees))
    return entries.where(Entry.employee_name.contains(employees[selection]))


def find_by_date():
    """Find by date of the task"""
    entries = Entry.select().order_by(Entry.task_date.desc())
    print("Find by date:\nSelect a date from the list below:")
    date = []

    for entry in entries:
        if entry.task_date not in date:
            date.append(entry.task_date)

    for entry in date:
        print("{}) {}".format(date.index(entry),
                              entry.strftime('%A %B %d, %Y %I:%Mp')))

    selection = test_input(len(date))
    return entries.where(Entry.task_date.contains(date[selection]))


def find_by_time_spent():
    """Find by time spent"""
    entries = Entry.select().order_by(Entry.task_date.desc())
    print("Find by date:\nSelect a date from the list below:")
    duration = []

    for entry in entries:
        if entry.task_minutes not in duration:
            duration.append(entry.task_minutes)

    for entry in duration:
        print("{}) {}".format(duration.index(entry), entry))

    selection = test_input(len(duration))
    return entries.where(Entry.duration.contains(duration[selection]))


def find_by_search_term():
    """Find by searching for a term"""
    search_query = input("Enter a term to search the work log:\n> ")
    entries = Entry.select().order_by(Entry.task_date.desc())
    logs = entries.where(Entry.employee_name.contains(search_query)|
                         Entry.task_name.contains(search_query)|
                         Entry.notes.contains(search_query))

    return logs


def delete_entry(entry):
    """Delete entry"""
    if input("Are you sure you want to delete this entry? Hit 'Y' for YES 'N' for NO ").upper() == 'Y':
        entry.delete_instance()
        print('Entry has been deleted!')
        input('Press ENTER to continue.')


def test_input(length):
    selection = None
    while selection is None:
        try:
            selection = int(input("> "))
        except ValueError:
            print("Invalid selection. Please select a number.")
            selection = None

        if selection not in range(0, length):
            selection = None

    return selection


directory_main = OrderedDict([
    ('1', add_entry),
    ('2', view_loop),
    ])


directory_view = OrderedDict([
    ('1', find_by_employee),
    ('2', find_by_date),
    ('3', find_by_time_spent),
    ('4', find_by_search_term)
    ])


if __name__ == '__main__':
    initialize()
    main_menu()
