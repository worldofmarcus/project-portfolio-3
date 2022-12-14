"""Import relevant modules for the application"""

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
custom_theme = Theme({"error": "bold red3", "success": "bold green3"})
console = Console(theme=custom_theme)

WELCOME = """
*** WOM RECORD COLLECTION***
WOM keeps track on your record collection!
Use the menu below to start using the application!
"""


def show_menu():
    """
    Function prints out the menu, waits for the user input
    and then calls the relevant function. Validation of users
    choice is also being made.
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
                f"Collections value is ???{sum_value}", style="success"
            )
        elif option == "0":  # exits program
            console.print(
                "\nThank you for using WOM Record Collection!",
                style="success",
            )
            sleep(1)
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
            sleep(1)
            main()


def add_id():
    """
    This function adds a numeric ID to each row in the first column
    in the sheet. This is being used by the other functions to keep
    track of what ID each item has. A process indicator is also being
    showed so that the user has an idea of how long the listing of
    the collection will take. When the adding of ID:s is done
    the create_table function is called. Convert to uppercase in list
    of lists taken (and slightly modified) from Stack Overflow:
    https://stackoverflow.com/questions/54438770/lowercase-a-list-of-lists

    """

    console.print("\nPlease wait. Listing collection.", style="success")
    collection = SHEET.worksheet("collection")
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
    )
    create_table(data)


def create_table(data):
    """
    This function creates the table. First it plots the
    columns and then it plots out all the rows in the
    data collection (from the collection sheet). Inspiration
    on importing Google Sheet to Rich table was taken from
    Stack Overflow: https://stackoverflow.com/questions/71799108/
    how-do-i-zip-a-list-of-lists-into-a-python-rich-table-with-
    headers-and-rows
    """

    table = Table(box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("ID")
    table.add_column("ARTIST")
    table.add_column("TITLE")
    table.add_column("LABEL")
    table.add_column("FORMAT")
    table.add_column("VALUE (???)")
    for row in data[0::1]:
        table.add_row(*row)
    os.system("clear")
    console.print(table)


def search_item():
    """
    This function allows the user to search for a specific item
    in the collection. The user can search for anything and if
    the item exists in the collection it's being printed in a table
    (this works for multiple matches as well).
    """

    collection = SHEET.worksheet("collection")
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
            table.add_column("VALUE (???)")
            for row in matches[0::1]:
                table.add_row(*row)
            os.system("clear")
            console.print(table)
            rows = len(matches)
            if rows == 0:
                console.print(f"\nNo match on {user_input}! Please try "
                              "again\n", style="error")
                sleep(1)
            else:
                pass
            search_item()


def add_item():
    """
    This function lets the user add an item to the record collection.
    It also checks for valid input for each cell input to secure that
    not invalid data is being sent to the Google Sheet. Before updating
    the Google Sheet the function accumulate data is being called to
    merge all the valid user input.
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
                sleep(1)
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
                if user_value < 0:
                    console.print(
                        "You need to provide a positive number! "
                        "Please try again!", style="error"
                    )
                else:
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
        sleep(1)
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
    This function let's the user edit a specific item in the collection
    by choosing the ID for the item (or choose '0' to get back to the main
    menu). When the user has provided the ID the user needs to choose a value
    to edit. When the user feeds in the input the update cell function is
    being called for validation to secure that not empty content (or negative
    numbers for the value cell) is being exported to the Google Sheet.
    If the user input is correct it is being exported to the Google Sheet and
    then the table updates.
    """

    os.system("clear")
    add_id()
    collection = SHEET.worksheet("collection")
    data = collection.get_all_values()
    while True:
        option = input("\nEnter ID for row to edit (0 for main menu): \n")
        option = option.strip()
        if option == "0":
            console.print("\nHeading back to main menu", style="success")
            sleep(1)
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
                table.add_column("VALUE (???)")
                table.add_row(data[1].upper(), data[2].upper(),
                              data[3].upper(), data[4].upper(),
                              data[5])
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
                    sleep(1)
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
                    sleep(1)


def remove_item():
    """
    This function lets the user remove a specific item from the collection
    It first lists the collection and then ask the user to enter the ID
    connected to the row that is in scope for deletion. The user can also
    choose '0' to head back to the main menu. When the user has provided
    the ID, the application checks for a valid input and then asks the user
    for deletion confirmation. If they choose 'N', the action will be aborted
    and the user is being redirected to the remove menu. If they choose 'Y',
    the item is being removed, the collection is being listed and the main
    menu is being printed.
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
            sleep(1)
            os.system("clear")
            console.print(f"{WELCOME}", style="dark_orange3")
            show_menu()
            break
        elif validate_max_rows(option):
            user_confirm = input("\nAre you sure?(Y/N) ").upper()
            if user_confirm == "N":
                console.print("Aborting...", style="error")
                sleep(1)
                remove_item()
                break
            elif user_confirm == "Y":
                console.print(
                    f"Removing row with ID {option}", style="error"
                )
                sleep(1)
                collection = SHEET.worksheet("collection")
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
    This function lets the user sort the collection based on
    the users choice of sorting credential. The function also
    creates a new table and prints the table based on the users
    sorting credential. The table doesn't print out the ID column
    because the user should not be able to sort on ID. The function
    also checks for valid input to secure that the sorting
    credential is correct. When the sorting has been made the user
    is being redirected to the sorting menu. Convert to uppercase in list
    of lists taken (and slightly modified) from Stack Overflow:
    https://stackoverflow.com/questions/54438770/lowercase-a-list-of-lists
    """

    os.system("clear")
    add_id()
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
            sleep(1)
            os.system("clear")
            console.print(f"{WELCOME}", style="dark_orange3")
            show_menu()
            break
        elif validate_data(sorting_credential):
            console.print(
                "\nPlease wait. Sorting collection.", style="success"
            )
            sleep(1)
            sorting_credential = int(sorting_credential)
            sorting_credential += 1
            collection = SHEET.worksheet("collection")
            collection.sort((sorting_credential, "asc"))
            data = collection.get_all_values()
            data = list(map(lambda x: list(map(lambda y: y.upper(), x)), data))
            create_table(data)


def calculate_total_value():
    """
    This function checks all values in the value column and
    convert them to integers. Then the total sum is being
    calculated and stored in the sum_value variable which
    then is being returned.
    """
    console.print(
        "\nPlease wait. Calculating total value of the collection.",
        style="success",
    )
    sleep(2)
    collection = SHEET.worksheet("collection")
    value_data = collection.col_values(6)
    value_data_converted = list(map(int, value_data))
    sum_value = sum(value_data_converted)
    os.system("clear")
    return sum_value


def update_cell(row, column):
    """
    This function updates a specific cell based on input
    from user. Before updating the cell a validation of the
    data is being made (check for empty string, int or not int
    and negative number). This is to secure that no invalid data
    is being exported to the Google Sheet.
    """

    while True:
        new_value = input("\nPlease add new value: \n").upper()
        new_value = new_value.strip()
        if column == "5":
            try:
                new_value = int(new_value)
                if new_value < 0:
                    console.print(
                        "You need to provide a positive number! "
                        "Please try again!", style="error"
                    )
                else:
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
    sleep(1)
    edit_item()


def validate_max_rows(option):
    """
    Validation function that converts the recieved value option
    from the function edit_value to an integer and then checks
    if the option is within the max row in the sheet and if the
    value can be converted to an integer. If not, an error is raised.
    It also checks for negative numbers to secure valid data is being
    exported to the Google Sheet.
    """

    collection = SHEET.worksheet("collection")
    max_rows = len(collection.get_all_values())
    try:
        if int(option) > max_rows or int(option) < 0:
            raise ValueError(
                f"Only numbers within the ID range! You provided {option}"
            )
    except ValueError as error_message:
        console.print(
            f"Invalid data: {error_message}. Please try again.\n",
            style="red3 bold",
        )
        sleep(1)
        return False
    return True


def validate_data(user_choice):
    """
    Validation function that converts the recieved value user_choice
    to an integer. If user_choice is larger than 5, a negative number,
    or if the value cannot be converted to an integer an error is raised.
    """

    try:
        if int(user_choice) > 5 or int(user_choice) < 0:
            raise ValueError(
                f"Only numbers between 0-5! You provided {user_choice}"
            )
    except ValueError as error_message:
        console.print(
            f"Invalid data: {error_message}. Please try again.\n",
            style="red3 bold",
        )
        sleep(1)
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
