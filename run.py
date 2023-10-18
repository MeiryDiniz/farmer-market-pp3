import pandas as pd
from pprint import pprint
import gspread
from google.oauth2.service_account import Credentials
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('farmer-market')


def get_worksheet_data():
    """
    Function to have revenue and month data inputted from the user,
    and run a while loop to have a correct data inputted by the
    user. With that the program will keep running just when the correct 
    data is inputted.
    """

# Add data to 'revenue' worksheet
    while True:
        print('Please, use the following examples to enter revenue \
date:\n')
        print(Fore.BLUE+'Please enter the "month" in the format "january".\n')

        month_input_revenue = input(
            Fore.GREEN+'Enter the month here:\n').lower()
        if validate_month_input(month_input_revenue):
            break

    while True:
        print(Fore.BLUE+'Please enter the "value" of daily revenue in the \
format "1.05" or "4" for whole numbers.\n')

        revenue_input = (input(Fore.GREEN+'Enter the revenue value here:\n'))
        if validate_value_input(revenue_input):
            break
    print(Fore.MAGENTA+f'Data inputted is valid: Month: "{month_input_revenue}"\
and Revenue: "{revenue_input}"!')

# Add data to 'expenses' worksheet
    while True:
        print('Please, use the following examples to enter expenses \
date:\n')
        print(Fore.BLUE+'Please enter the "month" in the format "january".\n')

        month_input_expense = input(
            Fore.GREEN+'Enter the month here:\n').lower()
        if validate_month_input(month_input_expense):
            break

    while True:
        print(Fore.BLUE+'Please enter the "value" of daily expenses in the \
format "1.05" or "4" for whole numbers.\n')

        expense_input = (input(Fore.GREEN+'Enter the expense value here:\n'))
        if validate_value_input(expense_input):
            break
    print(Fore.MAGENTA+f'Data inputted is valid: Month: "{month_input_expense}"\
and Expense: "{expense_input}"!')
    return month_input_revenue, revenue_input, month_input_expense, expense_input


def validate_month_input(data):
    """
    Check the data inputted for month_input in the get_worksheet_data
    function and raises a ValueError if data does not match with data asked
    """
    try:
        worksheet_data = SHEET.worksheet('revenue').get_all_values()
        if not any([data.lower() in col for col in zip(*worksheet_data)]):
            raise ValueError(Fore.RED+f'You provided "{data}", \
please provide a valid month')
    except ValueError as e:
        print(Fore.RED+f'Invalid data: {e}. Please try again.\n')
        return False

    return True


def validate_value_input(data):
    """
    Check the data inputted for revenue_input in the 
    get_worksheet_data function, convert data 
    to a float number and raises a ValueError if data does 
    not match with data asked
    """
    try:
        revenue_data = float(data)
        if revenue_data <= 0:
            raise ValueError
    except ValueError as e:
        print(Fore.RED+f'Invalid data: {e}Please enter the "value" of daily \
revenue in the format "1.05" or "4" for whole numbers.\n')
        return False

    return True


def add_worksheet_data(data, worksheet):
    """
    Function to add data to the correct worksheet
    according to the data inputted.
    """
    print(f'{Fore.CYAN}The {worksheet} are being updated!')
    worksheet_data = SHEET.worksheet(worksheet)
    months = worksheet_data.row_values(1)
    month_index = months.index(data[0]) + 1
    row_data = worksheet_data.col_values(month_index)
    last_row = len(row_data) + 1
    worksheet_data.update_cell(last_row, month_index, data[1])

    print(Fore.MAGENTA+'Data was updated successfuly!')


# data_revenue_worksheet = get_worksheet_data()
# month_input_revenue = data_revenue_worksheet[0]
# revenue_input = data_revenue_worksheet[1]
# data_worksheet_expenses = get_worksheet_data()
# month_input_expense = data_worksheet_expenses[0]
# expense_input = data_worksheet_expenses[1]
data = get_worksheet_data()
month_input_revenue = data[0]
revenue_input = data[1]
month_input_expense = data[2]
expense_input = data[3]
add_worksheet_data((month_input_revenue, revenue_input), 'revenue')
add_worksheet_data((month_input_expense, expense_input), 'expenses')

# def main():
#     """
#     Run all program functions.
#     """


# print(Back.MAGENTA + Fore.BLACK + 'Welcome to Farmer Market Automation! \
# The program will help you to deal with expenses and revenue data, \
# and so, calculating the profit of your farmer market.')
# main()
