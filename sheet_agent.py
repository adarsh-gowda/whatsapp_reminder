# sheet_agent.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_subscribers():
    """
    Connects to the Google Sheet and loads subscriber data.
    Assumes sheet headers like: name, phone_number, subscription_end, etc.
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
    client = gspread.authorize(creds)

    # Open the sheet using its ID
    sheet = client.open_by_key("1M3OrTyDeR1wQ66JKyBAKBugpz-q6-8M201n-Ly3JYNY").sheet1
    raw_data = sheet.get_all_records()

    # Optional: Normalize column names for consistency
    normalized_data = []
    for row in raw_data:
        normalized_data.append({
            "name": row.get("user name"),
            "phone_number": row.get("whatsapp number"),
            "subscription_end": row.get("Expiry Date"),
            "subscription_start": row.get("Subscription Start Date"),
            "subscription_pending": row.get("subscription pending"),
        })

    return normalized_data
