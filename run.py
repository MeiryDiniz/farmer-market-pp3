import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
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
        worksheet_data = SHEET.worksheet('revenue').row_values(1)
        if data.lower() not in [value.lower() for value in worksheet_data]:
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
        numeric_values = [float(value) if value !=
                          '' else 0 for value in column_data]
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


def calculate_profit(column2_index, column3_index, column4):
    """
    Function to have profit value calculated.
    """
    print(Fore.GREEN+'Calculating profit data...\n')
    column2_values = SHEET.worksheet('profit').col_values(column2_index)[1:]
    column3_values = SHEET.worksheet('profit').col_values(column3_index)[1:]
    column2_values = [float(value) if value !=
                      '' else 0 for value in column2_values]
    column3_values = [float(value) if value !=
                      '' else 0 for value in column3_values]

    profit_result = [column2 - column3 for column2,
                     column3 in zip(column2_values, column3_values)]
    sum_worksheet_data = SHEET.worksheet('profit')
    for i, result in enumerate(profit_result):
        sum_worksheet_data.update_cell(i + 2, column4, result)

    print(Fore.MAGENTA + 'Profit data has being calculated!\n')
    print(Fore.GREEN + 'Loading data to be printed......')


def sum_columns_profit(worksheet, column_range, total_cell):
    """
    Function to sum values of profit worksheet columns, 
    to show the total revenu, expenses and profit by month
    and year.
    """
    profit_worksheet = SHEET.worksheet(worksheet)
    values = profit_worksheet.get(column_range)
    total = sum([float(value[0]) for value in values])
    profit_worksheet.update(total_cell, total)


def print_profit_data():
    """
    Function to print the profit worksheet data using pandas.
    """
    print(Back.BLACK + '\033[1mYour Data is ready to be analysed.\033[0m\n')
    worksheet = SHEET.worksheet('profit')
    data = worksheet.get_all_values()    
    headers = data[0]
    table_data = data[1:]
    column_colors = [Fore.RESET, Fore.MAGENTA, Fore.GREEN, Fore.RED, Fore.BLUE]
    styled_headers = [f"{column_colors[i + 1]}{header}{Style.RESET_ALL}" for i, header in enumerate(headers)]
    styled_table_data = [[f"{column_colors[j + 1]}{cell}{Style.RESET_ALL}" for j, cell in enumerate(row)] for row in table_data]    
    table = [styled_headers] + styled_table_data   
    print(tabulate(table, headers='firstrow', tablefmt='grid'))   
    print(Back.BLACK + Fore.MAGENTA + '\033[1mThank you for using Farmer Market Automation!\033[0m')    


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

    revenue_worksheet = "revenue"
    revenue_sums = worksheet_sum(revenue_worksheet)
    append_worksheet_data("profit", revenue_sums, 2)
    expenses_worksheet = "expenses"
    expenses_sums = worksheet_sum(expenses_worksheet)
    append_worksheet_data("profit", expenses_sums, 3)
    calculate_profit(2, 3, 4)    
    sum_columns_profit('profit', 'B2:B13', 'B14') 
    sum_columns_profit('profit', 'C2:C13', 'C14')
    sum_columns_profit('profit', 'D2:D13', 'D14')
    print_profit_data()


print(Back.BLACK + Fore.MAGENTA + '\033[1mWelcome to Farmer Market \
Automation!\033[0m\n')
print(Back.BLACK + Fore.MAGENTA + '\033[1mThe program will help you to \
deal with expenses and revenue data, and so, calculating the profit of your \
farmer market.\033[0m\n')
main()
