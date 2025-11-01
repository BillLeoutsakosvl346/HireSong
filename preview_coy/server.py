# server.py
# MUST BE RUN WITH: sudo python3 server.py

import time
from dnslib import DNSLabel, QTYPE, RR, A, CNAME, TXT, DNSHeader, DNSRecord, DNSQuestion, RCODE
from dnslib.server import DNSServer, BaseResolver

LOG_FILE = 'cv_log.txt'
DOMAIN = 'my-hack.com' # Your domain

class CNHResolver(BaseResolver):
    """
    A custom resolver that logs all queries for our domain
    and replies with a dummy answer.
    """
    def resolve(self, request, handler):
        qname = request.get_q().get_qname()
        qname_str = str(qname)

        # Check if the query is for our special domain
        if qname_str.endswith(f'.cv.{DOMAIN}.'):
            # This is our CV data!
            print(f"[+] Received CV data: {qname_str}")
            
            # Log it to a file with a timestamp
            with open(LOG_FILE, 'a') as f:
                f.write(f"{int(time.time())} {qname_str}\n")
            
            # Send a dummy reply so the client doesn't hang
            # We'll just reply with 127.0.0.1
            reply = request.reply()
            reply.add_answer(RR(qname, QTYPE.A, rdata=A("127.0.0.1"), ttl=60))
            return reply

        # For any other query, just say we can't find it (NXDOMAIN)
        else:
            reply = request.reply()
            reply.header.rcode = RCODE.NXDOMAIN
            return reply

print(f"[*] Starting custom DNS server for *.{DOMAIN}...")
print(f"[*] Logging CV data to {LOG_FILE}")
print("[!] Make sure your domain's NS records point to this server's IP.")

# Start the server on port 53 (requires sudo)
server = DNSServer(CNHResolver(), port=53, address="0.0.0.0")
server.start()