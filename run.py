import pprint
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
GSPREAD_CLIENY = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENY.open('love_sandwiches')

sales = SHEET.worksheet('sales')

data = sales.get_all_values()
# print(data)

for row in data:
    pprint.pprint(row)

