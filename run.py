import gspread
from google.oauth2.service_account import Credentials
import colorama
from colorama import Fore, Back, Style 
colorama.init(autoreset=True)
import pandas as pd 
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('farmer-market')

print(Fore.BLUE+Back.WHITE+'Hello!')

worksheet_to_print = SHEET.worksheet('profit')
data = worksheet_to_print.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

print(df)