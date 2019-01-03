#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import sys
import os

from peewee import *

db = SqliteDatabase('Work_Database.db')

class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default = datetime.datetime.now)

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
    """Add a new entry"""
    get_employee()
    get_task()
    get_valid_date()





def get_employee():
    """Employee name input"""
    while True:
        employee_name = input("Please enter the employee's name: ")
        clear()

        if employee_name:
            if input("Save entry? [Y/N]").upper != 'N':
                Entry.create(content=employee_name)
                break

def get_task():
    while True:
        task_name = input("Please enter the task name: ")
        clear()

        if task_name:
            if input("Save entry? [Y/N]").upper != 'N':
                Entry.create(content=task_name)
                break

def get_minutes():
    pass


def find_employee(name_search):
    """Search using name of employee"""
    pass
    # present list of employees with entries and be able to chose one to see entries

def find_date(date_input):
    """Search by date"""
    pass



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
