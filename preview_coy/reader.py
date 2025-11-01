# reader.py
# Run with: python3 reader.py

import time
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- This is your existing project's code ---
# Make sure it's importable
# from your_project import generate_music_video
def generate_music_video(cv_text, photo_path):
    print("\n" + "="*40)
    print(f"🎬 TRIGGERING AI VIDEO GENERATOR 🎬")
    print(f"Photo: {photo_path}")
    print(f"Assembled CV:\n{cv_text}")
    print("="*40 + "\n")
    # ... your actual AI code goes here ...
# ---------------------------------------------


LOG_FILE_PATH = './cv_log.txt' # The log file from server.py

# A simple in-memory "database" to hold CV chunks
# Format: { "session_id": { index: "chunk", ... } }
cv_sessions = {}

# Regex to parse our log lines: [chunk].[index].[session_id].cv.my-hack.com.
# We use capturing groups () to extract the parts.
LOG_REGEX = re.compile(r"(\S+)\.(\d+)\.([a-f0-9\-]+)\.cv\.")

def process_log_line(line):
    """Parses a log line and stores the CV chunk."""
    try:
        # qname is the 2nd part of the log line
        qname = line.split(' ')[1] 
        match = LOG_REGEX.search(qname)
        
        if not match:
            return

        chunk, index, session_id = match.groups()
        index = int(index)

        if session_id not in cv_sessions:
            cv_sessions[session_id] = {}
        
        # Store the chunk
        cv_sessions[session_id][index] = chunk
        print(f"[Reader] Stored chunk {index} for session {session_id}: {chunk}")

        # Check if this is the "done" signal
        if chunk == 'HACK-END':
            print(f"[Reader] END signal detected for {session_id}!")
            assemble_and_run(session_id)

    except Exception as e:
        print(f"[Reader] Error parsing line: {e}")

def assemble_and_run(session_id):
    """Assembles the CV and triggers the video generator."""
    if session_id not in cv_sessions:
        return

    session_data = cv_sessions[session_id]
    
    # Sort the chunks by their index
    sorted_chunks = []
    # We sort up to the "HACK-END" packet
    for i in range(len(session_data) - 1): 
        sorted_chunks.append(session_data.get(i, ''))
    
    full_cv_text = " ".join(sorted_chunks)
    
    # --- TRIGGER YOUR AI ---
    # (You'll need to figure out how to get the photo path here)
    # For the demo, you can just hardcode it.
    photo_path = "demo_photo.jpg" 
    generate_music_video(full_cv_text, photo_path)
    
    # Clean up
    del cv_sessions[session_id]


class LogFileHandler(FileSystemEventHandler):
    """Watches for changes to the log file."""
    def __init__(self, file_path):
        self.file_path = file_path
        self.last_pos = 0
        # Process anything already in the log on startup
        self.process_existing()

    def process_existing(self):
        try:
            with open(self.file_path, 'r') as f:
                f.seek(0, 2) # Go to end of file
                self.last_pos = f.tell()
        except FileNotFoundError:
            pass # File might not exist yet

    def on_modified(self, event):
        if event.src_path == self.file_path:
            with open(self.file_path, 'r') as f:
                f.seek(self.last_pos) # Go to where we left off
                new_lines = f.readlines()
                self.last_pos = f.tell() # Update our position
                
                for line in new_lines:
                    if line.strip():
                        process_log_line(line.strip())

# --- Main script ---
print("[Reader] Starting log file watcher...")
event_handler = LogFileHandler(LOG_FILE_PATH)
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()