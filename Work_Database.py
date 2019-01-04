#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import sys
import os

from peewee import *

db = SqliteDatabase('Work_Database.db')

class User(Model):
    """Table that stores the user's name"""
    employee_name = CharField()

    class Meta:
        database = db


class Entry(Model):
    employee_name = CharField(max_length=255)
    task_minutes = IntegerField()
    task_name = CharField(max_length=535)
    task_date = DateTimeField(default=datetime.date.today().strftime('%d/%m/%Y'))
    notes = TextField(default="")

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't already exist"""
    db.connect()
    db.create_tables([User, Entry], safe=True)


def clear():
    """Clear the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
    """Show the menu"""

    choice = None

    clear()
    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('\n> ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()
        else:
            clear()
            print("That is not a valid selection.")
        clear()
        print("Thanks for using the Work Log Database.")


def find_entry():
    """Search for an existing entry"""
    choice = None
    clear()

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in sub_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('\n> ').lower().strip()

        if choice == 'a':
            clear()
            name_search = input("Please enter the name you'd like to search: ")
            find_employee(name_search)

        if choice == 'b':
            clear()
            while True:
                try:
                    time_input = int(input("Please enter time spent in minutes (Whole numbers only): "))
                    break
                except ValueError:
                    clear()
                    print("Invalid entry.")

            find_time(time_input)

        if choice == 'c':
            clear()
            string_search = input("Please enter your search: ")
            find_term(string_search)

        if choice == 'd':
            clear()
            while True:
                date_input = input("Please provide a date. Please use the format MM/DD/YYYY: ")
                clear()

                try:
                    datetime.datetime.strptime(date_input, "%m/%d/%Y")
                    find_date(date_input)
                    break

                except ValueError:
                    print("Invalid date")


def new_entry():
    """Add and create a new entry"""
    username = get_employee("Please enter the employee's name: ")
    clear()
    task_date = get_date("What is the date of the task? Please use the MM/DD/YYYY format: ")
    clear()
    task_name = input("Title of the task: ")
    clear()
    task_minutes = get_minutes("Time spent, rounded in minutes: ")
    clear()
    task_notes = input("Notes (optional, you may leave this blank): ")
    return username, task_date, task_name, task_minutes, task_notes


def get_employee(name_input):
    """Employee name input"""
    username = input(name_input)
    return username


def get_date(question):
    while True:
        try:
            date_input = input(question)
            datetime.datetime.strptime(date_input, "%m/%d/%Y")
            break
        except ValueError:
            print("Invalid date")


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


def write_entry(username, task_date, task_name, task_minutes, task_notes):
    """Write the work log to the database."""
    Entry.create(username=username,
                 task_date=task_date,
                 task_name=task_name,
                 task_minutes=task_minutes,
                 task_notes=task_notes)


def find_employee(name_search):
    """Search using name of employee"""
    pass
    # present list of employees with entries and be able to chose one to see entries

def find_date(date_input):
    """Search by date"""
    return Entry.select().where(Entry.task_date == date_input)

def find_time(time_input):
    """Search by time spent"""
    pass
    # search by time spent and presented with list of projects matching time spent

def find_term(string_search):
    """Search by term"""
    pass


menu = OrderedDict([
    ('a', new_entry),
    ('b', find_entry)
])

sub_menu = OrderedDict([
    ('a', find_employee),
    ('b', find_time),
    ('c', find_term),
    ('d', find_date)
])


if __name__ == '__main__':
    initialize()
    main_menu()
    write_entry()