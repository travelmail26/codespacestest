import gspread
from google.oauth2.service_account import Credentials
import json
import os

# Path to your service account JSON file
SERVICE_ACCOUNT_FILE = os.environ.get('GOOGLE_API')

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']


def sheets_call():

    try:
        service_account_info = json.loads(SERVICE_ACCOUNT_FILE)
        # Create a credentials object from the service account file
        creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
        #print ('DEBUG CREDS', creds)
        print("Credentials loaded successfully.")

        # Authorize and create a client to interact with Google Sheets
        client = gspread.authorize(creds)
        print("Authorized Google Sheets client successfully.")
    except FileNotFoundError:
        print(f"Error: Service account file not found at path: {SERVICE_ACCOUNT_FILE}")
        
        # Open your Google Sheet by ID
    spreadsheet_id = '1-SVTJh9jsMrlnhg7jVDOA7-CRX9Qe6i92c3nv1NTWTc'
    sheet_name = 'Sheet1'
    # print(f"Attempting to open the spreadsheet with ID: {spreadsheet_id}")

    # Access the spreadsheet
    spreadsheet = client.open_by_key(spreadsheet_id)
    # print(f"Spreadsheet '{spreadsheet.title}' opened successfully.")

    # Access the worksheet by name
    print(f"Attempting to access the worksheet named: {sheet_name}")
    sheet = spreadsheet.worksheet(sheet_name)
    # print(f"Worksheet '{sheet_name}' accessed successfully.")

    # Fetch data from the sheet
    #print("Attempting to fetch data from the worksheet...")
    data = sheet.get_all_values()
    #print ('json format', json.dumps(data))

    # print ('get all values', sheet.get_all_values())
    # print ('get A value', sheet.acell('A1').value)

    ## turn data into json format
    headers = data[0]
    # Initialize a list to hold all row dictionaries
    all_rows = []

    # Loop through each row (skipping the header row)
    for row in data[1:]:
        row_dict = {}  # Initialize an empty dictionary for each row
        for i in range(len(headers)):
            print (headers[i])
            print (row[i])
            row_dict[headers[i]] = row[i]  # Assign each header as a key and the corresponding row value as the value
        all_rows.append(row_dict) 

    json_data = all_rows 
    print (json_data)
    return json_data


sheets_call()

# except gspread.exceptions.SpreadsheetNotFound:
#     print(f"Error: Spreadsheet with ID {spreadsheet_id} not found.")
# except gspread.exceptions.WorksheetNotFound:
#     print(f"Error: Worksheet named '{sheet_name}' not found in the spreadsheet.")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")
