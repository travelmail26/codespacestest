import requests
import os
import json

# Fetching environment variables for API key
openai_api_key = os.environ.get('OPENAI_API_KEY')

class AIHandler:
    def __init__(self, openai_key=None):
        self.openai_key = openai_key or openai_api_key

        # Placeholder for extended context with file handling
        self.extended_context = "Here is the extended context: "
        try:
            print("DEBUG: articletexttest.txt executed")
            with open('/workspaces/codespacestest/reporter/writer/lawtest.txt', 'r') as file:
                text_from_file = file.read()
                self.extended_context += "\n" + text_from_file
                print("DEBUG: Extended context: ", self.extended_context[:50])
        except FileNotFoundError:
            print("DEBUG: articletexttest.txt not found. Using default extended context.")
            self.extended_context = "Here is some default extended context."
        
    def openai_request(self, messages):
        if not self.openai_key:
            return "OpenAI API key is missing."

        headers = {
            'Authorization': f'Bearer {self.openai_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'gpt-4o-mini',
            'messages': messages,
            'temperature': 0.5,
            'max_tokens': 4096,
            'stream': True
        }

        try:
            # Send the request to OpenAI and stream the response
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data, stream=True)
            response.raise_for_status()

            # Process the streamed response in chunks
            full_response = ""
            for chunk in response.iter_lines():
                if chunk:
                    # The chunk is a string of JSON data prefixed with "data: ", so strip that and parse it
                    if chunk.startswith(b"data: "):
                        chunk_data = chunk[len(b"data: "):].decode('utf-8')
                        try:
                            # Parse the chunk data as JSON
                            json_data = json.loads(chunk_data)

                            # Extract and print the content from the delta if it exists
                            if 'choices' in json_data and 'delta' in json_data['choices'][0]:
                                content = json_data['choices'][0]['delta'].get('content', '')
                                if content:
                                    print(content, end='', flush=True)  # Print content without newlines
                                    full_response += content
                        except json.JSONDecodeError:
                            pass  # Skip any malformed JSON
            return full_response

        except requests.RequestException as e:
            return f"Error in OpenAI request: {str(e)}"
    
    def chat(self):
        # Initialize conversation history
        messages = [
            {"role": "system", "content": """ You are are designed to create vector representations of text data. The data will by referred to as extended context
             and will come in the form of a legislative bill. Your answers should be in the form of a vector representation of the data. The key value
             pairs should include information from the instructions given to you by the user """},
            {"role": "system", "content": "This is the extended context: " + self.extended_context}
        ]

        first_input = True

        while True:
            # Get user input
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting chat.")
                break

            # Prepend extended context to the first user input
            if first_input:
                user_input = self.extended_context + "\n" + user_input
                first_input = False

            # Add user input to messages
            messages.append({"role": "user", "content": user_input})

            # Get response from OpenAI
            response = self.openai_request(messages)

            # Add AI response to messages
            messages.append({"role": "assistant", "content": response})

            # Print AI response
            print("\nAI: ", response)

# Example usage
if __name__ == "__main__":
    handler = AIHandler()
    handler.chat()
