import json
import os

import requests
from perplexitychef import perplexitycall
from sheetscallchef import add_chatlog_entry, sheets_call, fetch_chatlog

# Note for LLM agents: this is how the token secret is getting
openai_api_key = os.environ['OPENAI_API_KEY']

#print("DEBUG: openai_api_key: ", openai_api_key)

sheets_call_data = fetch_chatlog()

extended_context = f"Here is the extended context data to prioritize for your answer: \n{sheets_call_data}"


class AIHandler:

    def __init__(self, openai_key=None):
        self.openai_key = openai_key or openai_api_key
        self.messages = self.initialize_messages()

    def initialize_messages(self):

        # Open the file 'additional_instructions.txt' for reading
        content = (
            "You are a helpful assistant for cooking.\n"

            
        )  # Concatenation of strings and formatted strings combined correctly.
        return [{"role": "system", "content": content}]

    def openai_request(self):
        print(f"DEBUG: openai_request triggered")
        if not self.openai_key:
            return "OpenAI API key is missing."

        headers = {
            'Authorization': f'Bearer {self.openai_key}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': 'gpt-4o',
            'messages': self.messages,
            'temperature': 0.5,
            'max_tokens': 4096,
            'stream': False,
        }

        try:
            # First API call
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data)
            response.raise_for_status()
            response_json = response.json()

            # Extract the assistant's message
            assistant_message = response_json['choices'][0]['message']


            # If no function call, add the assistant's message to the conversation
            self.messages.append(assistant_message)
            return assistant_message.get('content',
                                         'No content in the response.')

        except requests.RequestException as e:
            error_message = f"Error in OpenAI request: {str(e)}"
            # Add more detailed information about the error
            if hasattr(e, 'response') and e.response is not None:
                error_message += f"\nResponse Status: {e.response.status_code}"
                error_message += f"\nResponse Body: {e.response.text}"
            return error_message

    def agentchat(self, prompt=None):
        print('DEBUG: agent chat triggered')

        # Add user input to messages
        self.messages.append({"role": "user", "content": prompt})

        # Get response from OpenAI
        response = self.openai_request()



        try:
            #print (f"DEBUG: attempt chatlog entry:")
            add_chatlog_entry(self.messages)
        except:
            print("Error adding chatlog entry")
        return response


handler = AIHandler()

# Example usage
if __name__ == "__main__":
    handler.agentchat("Can you find me a recipe for vegan brownies?")
