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


def main():
    """
    Run all application functions
    """

    os.system("clear")
    console.print(f"{LOGO}", style="dark_orange3")
    show_menu()


main()
