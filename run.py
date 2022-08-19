"""Import modules"""
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import os
from time import sleep
import gspread
from google.oauth2.service_account import Credentials
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.progress import Progress
from rich import box

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("music_collection")
collection = SHEET.worksheet("collection")

custom_theme = Theme({"error": "bold white on red",
                     "success": "bold black on green"})
console = Console(theme=custom_theme)

WELCOME = """
*** WOM RECORD COLLECTION ***

Welcome to WoM Record Collection, an application that keeps track on your record
collection. Use the menu below to start using the application!
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
            4: "Edit item in collection",
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

        option = input("\nEnter your choice: \n")
        option = option.strip()
        if option == "1":       # call function 'list_collection'
            add_id()
        elif option == "2":     # call function 'search_collection'
            search_collection()
        elif option == "3":     # call function 'add item'
            add_item()
            break
        elif option == "4":     # call function 'edit item'
            edit_item()
            break
        elif option == "5":     # call function 'remove item'
            remove_item()
            break
        elif option == "6":     # call function 'sort_collection'
            sort_collection()
            break
        elif option == "7":     # call function 'calculate_total_value'
            sum_value = calculate_total_value()
            console.print(
                f"\nThe collection is worth €{sum_value}", style="success"
            )
        elif option == "0":     # exits program
            console.print(
                "\nThank you for using WoM Record Collection!",
                style="success",
            )
            sleep(3)
            break
        else:                   # print out to user that option is invalid
            console.print(
                "\nInvalid Option. Please Try Again", style="red bold"
            )
            sleep(3)
            main()


def add_id():
    """
    This function adds an numeric ID to each row in the first column
    in the sheet. This is being used by the other functions to keep
    track of what ID each item has. A process indicator is also being
    showed so that the user has an idea of how long the listing of
    the collection will take. When the adding of ID:s is done
    the create_table function is called.
    """

    console.print("\nPlease wait. Listing collection.", style="success")
    max_rows = len(collection.get_all_values())
    i = 1
    with Progress() as progress:
        task = progress.add_task("[green]Processing...", total=max_rows)
        while i < max_rows:
            collection.update_cell(i, 1, (i))
            i += 1
            progress.update(task, advance=1)
    collection.update_cell(i, 1, (i))
    data = collection.get_all_values()
    create_table(data)


def create_table(data):
    """
    This function creates the table. First it plots the
    columns and then it plots out all the rows in the
    data collection (from the collection sheet)
    """

    table = Table(box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("ID")
    table.add_column("Artist")
    table.add_column("Title")
    table.add_column("Label")
    table.add_column("Format")
    table.add_column("Value (€)")

    for row in data[0::1]:
        table.add_row(*row)

    os.system("clear")
    console.print(table)


def search_collection():
    """
    This function search for item in the record collection
    """


def add_item():
    """
    This function adds item to the record collection
    """

    os.system("clear")

    while True:
        console.print(
            "\nTo add an item to the record collection,follow these"
            "\ninstructions (or choose 0 to return to main menu):",
            style="bold cyan",
        )
        console.print(
            "\n* Add all columns with comma separation"
            "\n(Artist,Title,Label,Format,Value)",
            style="cyan",
        )
        console.print(
            "\n* Example: Shield,Vampiresongs,Desperate Fight Records,"
            "\nCD,50", style="cyan"
        )

        user_input = input("\nAdd data: \n")
        user_data = list(user_input.split(","))
        if user_input == "0":
            console.print(
                "\nHeading back to main menu", style="success"
            )
            sleep(3)
            os.system("clear")
            console.print(f"{WELCOME}", style="dark_orange3")
            show_menu()
            break
        elif len(user_data) != 5:
            console.print(
                "\nExactly 5 values are required. Please try again",
                style="error",
            )
            sleep(3)
        else:
            worksheet_to_update = SHEET.worksheet("collection")
            user_data.insert(0, '0')
            console.print("\nUpdating worksheet.", style="success")
            sleep(2)

            # converts string numbers in list to integers - taken from
            # https://www.geeksforgeeks.org/python-convert-numeric-string-to-integers-in-mixed-list/
            new_row_converted = [
                int(ele) if ele.isdigit() else ele for ele in user_data
            ]

            # adds new row to the end of the current data
            worksheet_to_update.append_row(new_row_converted)
            add_id()
            break


def edit_item():
    """
    This function changes item in the record collection
    """

    os.system("clear")
    data = collection.get_all_values()
    create_table(data)

    while True:
        option = input("\nEnter ID for row to edit (0 for main menu): \n")
        option = option.strip()

        if option == "0":
            console.print(
                "\nHeading back to main menu", style="success"
            )
            sleep(3)
            os.system("clear")
            console.print(f"{WELCOME}", style="dark_orange3")
            show_menu()
            break
        elif validate_max_rows(option):
            while True:
                os.system("clear")
                data = collection.row_values(option)
                table = Table(box=box.MINIMAL_DOUBLE_HEAD)
                table.add_column("Artist")
                table.add_column("Title")
                table.add_column("Label")
                table.add_column("Format")
                table.add_column("Value (€)")
                table.add_row(data[1], data[2], data[3], data[4], data[5])
                console.print(table)
                console.print(
                    f"\nTo edit {data[2]} by {data[1]}, please choose a cell"
                    "\nto edit\n"
                    "\n1. Artist, 2. Title, 3.Label, 4. Format, 5. Value"
                    "\n0. Back to change menu", style="bold cyan"
                )
                user_input = input("\nChoose cell to edit: \n")

                if user_input == "0":
                    console.print(
                        "\nHeading back to change menu", style="success"
                    )
                    sleep(3)
                    os.system("clear")
                    console.print(f"{WELCOME}", style="dark_orange3")
                    edit_item()
                    break
                elif user_input == "1":
                    edit_collection(option, user_input)
                elif user_input == "2":
                    edit_collection(option, user_input)
                elif user_input == "3":
                    edit_collection(option, user_input)
                elif user_input == "4":
                    edit_collection(option, user_input)
                elif user_input == "5":
                    edit_collection(option, user_input)
                else:
                    console.print("Please choose a number between 0 and 5",
                                  style="error")
                    sleep(2)


def remove_item():
    """
    This function removes item in the record collection
    """

    os.system("clear")
    data = collection.get_all_values()
    create_table(data)

    while True:
        option = input("\nEnter ID for row to remove (0 for main menu): \n")
        option = option.strip()
        if option == "0":
            console.print(
                "\nHeading back to main menu", style="success"
            )
            sleep(3)
            os.system("clear")
            console.print(f"{WELCOME}", style="dark_orange3")
            show_menu()
            break
        elif validate_max_rows(option):
            user_confirm = input("\nAre you sure? ").lower()

            if user_confirm == "n":
                console.print("Aborting...", style="error")
                sleep(2)
                remove_item()

            elif user_confirm == "y":
                console.print(f"Removing row with ID {option}", style="error")
                sleep(1)
                cell = collection.find(option, in_column=1)
                row = cell.row
                collection.delete_rows(row)
                data = collection.get_all_values()
                create_table(data)
                break
            else:
                console.print("Invalid input. Please try again", style="error")
                sleep(1)


def sort_collection():
    """
    Sorting collection based on users choice of sorting
    credentials. The function also creates a new table.
    The reason is that the user should not be able to
    sort the data based on ID.
    """

    os.system("clear")
    data = collection.get_all_values()
    create_table(data)
    while True:
        console.print(
            "\nPlease choose a sorting credential.",
            style="success",
        )
        console.print("\n1. Artist", style="cyan")
        console.print("2. Title", style="cyan")
        console.print("3. Label", style="cyan")
        console.print("4. Format", style="cyan")
        console.print("5. Value", style="cyan")
        console.print("0. Back to main menu", style="cyan")

        sorting_credential = input("\nEnter your choice: \n")
        sorting_credential = sorting_credential.strip()
        if sorting_credential == "0":
            console.print(
                "\nHeading back to main menu", style="success"
            )
            sleep(3)
            os.system("clear")
            console.print(f"{WELCOME}", style="dark_orange3")
            show_menu()
            break
        elif validate_data(sorting_credential):
            console.print("\nPlease wait. Sorting collection.",
                          style="success")
            sleep(2)
            sorting_credential = int(sorting_credential)
            sorting_credential += 1
            collection.sort((sorting_credential, "asc"))
            data = collection.get_all_values()
            create_table(data)


def calculate_total_value():
    """
    Calculate the total value of record collection.
    """
    console.print(
        "\nPlease wait. Calculating total value of the record collection.",
        style="success",
    )
    sleep(2)
    value_data = collection.col_values(6)
    value_data = list(map(int, value_data))
    sum_value = sum(value_data)
    os.system("clear")
    return sum_value


def edit_collection(row, column):
    """
    This function updates a specific cell based on input
    from user.
    """

    new_value = input("\nPlease add new value: \n")
    column = int(column)
    column += 1
    worksheet_to_update = SHEET.worksheet("collection")
    worksheet_to_update.update_cell(row, column, new_value)
    console.print("\nUpdating cell.", style="success")
    sleep(2)
    edit_item()


def validate_max_rows(option):
    """
    Validation function that converts string values to integers.
    If sorting crentials is larger than 5 or if the value cannot
    be converted to an integer an error is raised.
    """

    max_rows = len(collection.get_all_values())
    try:
        if int(option) > max_rows:
            raise ValueError(
                f"Only numbers within the ID range! You provided {option}"
            )

    except ValueError as error_message:
        console.print(
            f"Invalid data: {error_message}. Please try again.\n",
            style="red bold",
        )
        sleep(3)
        return False
    return True


def validate_data(user_choice):
    """
    Validation function that converts string values to integers.
    If sorting crentials is larger than 5 or if the value cannot
    be converted to an integer an error is raised.
    """

    try:
        if int(user_choice) > 5:
            raise ValueError(
                f"Only numbers between 0-5! You provided {user_choice}"
            )

    except ValueError as error_message:
        console.print(
            f"Invalid data: {error_message}. Please try again.\n",
            style="red bold",
        )
        sleep(3)
        return False
    return True


def main():
    """
    Clear terminal, print WELCOME and
    run relevant functions to start
    application.
    """

    os.system("clear")
    console.print(f"{WELCOME}", style="dark_orange3")
    show_menu()


main()
