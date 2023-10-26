# Farmer Market

I live in a town where there are some farmer markets. Thinking of something to automate the way they control and check their business revenue, expenses and profits, I created **Farmer Market**.

**Farmer Market** is an automation program that you can enter the revenue and expenses of your business, and the program will calculate the profit. 
Although it was created to be a farmer market automation, this program can be used by other types of businesses, or even to control our finances.   

![Farmer Market Automation]()

Visit the live version of the program automation: [Farmer Market Automation]()

- - -

## CONTENTS
  
* [AUTOMATED TESTING](#automated-testing)
  * [PEP8 Python Validator](#pep8-python-validator)  
* [MANUAL TESTING](#manual-testing)
   * [Test done by Developer](#test-done-by-developer)
* [BUGS](#bugs)
   * [Fixed bugs](#fixed-bugs)   
   * [Unfixed bugs](#unfixed-bugs)
* [DEPLOYMENT](#deployment) 
* [RESOURCE](#resource)
* [IMPROVEMENT](#improvement)  
* [CONTENT](#content)
* [CREDITS](#credits)  
* [MEDIA]

- - -

## AUTOMATED TESTING

###  PEP8 Python Validator

 * [PEP8 Python Validator](https://pep8ci.herokuapp.com/) was used to validate the code, and any error was returned.

- - -

## MANUAL TESTING

### Test done by developer

`Data Inputted`

| Feature | Expected Outcome | Testing Performed | Result | Passed/Failed | Image
| --- | --- | --- | --- | --- | --- |
| ``while loop`` in ``get_worksheet_data()`` function | Keep the code running until all required data is inputted correctly. | Data was inputted to have the function feature tested. | The code in the function ran until the required data was inputted correctly. | Passed | () |
| ``try`` and ``except`` block in ``validate_month_input(data)`` and ``validate_value_input(data)`` function | Have the data inputted by the user validated and keep the program running even if ivalid data is inputted. | Invalid and valid data were inputted to check if the code was working as expected.| When an invalid data was inputted the code returned a message to the user informing what happend and what should bedone. The code kept running normally. | Passed | () |

`Worksheet data, sum, and data updated on worksheets`

| Feature | Expected Outcome | Testing Performed | Result | Passed/Failed | Image
| --- | --- | --- | --- | --- | --- |
| ``add_worksheet_data(data, worksheet)`` | Function to have the data inputted by the user entered to the correctly worksheet after it is validated. | The worksheet was checked after the code finished running to check if values were entered correctly. | Data was entered to the correctly workshhet. | Passed | () |
|``worksheet_sum(worksheet)`` and ``sum_columns_profit(worksheet, column_range, total_cell)`` | Function to have data inputted summed. | Data was inputted to have values summed and printed on the console to have the function feature tested. | The values printed were correctly. | Passed | () |
| ``append_worksheet_data(worksheet, values, column)`` | Function to have data entered to the correctly worksheet after it is summed. | Data was inputted and the worksheet was checked after the code finished running. | Data was entered to the correctly worksheet. | Passed | () |

`Profit Worksheet updated and printed`

| Feature | Expected Outcome | Testing Performed | Result | Passed/Failed | Image
| --- | --- | --- | --- | --- | --- |
| ``calculate_profit(column2_index, column3_index, column4)`` | Function to have profit calculated after data is entered to the profit worksheet and each time it is updated. | Data was inputted and profit worksheet was checked after the code finished running. | Data was calculated correctly. | Passed | () |
|``sum_columns_profit(worksheet, column_range, total_cell)`` | Function to have anual data calculated. | Data was inputted to have values entered to the worksheets and have the function feature tested. | The values calculated were correctly. | Passed | () |
| ``print_profit_data()`` | Function to have data printed to the console after data inputted is calculated. | Data was inputted and values in worksheet were checked to be sure they match to the values printed. | Data printed matched correctly to the data in worksheet. | Passed | () |

- - -

## BUGS

### Fixed bugs

| Bug | Reason | Action |
| --- | --- | --- |
| The ``validate_month_input(data)`` function was not returning an error when some numbers were inputted instead of a month. | It was happening because I did not specify in the function that I would like the inputted data to be compared just with the data in the first row of the worksheet.  | I specified in the function which row of the worksheet I would like to be compared with the inputted data. (``row_values(1)``) |
| I had a considerable number of problems with the result of functions in my code and also, how them were running. | It happened because I was not using the correct indentation and sequence to write the functions. | I revised the course content, did research on google and kept trying until I got the result that I needed. |

### Unfixed bugs
I have tested the program and did not find any other bug.

- - -

## DEPLOYMENT 

The **Farmer Market** program automation was deployed on Heroku using Code Institute's mock terminal.

- - -

## RESOURCE

In addition to the course content I used [Stack Overflow](http://stackoverflow.com) to do research to develop my program. 

- - - 

## IMPROVEMENT 

At the moment the program can just be used to input revenue and expenses data, and have the profit calculated. I think it is really basic and would like to continue improving this program as I improve my skills. My goal is develop a complete program automation.

- - - 

## MEDIA

- The pictures used on ``README.md`` were converted to _webp_ using [Pixelied](https://pixelied.com/).
- The program's image was displayed using [Am I Responsive](https://ui.dev/amiresponsive)
- [Tabulate](https://pypi.org/project/tabulate/) and [Colorama](https://pypi.org/project/colorama/) libraries were used in the program.


- - - 

## CONTENT

The content and code of the program were wrote by the developer.

- - - 

## CREDITS

I used the Code Intitute's **Love Sandwiches** milestone project as a base to develop my proram and understand better how to use ``Python`` on its development.
