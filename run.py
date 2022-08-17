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
    table.add_column("Artist", style="black bold on grey78")
    table.add_column("Title", style="black bold on grey78")
    table.add_column("Label", style="black bold on grey78")
    table.add_column("Format", style="black bold on grey78")
    table.add_column("Rating (1-5)", style="black bold on grey78")
    table.add_column("Released", style="black bold on grey78")
    table.add_column("Date Added", style="black bold on grey78")
    table.add_column("Value (€)", style="black bold on grey78")

    for row in data[0::1]:
        table.add_row(*row, style="black bold on grey78")

    os.system("clear")
    console.print(f"{LOGO}", style="dark_orange3")
    console.print(table)

def main():
    """
    Run all application functions
    """

    os.system("clear")
    console.print(f"{LOGO}", style="dark_orange3")
    show_menu()


main()
