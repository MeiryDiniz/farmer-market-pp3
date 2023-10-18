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
    Function to have revenue and expense data inputted from the user.
    A while loop runs to keep program running while correct data is not 
    inputted by the user. Data inputted is passed to the 
    validate_month_input(data) function to be validated.
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
    print(Fore.MAGENTA+f'Data inputted is valid: Month: \
"{month_input_revenue}" and Revenue: "{revenue_input}"!')

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
    print(Fore.MAGENTA+f'Data inputted is valid: Month: \
"{month_input_expense}" and Expense: "{expense_input}"!')
    return month_input_revenue, revenue_input, month_input_expense, expense_input


def validate_month_input(data):
    """
    Check data inputted for month_input_revenue and  month_input_expense
    in the get_worksheet_data function, and raises a ValueError if data 
    does not match with data asked.
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
    Check data inputted for revenue_input and expense_input in the
    get_worksheet_data function, convert data to a float number and 
    raises a ValueError if data does not match with data asked.
    """
    try:
        revenue_data = float(data)
        if revenue_data < 0:
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


def worksheet_sum(worksheet):
    """
    Function to sum the values inputted in the worksheets.
    """
    worksheet_sum_revenue = SHEET.worksheet(worksheet)
    months = worksheet_sum_revenue.row_values(1)

    sum_values = []
    for month_index in range(1, len(months) + 1):
        column_data = worksheet_sum_revenue.col_values(month_index)[1:]  # Exclude the header row
        numeric_values = [float(value) if value != '' else 0 for value in column_data]
        column_sum = sum(numeric_values)
        sum_values.append(column_sum)

    return sum_values


def add_profit_data(data, worksheet):
    """
    Function to add data to the profit worksheet.
    """
    print(f'{Fore.CYAN}The {worksheet} is being updated!')
    profit_worksheet = SHEET.worksheet(worksheet)
    months = profit_worksheet.col_values(1)
    month_index = months.index(data[0]) + 1
    col_data = profit_worksheet.row_values(month_index)
    last_col = len(col_data) + 1
    profit_worksheet.update_cell(month_index, last_col, data[1])

    print(Fore.MAGENTA+'Data was updated successfuly!')    


def main():
    """
    Run all program functions.
    """
    data = get_worksheet_data()
    month_input_revenue = data[0]
    revenue_input = data[1]
    month_input_expense = data[2]
    expense_input = data[3]
    add_worksheet_data((month_input_revenue, revenue_input), 'revenue')
    add_worksheet_data((month_input_expense, expense_input), 'expenses')

    worksheet_sum_revenue = SHEET.worksheet('revenue')
    months = worksheet_sum_revenue.row_values(1)
    revenue_sums = worksheet_sum('revenue')
    print("Sum values for each column in the 'revenue' worksheet:")
    for month, sum_value in zip(months, revenue_sums):
        sum_revenue_formatted = round(sum_value, 2)
        print(f"{month}: {sum_revenue_formatted}")

    worksheet_data_expense = SHEET.worksheet('expenses')
    expense_months = worksheet_data_expense.row_values(1)  
    expense_sums = worksheet_sum('expenses')
    print("Sum values for each column in the 'expenses' worksheet:")
    for month, sum_value in zip(expense_months, expense_sums):
        sum_expense_formatted = round(sum_value, 2)
        print(f"{month}: {sum_expense_formatted}") 

    add_profit_data(sum_revenue_formatted, 'profit')    
    add_profit_data(sum_expense_formatted, 'profit')


print(Back.BLACK + Fore.MAGENTA + '\033[1m'+"Welcome to Farmer Market \
Automation!'\033[0m'\n")
print(Back.BLACK + Fore.MAGENTA + '\033[1m'+"The program will help you to \
deal with expenses and revenue data, and so, calculating the profit of your \
farmer market.'\033[0m'\n")
main()
