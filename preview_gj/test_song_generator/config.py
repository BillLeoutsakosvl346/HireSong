import os
from dotenv import load_dotenv

# Debug: Show where we're looking for .env
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
print(f"🔍 Looking for .env at: {os.path.abspath(env_path)}")
print(f"📂 .env exists: {os.path.exists(env_path)}")

# Read file content directly to debug
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        content = f.read()
        print(f"📄 .env content: {repr(content)}")

# Load with debug
load_dotenv(env_path, verbose=True)

# Check all environment variables
print(f"\n🔍 All environment variables with 'ELEVEN':")
for key, value in os.environ.items():
    if 'ELEVEN' in key.upper():
        print(f"   {key}={value[:20]}...")

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
print(f"\n🔑 ELEVENLABS_API_KEY: {ELEVENLABS_API_KEY}")
print(f"🔑 API Key found: {bool(ELEVENLABS_API_KEY)}")
if ELEVENLABS_API_KEY:
    print(f"   Key starts with: {ELEVENLABS_API_KEY[:10]}...")
    print(f"   Key length: {len(ELEVENLABS_API_KEY)}")

if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY not found in .env file")

print("✅ Configuration loaded successfully!\n")
