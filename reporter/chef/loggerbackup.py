import json
import os
from datetime import datetime
from pathlib import Path
from sheetscallchef import add_chatlog_entry

def get_current_time():
    return datetime.now().strftime('%H:%M:%S %d-%m-%Y')

class ConversationLogger:
    def __init__(self):
        self.backup_file = 'reporter/chef/conversation_backup.jsonl'
        self.ensure_backup_file()
        print('DEBUG: conversation logger initialized')

    def ensure_backup_file(self):
        if not os.path.exists(self.backup_file):
            Path(self.backup_file).touch()

    def log_conversation(self, messages, metadata=None):
        print('DEBUG: log conversation triggered')
        current_time = get_current_time()

        # Read existing entry if it exists
        if os.path.exists(self.backup_file) and os.path.getsize(self.backup_file) > 0:
            with open(self.backup_file, 'r') as f:
                try:
                    existing_entry = json.loads(f.readline())
                    existing_timestamp = datetime.strptime(existing_entry['timestamp'], '%H:%M:%S %d-%m-%Y').timestamp()
                    current_timestamp = datetime.strptime(current_time, '%H:%M:%S %d-%m-%Y').timestamp()
                    time_diff = current_timestamp - existing_timestamp
                    print(f"DEBUG: time_diff in seconds: {time_diff}")

                    # If enough time has passed, sync to sheets
                    if time_diff >= 300:
                        print('DEBUG: Time threshold met, syncing to sheets')
                        add_chatlog_entry(existing_entry['content'])
                except json.JSONDecodeError:
                    print("DEBUG: No valid existing entry found")

        # Write new entry
        new_entry = {
            'timestamp': current_time,
            'type': 'conversation',
            'content': messages,
            'metadata': metadata or {},
            'synced_to_sheets': False
        }

        with open(self.backup_file, 'w') as f:
            f.write(json.dumps(new_entry) + '\n')