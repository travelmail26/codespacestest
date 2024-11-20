import os
import json
import time
import importlib
from datetime import datetime, timedelta
import pytz
from pathlib import Path
import uuid

def create_alarm_dict(seconds, message):
    """
    Creates a dictionary representing an alarm with unique ID
    Args:
        seconds (int): Seconds from now when alarm should trigger
        message (str): Message associated with the alarm
    Returns:
        dict: Alarm dictionary with ID, time, message, and triggered status
    """
    
    current_time = datetime.now(pytz.timezone('America/New_York'))
    trigger_time = current_time + timedelta(seconds=int(seconds))  # Use the passed in seconds parameter

    
    
    return {
        'id': str(uuid.uuid4()),
        'time': trigger_time.isoformat(),
        'message': message,
        'triggered': False
    }

def append_alarm(trigger_time, message):
    print (f"DEBUG: append alarm triggered")
    """
    Appends a new alarm to active_alarms.json
    Args:
        trigger_time (str): When alarm should trigger (ISO format)
        message (str): Message for the alarm
    Returns:
        bool: True if successful, False if failed
    """
    try:
        # Create new alarm dictionary
        
        alarm_dict = create_alarm_dict(trigger_time, message)
        print (f"DEBUG: alarm dict: {alarm_dict}")

        # Create/load alarms file
        if not os.path.exists('active_alarms.json'):
            current_alarms = []
        else:
            with open('active_alarms.json', 'r') as f:
                current_alarms = json.load(f)

        # Append new alarm
        current_alarms.append(alarm_dict)

        # Write back to file
        with open('active_alarms.json', 'w') as f:
            json.dump(current_alarms, f)

        return True

    except Exception as e:
        print(f"Error appending alarm: {str(e)}")
        return False

def remove_triggered_alarm(alarm_id):
    """
    Removes a specific alarm from the active_alarms.json file
    Args:
        alarm_id (str): Unique ID of alarm to remove
    Returns:
        bool: True if successful, False if failed
    """
    try:
        if os.path.exists('active_alarms.json'):
            # Read existing alarms
            with open('active_alarms.json', 'r') as f:
                alarms = json.load(f)

            # Filter out the triggered alarm
            updated_alarms = [alarm for alarm in alarms if alarm['id'] != alarm_id]

            # Write back to file
            with open('active_alarms.json', 'w') as f:
                json.dump(updated_alarms, f)

            return True
        return False

    except Exception as e:
        print(f"Error removing alarm: {str(e)}")
        return False

def send_alarm_message(alarm_dict):
    """
    Sends alarm message directly to Telegram and removes sent alarm
    Args:
        alarm_dict (dict): Dictionary containing alarm id and message
    """
    try:
        from telegram_bot import send_telegram_message
        print(f"DEBUG: sending alarm {alarm_dict['id']}")
        message = f"🔔 TIMER ALERT: {alarm_dict['message']}"

        send_telegram_message(message)
        # Remove the triggered alarm
        remove_triggered_alarm(alarm_dict['id'])
        return True
    except Exception as e:
        print(f"Error sending alarm message: {str(e)}")
        return False

def check_alarms():
    while True:
        try:
            with open('active_alarms.json', 'r') as f:
                current_alarms = json.load(f)

            # Use timezone-aware current time
            timezone = pytz.timezone('America/New_York')
            current_time = datetime.now(timezone)

            # Check each alarm
            for alarm in current_alarms:
                if not alarm['triggered']:
                    # Convert alarm time string to timezone-aware datetime
                    alarm_time = datetime.fromisoformat(alarm['time'])
                    if alarm_time.tzinfo is None:
                        # If alarm time has no timezone, make it timezone-aware
                        alarm_time = timezone.localize(alarm_time)

                    if current_time >= alarm_time:
                        # Trigger alarm
                        print(f"ALARM: {alarm['message']}")
                        send_alarm_message(alarm)
                        alarm['triggered'] = True

            # Save updated alarm states
            with open('active_alarms.json', 'w') as f:
                json.dump(current_alarms, f)

        except Exception as e:
            print(f"Error checking alarms: {e}")

        # Wait before next check
        time.sleep(2)  # Check every 10 seconds


if __name__ == "__main__":
    check_alarms()  # Start checking for alarms when script is run directly