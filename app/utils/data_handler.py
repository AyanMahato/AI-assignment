import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

def handle_csv_upload(uploaded_file):
    df=pd.read_csv(uploaded_file)
    print("Column Headings:")
    for column in df.columns:
        print(column)
    return df

def connect_google_sheet(sheet_url):
    google_credentials = json.loads(os.getenv('GOOGLE_CREDENTIALS_JSON'))
    # Load credentials
    creds = Credentials.from_service_account_info(google_credentials, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    service = build('sheets', 'v4', credentials=credentials)
    sheet_id = sheet_url.split("/")[5]
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range="Sheet1").execute()
    data = result.get('values', [])
    df=pd.DataFrame(data[1:], columns=data[0])
    print("Column Headings:")
    for column in df.columns:
        print(column)
    return df

