import gspread
from google.oauth2.service_account import Credentials

# Define the scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Define the credentials
CREDENTIALS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDENTIALS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')
# sales = SHEET.worksheet('sales')

def get_sales_data():
    """
    Get sales figures input from the user
    """
    
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")
        data = validate_data(sales_data)
        if data:
            print("Data is valid!")
            break

    return data
          
            
def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    
    try:
        result = [int(value) for value in values]
        if len(result) != 6:
              raise ValueError(
               print(f"Exactly 6 values required, you provided {len(result)}") 
              )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return result
       
   

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def calculate_surplus_data(stock_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock_row = SHEET.worksheet('stock').get_all_values()
    stock = stock_row[-1]
    sales_row = SHEET.worksheet('sales').get_all_values()
    sales = sales_row[-1]
    surplus_data = []
    for stock, sales in zip(stock, sales):
        surplus = int(stock) - int(sales)
        surplus_data.append(surplus)
    print(f"Surplus data calculated successfully: {surplus_data}\n")
    return surplus_data

def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list data provided
    """
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfully.\n")
  

def main():
    """
    Run all program functions
    """
    print("Welcome to Love Sandwiches Data Automation \n")
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(surplus_data)

main()


