#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import os

from peewee import *

db = SqliteDatabase('Work_Database.db')


class Entry(Model):
    employee_name = CharField(max_length=255, unique=False)
    task_minutes = CharField(max_length=255, unique=False)
    task_name = CharField(max_length=255, unique=False)
    task_date = DateTimeField()
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
        print("Enter 'q' to quit.")
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
        print('m) main menu')

        next_action = None

        while next_action is None:
            next_action = input(">  ").lower().strip()

            if next_action == 'd':
                delete_entry(entry)

            elif next_action == 'm':
                main_menu()

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

    print("Add a new entry:")
    info5 = get_task_date()
    clear()

    Entry.create(employee_name=info1, task_name=info2, task_minutes=info3, notes=info4, task_date=info5)

    print("Your entry has been saved.")
    input("Press ENTER to continue.")


def get_employee_name():
    """Get the name of the employee"""
    while True:
        employee = input("Enter the name of the employee: ")
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


def get_task_date():
    while True:
        task_date = input("Enter a date for the task. Please use MM/DD/YYYY format: ")
        try:
            datetime.datetime.strptime(task_date, "%m/%d/%Y")
        except ValueError:
            clear()
            print("Invalid date. Please provide a valid date using the format MM/DD/YYYY: ")
            continue
        else:
            return task_date


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
    notes = input("Please enter any additional notes for this task entry (OPTIONAL): ")
    return notes


def find_by_employee():
    """Find employee based on entry"""
    entries = Entry.select().order_by(Entry.employee_name.desc())
    if not entries:
        input("The database is empty. Press ENTER to return to the main menu")
        main_menu()
    else:
        print("Find by employee:\nSelect an employee from the list below:")
        employees = []
        for entry in entries:
            if entry.employee_name not in employees:
                employees.append(entry.employee_name)

        for entry in employees:
            print("{}.)  {}".format(employees.index(entry), str(entry)))

        selection = test_input(len(employees))
        return entries.where(Entry.employee_name.contains(employees[selection]))


def find_by_date():
    """Find by date of the task"""
    entries = Entry.select().order_by(Entry.task_date.desc())
    if not entries:
        input("The database is empty. Press ENTER to return to the main menu")
        main_menu()
    else:
        date = []
        print("Find by date:\nSelect a date from the list below:")
        for entry in entries:
            if entry.task_date not in date:
                date.append(entry.task_date)
        else:
            for entry in date:
                print("{}.)  {}".format(date.index(entry),
                                        entry))

            selection = test_input(len(date))
            return entries.where(Entry.task_date.contains(selection))


def find_by_time_spent():
    """Find by time spent"""
    entries = Entry.select().order_by(Entry.task_date.desc())
    if not entries:
        input("The database is empty. Press ENTER to return to the main menu")
        main_menu()
    else:
        duration = []
        print("Find by date:\nSelect a date from the list below:")
        for entry in entries:
            if entry.task_minutes not in duration:
                duration.append(entry.task_minutes)

        for entry in duration:
            print("{}.)  {}".format(duration.index(entry), entry))

        selection = test_input(len(duration))
        return entries.where(Entry.task_minutes.contains(duration[selection]))


def find_by_search_term():
    """Find by searching for a term"""
    while True:
        search_query = input("Enter a term to search the work log:\n> ")
        entries = Entry.select().order_by(Entry.task_date.desc())
        logs = entries.where(Entry.employee_name.contains(search_query)|
                             Entry.task_name.contains(search_query)|
                             Entry.notes.contains(search_query))
        if logs:
            return logs
        else:
            input("That term is not in the database. Press ENTER to return to the main menu")
            main_menu()


def delete_entry(entry):
    """Delete entry"""
    if input("Are you sure you want to delete this entry? Hit 'Y' for YES 'N' for NO ").upper() == 'Y':
        entry.delete_instance()
        print('Entry has been deleted.\n')
        input('Press ENTER to continue.')
        clear()
    else:
        clear()
        main_menu()


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
    ('a', add_entry),
    ('b', view_loop),
    ])


directory_view = OrderedDict([
    ('a', find_by_employee),
    ('b', find_by_date),
    ('c', find_by_time_spent),
    ('d', find_by_search_term)
    ])


if __name__ == '__main__':
    initialize()
    main_menu()
