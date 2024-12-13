import json
import os

def write_message_to_file(message_info):
  print(f"DEBUG: Writing message to file: {message_info}")

  chat_id = message_info['chat_id']
  # Ensure the chats directory exists in the specified path
  chats_dir = os.path.join(os.getcwd(), 'reporter', 'chef', 'chats')
  os.makedirs(chats_dir, exist_ok=True)

  # Create the filename with user_id and current datetime
  filename = os.path.join(chats_dir, f"user_{chat_id}.txt")

  # Write the message information to the file
  with open(filename, 'w', encoding='utf-8') as file:
      file.write(json.dumps(message_info, indent=4))




def readchatfile(file_path):
    """
    Reads a message from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file.
        
    Returns:
        dict: Dictionary containing message information, or an error message.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File {file_path} contains invalid JSON.")
        return None

def appendturn(file_path, new_text):
  """
  Appends a message to the 'text' key in a JSON file.
  Args:
      file_path (str): Path to the JSON file.
      new_text (str): Text to append to the message.
  """
  try:
      # Read existing content from the file
      with open(file_path, 'r', encoding='utf-8') as file:
          message_info = json.load(file)

      # Append the new text to the existing message
      if 'text' in message_info:
          message_info['text'] += f"\n{new_text}"  # New message appended
      else:
          message_info['text'] = new_text

      # Write the updated content back to the file
      with open(file_path, 'w', encoding='utf-8') as file:
          json.dump(message_info, file, indent=4)

      print(f"Updated message appended to {file_path}.")

  except FileNotFoundError:
      print(f"Error: File not found at {file_path}.")
  except json.JSONDecodeError:
      print(f"Error: File {file_path} contains invalid JSON.")
  except IOError as e:
      print(f"Error writing to file {file_path}: {e}")

def write_message_to_file(file_path, message_info):
    """
    Writes a message to a JSON file.
    
    Args:
        file_path (str): Path to the JSON file.
        message_info (dict): Dictionary containing message information.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(message_info, file, indent=4)
        print(f"Message written to {file_path}.")
    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")

# Example usage (if running this script standalone)
if __name__ == "__main__":
    # Example file path and message info
    file_path = 'reporter/chef/chats/user_1275063227.txt'
    message_info = {
        "chat_id": 1275063227,
        "user_id": 1275063227,
        "username": "ferenstein",
        "first_name": "Greg",
        "message_id": 2486,
        "text": "yo"
    }

    # Write the message info to the file
    write_message_to_file(file_path, message_info)

    # Read the message info from the file
    read_result = read_message_from_file(file_path)
    if read_result:
        print("Message read from file:", read_result)