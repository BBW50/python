import gspread
from google.oauth2.service_account import Credentials

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'your-json-file-name.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)

SP_SHEET_KEY = 'your-google-key'
SP_SHEET = 'your-sheet-name'

sh = gc.open_by_key(SP_SHEET_KEY)