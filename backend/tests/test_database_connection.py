"""
Quick test to verify Google Sheets connection.
Usage: python backend/tests/test_database_connection.py
"""

import sys
import os

# Point sys.path at backend/ (where 'api' lives)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

# Load .env BEFORE importing the service
from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

print("="*80)
print("GOOGLE SHEETS CONNECTION DIAGNOSTIC")
print("="*80)

# Test 1: Check if service account file exists
print("\n[1] Checking service account file...")
service_account_path = os.path.join(BACKEND_DIR, "hiresong-key.json")
if os.path.exists(service_account_path):
    print(f"✅ Found: {service_account_path}")
else:
    print(f"❌ NOT FOUND: {service_account_path}")
    print("\nPlease ensure the service account key file exists at:")
    print(f"  {service_account_path}")
    sys.exit(1)

# Test 2: Try to load credentials
print("\n[2] Testing credentials loading...")
try:
    from google.oauth2.service_account import Credentials
    
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    
    creds = Credentials.from_service_account_file(service_account_path, scopes=SCOPES)
    print("✅ Credentials loaded successfully")
    print(f"   Service account email: {creds.service_account_email}")
except Exception as e:
    print(f"❌ Failed to load credentials: {str(e)}")
    sys.exit(1)

# Test 3: Try to connect to Google Sheets
print("\n[3] Testing Google Sheets connection...")
try:
    import gspread
    
    client = gspread.authorize(creds)
    print("✅ Authorized with Google Sheets API")
except Exception as e:
    print(f"❌ Failed to authorize: {str(e)}")
    print("\nMake sure you have installed gspread:")
    print("  pip install gspread google-auth")
    sys.exit(1)

# Test 4: Try to open the specific sheet
print("\n[4] Testing access to your specific sheet...")
SHEET_ID = "1ZBwSfDbNE9DA5YQ2LVGovLdhtkYzEwwmGiaLvE9E5QA"
try:
    sheet = client.open_by_key(SHEET_ID).sheet1
    print(f"✅ Successfully opened sheet: {sheet.title}")
    print(f"   Spreadsheet: {client.open_by_key(SHEET_ID).title}")
    print(f"   Rows: {sheet.row_count}, Columns: {sheet.col_count}")
    
    # Test 5: Try to read first row
    print("\n[5] Testing read access...")
    try:
        first_row = sheet.row_values(1)
        if first_row:
            print(f"✅ Can read data. First row has {len(first_row)} columns")
            print(f"   First 3 columns: {first_row[:3]}")
        else:
            print("⚠️  Sheet is empty")
    except Exception as e:
        print(f"❌ Failed to read: {str(e)}")
    
    # Test 6: Try to write (append a test row)
    print("\n[6] Testing write access...")
    try:
        test_row = ["TEST", "connection_test", "Test URL", "Test", "Testing", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "Connection test"]
        sheet.append_row(test_row)
        print("✅ Successfully wrote test row")
        print("   Check your sheet - you should see a TEST row")
    except Exception as e:
        print(f"❌ Failed to write: {str(e)}")
        print("\nMake sure the service account has 'Editor' access to the sheet!")
        
except Exception as e:
    print(f"❌ Failed to open sheet: {str(e)}")
    print("\nPossible issues:")
    print("  1. The SHEET_ID might be wrong")
    print("  2. The service account doesn't have access to this sheet")
    print("\nTo fix:")
    print("  - Open the sheet in Google Sheets")
    print("  - Click 'Share' button")
    print("  - Add the service account email as an Editor:")
    print(f"    {creds.service_account_email}")
    sys.exit(1)

print("\n" + "="*80)
print("✅ ALL TESTS PASSED!")
print("="*80)
print("\nYour Google Sheets connection is working correctly.")
print("You can now run: python backend/tests/test_database.py")

