"""Import modules"""
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import os
from time import sleep
import gspread
from google.oauth2.service_account import Credentials
from rich.console import Console
from rich.theme import Theme
from rich.table import Table

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("credentials.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("music_collection")
collection = SHEET.worksheet("collection")

custom_theme = Theme({"error": "bold red", "success": "bold green"})
console = Console(theme=custom_theme)

LOGO = """
██     ██  ██████  ███    ███
██     ██ ██    ██ ████  ████
██  █  ██ ██    ██ ██ ████ ██
██ ███ ██ ██    ██ ██  ██  ██
 ███ ███   ██████  ██      ██


██████  ███████  ██████  ██████  ██████  ██████  ███████
██   ██ ██      ██      ██    ██ ██   ██ ██   ██ ██
██████  █████   ██      ██    ██ ██████  ██   ██ ███████
██   ██ ██      ██      ██    ██ ██   ██ ██   ██      ██
██   ██ ███████  ██████  ██████  ██   ██ ██████  ███████
"""


def show_menu():
    """
    Function prints out the menu and get the user input.
    Validation of users choice is also being made.
    """

    while True:
        menu_options = {
            1: "List music collection",
            2: "Search item in music collection",
            3: "Add item to collection",
            4: "Change item in collection",
            5: "Remove item from collection",
            6: "Sort collection",
            7: "Show total value of collection",
            0: "Exit application",
        }
        print("\n")

        for choice in menu_options.keys():
            console.print(
                choice, " - ", menu_options[choice], style="cyan"
            )

        option = input("\nEnter your choice: ")
        option = option.strip()
        if option == "1":
            list_collection()



        elif option == "3":
            while True:
                os.system("clear")
                console.print(f"{LOGO}", style="dark_orange3")
                console.print(
                    "\nTo add an item to the record collection, follow these"
                    "\ninstructions (or choose 0 to return to main menu):",
                    style="bold cyan",
                )
                console.print(
                    "\n* Add all columns with comma separation"
                    "\n(Artist,Title,Label,Format, Rating (1-5),"
                    "\nReleased,Date Added (yyyy-mm-dd),Value)",
                    style="cyan",
                )
                console.print(
                    "\n* Example: Shield,Vampiresongs,Desperate Fight Records,"
                    "\nCD,5,1995,2022-08-17,50",
                    style="cyan",
                )
                user_input = input("\nAdd data: ")
                user_data = list(user_input.split(","))
                if user_input == "0":
                    console.print(
                        "\nHeading back to main menu", style="success"
                    )
                    sleep(3)
                    os.system("clear")
                    console.print(f"{LOGO}", style="dark_orange3")
                    show_menu()
                    break
                elif len(user_data) != 8:
                    console.print(
                        "\nExactly 8 values are required. Please try again",
                        style="error",
                    )
                    sleep(3)
                else:
                    add_item(user_data, "collection")
                    break
        elif option == "7":
            sum_value = calculate_total_value()
            console.print(
                f"\nThe collection is worth €{sum_value}", style="success"
            )

def list_collection():
    """
    This function import all the values from the collection
    sheet and pass it to the variable 'data'. After that
    the function calls the create_table function.
    """

    console.print("\nPlease wait. Listing collection.", style="success")
    sleep(2)
    data = collection.get_all_values()
    create_table(data)


def create_table(data):
    """
    This function creates the table. First it plots the
    columns and then it plots out all the rows in the
    data collection (from the collection sheet)
    """

    table = Table()
    table.add_column("Artist")
    table.add_column("Title")
    table.add_column("Label")
    table.add_column("Format")
    table.add_column("Rating (1-5)")
    table.add_column("Released")
    table.add_column("Date Added")
    table.add_column("Value (€)")

    for row in data[0::1]:
        table.add_row(*row, style="black bold on grey78")

    os.system("clear")
    console.print(f"{LOGO}", style="dark_orange3")
    console.print(table)


def add_item(new_row, worksheet):
    """
    This function adds item to the record collection
    """

    console.print(f"\nUpdating {worksheet}' worksheet.\n", style="success")
    sleep(2)
    worksheet_to_update = SHEET.worksheet(worksheet)
    # converts string numbers in list to integers - taken from
    # https://www.geeksforgeeks.org/python-convert-numeric-string-to-integers-in-mixed-list/
    new_row_converted = [
        int(ele) if ele.isdigit() else ele for ele in new_row
    ]

    # adds new row to the end of the current data
    worksheet_to_update.append_row(new_row_converted)
    os.system("clear")
    console.print(f"{LOGO}", style="dark_orange3")
    list_collection()


def calculate_total_value():
    """
    Calculate the total value of record collection.
    """
    console.print(
        "\nPlease wait. Calculating total value of the record collection.",
        style="success",
    )
    sleep(2)
    value_data = collection.col_values(8)
    value_data = list(map(int, value_data))
    sum_value = sum(value_data)
    os.system("clear")
    console.print(f"{LOGO}", style="dark_orange3")
    return sum_value

def main():
    """
    Run all application functions
    """

    os.system("clear")
    console.print(f"{LOGO}", style="dark_orange3")
    show_menu()


main()
