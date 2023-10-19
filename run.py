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
        print('\033[1mPlease, use the following examples to enter \
revenue date:\033[0m\n')
        print(Fore.BLUE+'Please enter the "month" in the format "january".\n')

        month_input_revenue = input(
            Fore.GREEN+'Enter the month here:').lower()
        if validate_month_input(month_input_revenue):
            break

    while True:
        print(Fore.BLUE+'Please enter the "value" of daily revenue in the \
format "1.05" or "4" for whole numbers.\n')

        revenue_input = (input(Fore.GREEN+'Enter the revenue value here:'))
        if validate_value_input(revenue_input):
            break
    print(Fore.MAGENTA+f'Data inputted is valid: Month: \
"{month_input_revenue}" and Revenue: "{revenue_input}"!\n')

# Add data to 'expenses' worksheet
    while True:
        print('\033[1mPlease, use the following examples to enter \
expenses date:\033[0m\n')
        print(Fore.BLUE+'Please enter the "month" in the format "january" \
without quotes.\n')

        month_input_expense = input(
            Fore.GREEN+'Enter the month here:').lower()
        if validate_month_input(month_input_expense):
            break

    while True:
        print(Fore.BLUE+'Please enter the "value" of daily expenses in the \
format "1.05" or "4" for whole numbers, without quotes.\n')

        expense_input = (input(Fore.GREEN+'Enter the expense value here:'))
        if validate_value_input(expense_input):
            break
    print(Fore.MAGENTA+f'Data inputted is valid: Month: \
"{month_input_expense}" and Expense: "{expense_input}"!\n')

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
revenue in the format "1.05" or "4" for whole numbers, without quotes.\n')
        return False

    return True


def add_worksheet_data(data, worksheet):
    """
    Function to add data to the correct worksheet
    according to the data inputted.
    """
    print(f'{Fore.CYAN}The {worksheet} are being updated!\n')
    worksheet_data = SHEET.worksheet(worksheet)
    months = worksheet_data.row_values(1)
    month_index = months.index(data[0]) + 1
    row_data = worksheet_data.col_values(month_index)
    last_row = len(row_data) + 1
    worksheet_data.update_cell(last_row, month_index, data[1])

    print(f'{Fore.MAGENTA}The {worksheet} has being updated successfuly!\n')


def worksheet_sum(worksheet):
    """
    Function to sum the values inputted in the worksheets.
    """
    print(f'{Fore.GREEN}Calculating {worksheet}...\n')
    worksheet = SHEET.worksheet(worksheet)
    months = worksheet.row_values(1)   

    sum_values = []
    for month_index in range(1, len(months) + 1):
        column_data = worksheet.col_values(month_index)[1:]  
        numeric_values = [float(value) if value != '' else 0 for value in column_data]
        column_sum = sum(numeric_values)
        sum_values.append(column_sum)

    print(f'{Fore.CYAN}The {worksheet.title} data has being calculated \
successfuly!\n')        

    return sum_values 
    

def append_worksheet_data(worksheet, values, column):
    """
    Function to append revenue and expenses sum to the 
    profit worksheet.
    """
    sum_worksheet_data = SHEET.worksheet(worksheet)    
    for i, value in enumerate(values):
        sum_worksheet_data.update_cell(i + 2, column, value)

# def profit_worksheet_data(data, worksheet):
#     print(Fore.GREEN+'Updating profit data...\n')
#     profit_worksheet = SHEET.worksheet(worksheet)
#     existing_data = profit_worksheet.get_all_values()
#     for i, value in enumerate(data, start=1):
#         profit_worksheet.update_cell(i + 1, 4, value)
#     print(Fore.CYAN+'Profit data has been calculated successfully!\n')    
    # months = profit_worksheet.col_values(1) 
    # worksheet_data = data.col_values()
    # profit_worksheet.append(worksheet_data[1:]) 

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

#  worksheet_sum(worksheet) function and 
# append_worksheet_data(worksheet, values, column) function      
    revenue_worksheet = "revenue"
    revenue_sums = worksheet_sum(revenue_worksheet)
    append_worksheet_data("profit", revenue_sums, 2)
    
    expenses_worksheet = "expenses"  
    expenses_sums = worksheet_sum(expenses_worksheet)
    append_worksheet_data("profit", expenses_sums, 3)
    

    # print(Fore.GREEN+'Updating profit data...\n')
    # revenue_sums = worksheet_sum("revenue")
    # expenses_sums = worksheet_sum("expenses")
    # profit_sum = [revenue_sums[i] - expenses_sums[i] for i in range(len(revenue_sums))]
    # profit_worksheet_data(profit_sum, "profit")

    # revenue_sums = worksheet_sum("revenue")
    # expenses_sums = worksheet_sum("expenses")
    # profit_sum = [revenue_sums[i] - expenses_sums[i] for i in range(len(revenue_sums))]
    # profit_worksheet_data(profit_sum, "profit")
    # revenue_sums = worksheet_sum("revenue")
    # expenses_sums = worksheet_sum("expenses")
    # profit_worksheet_data(revenue_sums,'profit')
    # profit_worksheet_data(expenses_sums,'profit')


print(Back.BLACK + Fore.MAGENTA + '\033[1mWelcome to Farmer Market \
Automation!\033[0m\n')
print(Back.BLACK + Fore.MAGENTA + '\033[1mThe program will help you to \
deal with expenses and revenue data, and so, calculating the profit of your \
farmer market.\033[0m\n')
main()
