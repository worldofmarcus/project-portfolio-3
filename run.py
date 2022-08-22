"""Import modules"""

import os
import sys
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

custom_theme = Theme({"error": "bold red3", "success": "bold green3"})
console = Console(theme=custom_theme)

WELCOME = """
*** WOM RECORD COLLECTION***
WOM keeps track on your record collection!
Use the menu below to start using the application!
"""


def show_menu():
    """
    Function prints out the menu and get the user input.
    Validation of users choice is also being made.
    """

    while True:
        print("\n")
        console.print("1: List collection", style="cyan2")
        console.print("2: Search item in collection", style="cyan2")
        console.print("3: Add item to collection", style="cyan2")
        console.print("4: Edit item in collection", style="cyan2")
        console.print("5: Remove item from collection", style="cyan2")
        console.print("6: Sort collection", style="cyan2")
        console.print("7: Show total value of collection", style="cyan2")
        console.print("0: Exit application", style="cyan2")

        option = input("\nEnter your choice: \n")
        option = option.strip()
        if option == "1":  # call function 'list_collection'
            add_id()
        elif option == "2":  # call function 'search_item'
            search_item()
        elif option == "3":  # call function 'add item'
            add_item()
        elif option == "4":  # call function 'edit item'
            edit_item()
        elif option == "5":  # call function 'remove item'
            remove_item()
        elif option == "6":  # call function 'sort_collection'
            sort_collection()
        elif option == "7":  # call function 'calculate_total_value'
            sum_value = calculate_total_value()
            console.print(
                f"Collections value is €{sum_value}", style="success"
            )
        elif option == "0":  # exits program
            console.print(
                "\nThank you for using WoM Record Collection!",
                style="success",
            )
            sleep(2)
            console.print(
                "\nApplication has shutdown. Use the RUN PROGRAM button if"
                "\nyou want to restart the app.",
                style="success",
            )
            sys.exit()
        else:  # print out to user that option is invalid
            console.print(
                "\nInvalid Option. Please provide a number between 0 - 7",
                style="red3 bold"
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
        task = progress.add_task("[green3]Processing...", total=max_rows)
        while i < max_rows:
            collection.update_cell(i, 1, (i))
            i += 1
            progress.update(task, advance=1)
    collection.update_cell(i, 1, (i))
    data = collection.get_all_values()
    data = list(
        map(lambda x: list(map(lambda y: y.upper(), x)), data)
    )  # Change all strings to uppercase
    create_table(data)


def create_table(data):
    """
    This function creates the table. First it plots the
    columns and then it plots out all the rows in the
    data collection (from the collection sheet)
    """

    table = Table(box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("ID")
    table.add_column("ARTIST")
    table.add_column("TITLE")
    table.add_column("LABEL")
    table.add_column("FORMAT")
    table.add_column("VALUE (€)")

    for row in data[0::1]:
        table.add_row(*row)

    os.system("clear")
    console.print(table)


def search_item():
    """
    This function search for item in the record collection
    Allows the user to search for a specific item. The user
    can search for anything and if the item exists in the
    collection it's being printed in a table (this works
    for multiple matches as well)
    """

    data = collection.get_all_values()
    data = list(map(lambda x: list(map(lambda y: y.upper(), x)), data))
    matches = []
    console.print("\nInput your search credentials below. "
                  "0 for main menu", style="cyan2")

    while True:
        user_input = input("\nInput your search credential: \n").upper()
        user_input = user_input.strip()

        if user_input == "0":
            console.print("\nHeading back to main menu", style="success")
            sleep(3)
            os.system("clear")
            console.print(f"{WELCOME}", style="dark_orange3")
            show_menu()

        elif not user_input:
            console.print(
                "You did not provide any information. "
                "Please try again.",
                style="error"
            )

        else:
            for match in data:
                if user_input in match:
                    matches.append(match)

            table = Table(box=box.MINIMAL_DOUBLE_HEAD)
            table.add_column("ID")
            table.add_column("ARTIST")
            table.add_column("TITLE")
            table.add_column("LABEL")
            table.add_column("FORMAT")
            table.add_column("VALUE (€)")
            for row in matches[0::1]:
                table.add_row(*row)
            os.system("clear")
            console.print(table)

            rows = len(matches)
            if rows == 0:
                console.print(f"\nNo match on {user_input}! Please try "
                              "again\n", style="error")
                sleep(2)
            else:
                pass
            search_item()


def add_item():
    """
    This function adds item to the record collection. It also checks for
    valid input for each cell input to secure that not empty strings are
    being sent to the Google Sheet.
    """
    os.system("clear")
    add_id()
    while True:

        while True:
            option = input("Do you want to add a new item (Y/N)? ").upper()
            if option == "N":
                console.print(
                    "\nHeading back to main menu", style="success"
                )
                sleep(3)
                os.system("clear")
                console.print(f"{WELCOME}", style="dark_orange3")
                show_menu()
                break
            elif option == "Y":
                break
            else:
                console.print("Please choose Y or N", style="error")

        while True:
            user_artist = input("\nAdd artist: \n").upper()
            if not user_artist.strip():
                console.print(
                    "You did not provide any artist information. "
                    "Please try again.",
                    style="error"
                )
            else:
                break

        while True:
            user_title = input("\nAdd title: \n").upper()
            if not user_title.strip():
                console.print(
                    "You did not provide any title information. "
                    "Please try again.",
                    style="error"
                )
            else:
                break

        while True:
            user_label = input("\nAdd label: \n").upper()
            if not user_label.strip():
                console.print(
                    "You did not provide any label information. "
                    "Please try again.",
                    style="error"
                )
            else:
                break
        while True:
            user_format = input("\nAdd format: \n").upper()
            if not user_format.strip():
                console.print(
                    "You did not provide any format information. "
                    "Please try again.",
                    style="error"
                )
            else:
                break

        while True:
            try:
                user_value = input("\nAdd value: \n")
                user_value.strip()
                user_value = int(user_value)
                break
            except ValueError:
                console.print(
                    "You need to provide a number! Please try again!",
                    style="error",
                )

        user_input = accumulate_input(
            user_artist, user_title, user_label, user_format, user_value
        )

        worksheet_to_update = SHEET.worksheet("collection")
        user_input.insert(0, "0")
        console.print("\nUpdating worksheet.", style="success")
        sleep(2)

        # adds new row to the end of the current data
        worksheet_to_update.append_row(user_input)
        add_id()


def accumulate_input(str1, str2, str3, str4, int1):
    """
    This function accumulate the users input from the add function to a list
    and then strips the strings in the list to remove blank spaces before
    and after the string. No need to strip the user_value, it has been
    handeled in the add function.
    """

    user_input = [
        str1.strip(),
        str2.strip(),
        str3.strip(),
        str4.strip(),
        int1,
    ]
    return user_input


def edit_item():
    """
    This function changes item in the record collection
    """

    os.system("clear")
    add_id()
    data = collection.get_all_values()

    while True:
        option = input("\nEnter ID for row to edit (0 for main menu): \n")
        option = option.strip()

        if option == "0":
            console.print("\nHeading back to main menu", style="success")
            sleep(3)
            os.system("clear")
            console.print(f"{WELCOME}", style="dark_orange3")
            show_menu()
        elif validate_max_rows(option):
            while True:
                os.system("clear")
                data = collection.row_values(option)
                table = Table(box=box.MINIMAL_DOUBLE_HEAD)
                table.add_column("ARTIST")
                table.add_column("TITLE")
                table.add_column("LABEL")
                table.add_column("FORMAT")
                table.add_column("VALUE (€)")
                table.add_row(data[1], data[2], data[3], data[4], data[5])
                console.print(table)
                console.print(
                    f"\nTo edit {data[2]} by {data[1]}, please choose the"
                    "\nvalue you want to edit.\n"
                    "\n1. Artist"
                    "\n2. Title"
                    "\n3. Label"
                    "\n4. Format"
                    "\n5. Value"
                    "\n0. Back to edit menu",
                    style="cyan2",
                )
                user_input = input("\nChoose cell to edit: \n")
                user_input = user_input.strip()

                if user_input == "0":
                    console.print(
                        "\nHeading back to edit menu", style="success"
                    )
                    sleep(3)
                    os.system("clear")
                    console.print(f"{WELCOME}", style="dark_orange3")
                    edit_item()
                elif user_input == "1":
                    update_cell(option, user_input)
                elif user_input == "2":
                    update_cell(option, user_input)
                elif user_input == "3":
                    update_cell(option, user_input)
                elif user_input == "4":
                    update_cell(option, user_input)
                elif user_input == "5":
                    update_cell(option, user_input)
                else:
                    console.print(
                        "Please choose a number between 0 and 5",
                        style="error",
                    )
                    sleep(2)


def remove_item():
    """
    This function removes item in the record collection
    """

    os.system("clear")
    add_id()
    while True:
        option = input(
            "\nEnter ID for row to remove (0 for main menu): \n"
        )
        option = option.strip()
        if option == "0":
            console.print("\nHeading back to main menu", style="success")
            sleep(3)
            os.system("clear")
            console.print(f"{WELCOME}", style="dark_orange3")
            show_menu()
            break
        elif validate_max_rows(option):
            user_confirm = input("\nAre you sure?(Y/N) ").upper()
            if user_confirm == "N":
                console.print("Aborting...", style="error")
                sleep(2)
                remove_item()
                break
            elif user_confirm == "Y":
                console.print(
                    f"Removing row with ID {option}", style="error"
                )
                sleep(1)
                cell = collection.find(option, in_column=1)
                row = cell.row
                collection.delete_rows(row)
                add_id()
                break
            else:
                console.print(
                    "Invalid input. Please choose ID to remove "
                    "again.", style="error"
                )
                sleep(1)


def sort_collection():
    """
    Sorting collection based on users choice of sorting
    credentials. The function also creates a new table.
    The reason is that the user should not be able to
    sort the data based on ID.
    """

    os.system("clear")
    add_id()
    data = collection.get_all_values()
    while True:
        console.print(
            "\nPlease choose a sorting credential.",
            style="success",
        )
        console.print("\n1. Artist", style="cyan2")
        console.print("2. Title", style="cyan2")
        console.print("3. Label", style="cyan2")
        console.print("4. Format", style="cyan2")
        console.print("5. Value", style="cyan2")
        console.print("0. Back to main menu", style="cyan2")

        sorting_credential = input("\nEnter your choice: \n")
        sorting_credential = sorting_credential.strip()
        if sorting_credential == "0":
            console.print("\nHeading back to main menu", style="success")
            sleep(3)
            os.system("clear")
            console.print(f"{WELCOME}", style="dark_orange3")
            show_menu()
            break
        elif validate_data(sorting_credential):
            console.print(
                "\nPlease wait. Sorting collection.", style="success"
            )
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


def update_cell(row, column):
    """
    This function updates a specific cell based on input
    from user.
    """

    while True:
        print(column)
        new_value = input("\nPlease add new value: \n").upper()
        new_value = new_value.strip()

        if column == "5":
            try:
                new_value = int(new_value)
                break
            except ValueError:
                console.print(
                    "You need to provide a number! Please try again!",
                    style="error"
                )
        elif not new_value:
            console.print(
                "You did not provide any information. "
                "Please try again.",
                style="error"
            )

        else:
            break

    column = int(column)
    column += 1
    worksheet_to_update = SHEET.worksheet("collection")
    worksheet_to_update.update_cell(row, column, new_value)
    console.print("\nUpdating cell.", style="success")
    sleep(2)
    edit_item()


def validate_max_rows(option):
    """
    Validation function that converts the recieved value option
    from the function edit_value to an integer and then checks
    if the option is within the max row in the sheet and if the
    value can be converted to an integer. If not, an error is raised.
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
            style="red3 bold",
        )
        sleep(3)
        return False
    return True


def validate_data(user_choice):
    """
    Validation function that converts the recieved value user_choice
    to an integer. If user_choice is larger than 5 or if the value
    cannot be converted to an integer an error is raised.
    """

    try:
        if int(user_choice) > 5:
            raise ValueError(
                f"Only numbers between 0-5! You provided {user_choice}"
            )

    except ValueError as error_message:
        console.print(
            f"Invalid data: {error_message}. Please try again.\n",
            style="red3 bold",
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
