from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

# === EDIT THESE ===
SERVICE_ACCOUNT_FILE = "backend/hiresong-key.json"   # path to your JSON key
SHEET_ID = "1ZBwSfDbNE9DA5YQ2LVGovLdhtkYzEwwmGiaLvE9E5QA"  # from the Sheet URL

# Scopes: Sheets + Drive (Drive lets gspread open by key/url)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def main():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)

    # Open first worksheet (the bottom-left tab)
    ws = client.open_by_key(SHEET_ID).sheet1

    # Write something to A1
    value = f"HireSong smoke test @ {datetime.utcnow().isoformat(timespec='seconds')}Z"
    ws.update_acell("A1", value)   # gspread’s documented helper for a single cell

    print("✅ Wrote to A1:", value)

if __name__ == "__main__":
    main()
