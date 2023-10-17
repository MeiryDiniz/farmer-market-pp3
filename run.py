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
    Function to have revenue and month data inputted from the user
    """
    print(Fore.GREEN+'Please, use the following examples to enter revenue date:')
    print(Fore.GREEN+'Please enter the "month" in the format "january"')
    print(Fore.GREEN+'Please enter the "value" of daily revenue in the format "1.05"')

    month_inf = input('Enter the month here:').lower()
    revenue_data = float(input('Enter the revenue value here:'))
    validate_input_data(month_inf)
    

def validate_input_data(data):
    """
    Check the data inputted in the get_revenue_worksheet_input 
    function and raises a ValueError if data does not match with
    data asked 
    """
    try:
        values = SHEET.worksheet('revenue').get_all_values()
        if not any([data.lower() in col for col in zip(*values)]):
            raise ValueError(
                f'You provided "{data}", please provide a valid month')

    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')


get_revenue_worksheet_input()
