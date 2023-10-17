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


def get_revenue_worksheet_input():
    """
    Function to have revenue and month data inputted from the user,
    and run a while loop to have a correct data inputted by the
    user. With that the program will keep running just when the correct 
    data is inputted.
    """
    while True:
        print(Fore.GREEN+'Please, use the following examples to enter revenue \
date:\n')
        print(Fore.GREEN+'Please enter the "month" in the format "january".\n')

        month_input = input(Fore.BLUE+'Enter the month here:').lower()
        if validate_month_input(month_input):
            break

    while True:
        print(Fore.GREEN+'Please enter the "value" of daily revenue in the \
format "1.05" or "4" for whole numbers.\n')

        revenue_input = (input(Fore.BLUE+'Enter the revenue value here:'))
        if validate_revenue_input(revenue_input):
            break
    print(Fore.MAGENTA+f'Data inputted is valid: Month: "{month_input}" and \
Revenue: "{revenue_input}"!')
    return month_input, revenue_input


def validate_month_input(data):
    """
    Check the data inputted for month_input in the get_revenue_worksheet_input
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


def validate_revenue_input(data):
    """
    Check the data inputted for revenue_input in the 
    get_revenue_worksheet_input function, convert data 
    to a float number and raises a ValueError if data does 
    not match with data asked
    """
    try:
        revenue_data = float(data)
        if revenue_data <= 0:
            raise ValueError
    except ValueError:
        print(Fore.RED+f'Invalid data: Please enter the "value" of daily \
revenue in the format "1.05" or "4" for whole numbers.\n')
        return False

    return True


get_revenue_worksheet_input()
