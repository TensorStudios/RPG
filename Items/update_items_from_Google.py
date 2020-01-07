# Note: this is pretty much a copy and paste from google's instructions. It may be out of date


import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1g3umkK_gBPgHe1Yav-3LCsi19i7Bfc22gxfkA5x0j48'
RANGE_NAME_ARMOR = 'Armor!A1:J'
RANGE_NAME_HATS = 'Hats!A1:J'
RANGE_NAME_WEAPONS = 'Weapons!A1:J'


creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('Items/api_credentials/token.pickle'):
    with open('Items/api_credentials/token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'Items/api_credentials/credentials.json', SCOPES)
        creds = flow.run_local_server()
    # Save the credentials for the next run
    with open('Items/api_credentials/token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range=RANGE_NAME_ARMOR).execute()
Armor = result.get('values', [])
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range=RANGE_NAME_HATS).execute()
Hats = result.get('values', [])
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range=RANGE_NAME_WEAPONS).execute()
Weapons = result.get('values', [])

with open("Items/Armor.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerows(Armor)
with open("Items/Hats.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerows(Hats)
with open("Items/Weapons.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerows(Weapons)
