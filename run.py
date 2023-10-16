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


def get_revenue_input():
    """
    Function to have revenue and month data inputted from the user
    """
    print(Fore.GREEN+'Please, use the following examples to enter revenue date:')
    print(Fore.GREEN+'Please enter the "month" in the format "january"')
    print(Fore.GREEN+'Please enter the "value" of daily revenue in the format "1.05"')

    month_inf = input('Enter the month here:').lower()      
    revenue_data = float(input('Enter the revenue value here:'))     

    print(Fore.BLUE+f'Month and revenue provided were: "{month_inf}"; "{revenue_data}"')        


get_revenue_input()    