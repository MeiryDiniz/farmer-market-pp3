import pandas as pd
from pprint import pprint
import gspread
from google.oauth2.service_account import Credentials
import colorama
from colorama import Fore, Back, Style
from datetime import datetime
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


def get_revenue_input():
    """
    Function to have date and revenue value input from the user
    """
    print(Fore.GREEN+'Please, use the following examples to enter revenue date:')
    print(Fore.GREEN+'Please enter the "date" in the format "YYYY-MM-DD"')
    print(Fore.GREEN+'Please enter the "value" of daily revenue in the format "1.05"')

    date_inf = input('Enter the date here:')
    date_added = datetime.strptime(date_inf, '%Y-%m-%d').date()
    worksheet_to_input = SHEET.worksheet('revenue')

    revenue_data = input('Enter the revenue value here:')
    revenue_value = float(revenue_data)

    row_to_append = [str(date_added), revenue_value]
    worksheet_to_input.append_row(row_to_append)

    print(f'Date "{date_added}" and "{revenue_value}" added successfully')

    return worksheet_to_input    


get_revenue_input()    