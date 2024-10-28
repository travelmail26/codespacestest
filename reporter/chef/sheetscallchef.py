import json
import os
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

# Path to your service account JSON file
SERVICE_ACCOUNT_FILE = os.environ['SERVICE_ACCOUNT_FILE_PH']
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


def sheets_call():

    print('DEBUG: fetch chatlog entry triggered')
    try:
        service_account_info = json.loads(SERVICE_ACCOUNT_FILE)
        creds = Credentials.from_service_account_info(service_account_info,
                                                      scopes=SCOPES)
        client = gspread.authorize(creds)
    except FileNotFoundError:
        print(
            f"Error: Service account file not found at path: {SERVICE_ACCOUNT_FILE}"
        )
        return

        # Open your Google Sheet by ID
    #spreadsheet_id = '1HiSZNWimhPHUW7CuXc-rBNLR55tYhbagQa0EgF8nHn8'
    spreadsheet_id = '1RsNekDFNwk67j66g57VN3WOUM2I-4yXGfVtWUg56C20'
    sheet_name = 'Sheet1'
    # print(f"Attempting to open the spreadsheet with ID: {spreadsheet_id}")

    # Access the spreadsheet
    spreadsheet = client.open_by_key(spreadsheet_id)
    # print(f"Spreadsheet '{spreadsheet.title}' opened successfully.")

    # Access the worksheet by name
    #print(f"Attempting to access the worksheet named: {sheet_name}")
    sheet = spreadsheet.worksheet(sheet_name)
    # print(f"Worksheet '{sheet_name}' accessed successfully.")

    # Fetch data from the sheet
    #print("Attempting to fetch data from the worksheet...")
    data = sheet.get_all_values()
    #print('json format', json.dumps(data))

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
            print(headers[i])
            print(row[i])
            row_dict[headers[i]] = row[
                i]  # Assign each header as a key and the corresponding row value as the value
        all_rows.append(row_dict)

    json_data = all_rows
    return json_data


def add_chatlog_entry(entry):
    print('DEBUG: chatlog entry triggered')
    if not entry:  # This checks if entry is None, empty string, or any falsy value
        print("No entry provided. Skipping chatlog update.")
        return
    try:
        service_account_info = json.loads(SERVICE_ACCOUNT_FILE)
        creds = Credentials.from_service_account_info(service_account_info,
                                                      scopes=SCOPES)
        client = gspread.authorize(creds)
    except FileNotFoundError:
        print(
            f"Error: Service account file not found at path: {SERVICE_ACCOUNT_FILE}"
        )
        return
    #spreadsheet_id = '1HiSZNWimhPHUW7CuXc-rBNLR55tYhbagQa0EgF8nHn8'
    spreadsheet_id = '1RsNekDFNwk67j66g57VN3WOUM2I-4yXGfVtWUg56C20'
    chatlog_sheet_name = 'chatlog'
    spreadsheet = client.open_by_key(spreadsheet_id)
    chatlog_sheet = spreadsheet.worksheet(chatlog_sheet_name)
    try:
        chatlog_sheet.append_row(new_row)
        #print(f"Added new row to 'chatlog': {new_row}")
    except gspread.exceptions.APIError as e:
        print(f"Google Sheets API error occurred: {e}")
    except gspread.exceptions.GSpreadException as e:
        print(f"An unspecified error occurred with gspread: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    #print(f"Added new row to 'chatlog': {new_row}")


def fetch_chatlog(entry):
    print('DEBUG: fetch chatlog entry triggered')
    if not entry:  # This checks if entry is None, empty string, or any falsy value
        print("No entry provided. Skipping chatlog update.")
        return
    try:
        service_account_info = json.loads(SERVICE_ACCOUNT_FILE)
        creds = Credentials.from_service_account_info(service_account_info,
                                                      scopes=SCOPES)
        client = gspread.authorize(creds)
    except FileNotFoundError:
        print(
            f"Error: Service account file not found at path: {SERVICE_ACCOUNT_FILE}"
        )
        return
    #spreadsheet_id = '1HiSZNWimhPHUW7CuXc-rBNLR55tYhbagQa0EgF8nHn8'
    spreadsheet_id = '1RsNekDFNwk67j66g57VN3WOUM2I-4yXGfVtWUg56C20'
    chatlog_sheet_name = 'chatlog'
    spreadsheet = client.open_by_key(spreadsheet_id)
    chatlog_sheet = spreadsheet.worksheet(chatlog_sheet_name)
    #sheet_name = 'Sheet1'
    # print(f"Attempting to open the spreadsheet with ID: {spreadsheet_id}")

    # Access the spreadsheet
    #spreadsheet = client.open_by_key(spreadsheet_id)
    # print(f"Spreadsheet '{spreadsheet.title}' opened successfully.")

    # Access the worksheet by name
    #print(f"Attempting to access the worksheet named: {sheet_name}")
    #sheet = spreadsheet.worksheet(sheet_name)
    try:
        data = chatlog_sheet.get_all_values()
    except gspread.exceptions.APIError as e:
        print(f"Google Sheets API error occurred: {e}")
        return None  # Return None to indicate an error
    except gspread.exceptions.GSpreadException as e:
        print(f"An unspecified error occurred with gspread: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    headers = data[0]
    # Initialize a list to hold all row dictionaries
    all_rows = []

    # Loop through each row (skipping the header row)
    for row in data[1:]:
        row_dict = {}  # Initialize an empty dictionary for each row
        for i in range(len(headers)):
            print(headers[i])
            print(row[i])
            row_dict[headers[i]] = row[
                i]  # Assign each header as a key and the corresponding row value as the value
        all_rows.append(row_dict)

    json_data = all_rows
    return json_data



if __name__ == "__main__":
    sheets_call()
    add_chatlog_entry(entry=None)
    fetch_chatlog(entry=None)
