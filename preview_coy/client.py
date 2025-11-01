# client.py
# Run with: python3 client.py

import dns.resolver
import uuid
import time
import re
from PyPDF2 import PdfReader

# --- CONFIGURE THIS ---
CV_PDF= 'test_files/CoyKZhu_CV.pdf'
reader = PdfReader("test_files/CoyKZhu_CV.pdf")
number_of_pages = len(reader.pages)
textarr = []

for i in range(number_of_pages):
    page = reader.pages[0]
    pgtext = page.extract_text()
    textarr.append(pgtext)
    textarr.append("\n")

text = "".join(textarr)

DOMAIN = 'my-hack.com' # Your domain
YOUR_SERVER_IP = '127.0.0.1' # Your server's public IP
# ----------------------

# Set up the resolver to *only* ask our custom server
# This bypasses local caching and normal DNS, making it faster
resolver = dns.resolver.Resolver()
resolver.nameservers = [YOUR_SERVER_IP]

def send_cv_chunk(session_id, chunk_index, chunk):
    """
    Encodes and sends a single chunk of data as a DNS query.
    """
    # Sanitize the chunk to be DNS-safe (alphanumeric and hyphens)
    safe_chunk = re.sub(r'[^a-zA-Z0-9]', '-', chunk)
    
    # DNS labels are max 63 chars. We'll be safe at 50.
    if len(safe_chunk) > 50:
        safe_chunk = safe_chunk[:50]
        
    if not safe_chunk:
        return # Don't send empty chunks

    # Format: [chunk].[index].[session_id].cv.[your_domain].
    # Example: Python.1.abc12345.cv.my-hack.com
    query = f"{safe_chunk}.{chunk_index}.{session_id}.cv.{DOMAIN}."
    
    print(f"[*] Sending: {query}")
    try:
        # We send the query. We don't care about the answer.
        # The 'except' is expected because our server sends a dummy reply.
        resolver.query(query, 'A')
    except Exception as e:
        pass # Expected

# --- Main script ---
session_id = str(uuid.uuid4())[:8] # A unique ID for this CV

print(f"[*] Starting CV upload with session ID: {session_id}")

# Split the CV into simple words
words = text.split()

for i, word in enumerate(words):
    send_cv_chunk(session_id, i, word)
    time.sleep(0.1) # A small delay to be nice to the network

# Send a "done" signal
send_cv_chunk(session_id, len(words), 'HACK-END')

print(f"[+] CV upload finished for session ID: {session_id}")