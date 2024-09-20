import json
import os

import requests

# Fetching environment variables for API key
openai_api_key = os.environ['OPEN_API_KEY']

print("DEBUG: openai_api_key: ", openai_api_key)

with open('reporter/writer/tools.txt', 'r') as file:
    tools = json.loads(file.read())


class AIHandler:

    def __init__(self, openai_key=None):
        self.openai_key = openai_key or openai_api_key

    def openai_request(self, messages, function_call=None):
        print('openai request triggered')
        if not self.openai_key:
            return "OpenAI API key is missing."

        headers = {
            'Authorization': f'Bearer {self.openai_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'gpt-4-0613',
            'messages': messages,
            'temperature': 0.5,
            'max_tokens': 4096,
            'stream': True,
            'tools': tools
        }
        if function_call:
            data['function_call'] = function_call

        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                stream=True)
            response.raise_for_status()

            full_response = ""
            #for streaming responses
            for chunk in response.iter_lines():
                if chunk:
                    if chunk.startswith(b"data: "):
                        chunk_data = chunk[len(b"data: "):].decode('utf-8')
                        try:
                            json_data = json.loads(chunk_data)
                            if 'choices' in json_data and 'delta' in json_data[
                                    'choices'][0]:
                                delta = json_data['choices'][0]['delta']
                                if 'content' in delta:
                                    content = delta['content']
                                    print(content, end='', flush=True)
                                    full_response += content
                                elif 'function_call' in delta:
                                    return json_data['choices'][0]['message']
                        except json.JSONDecodeError:
                            pass
            return {"role": "assistant", "content": full_response}

        except requests.RequestException as e:
            return f"Error in OpenAI request: {str(e)}"

    def chat(self):
        messages = [{
            "role": "system",
            "content": "You are a helpful assistant."
        }]

        first_input = True
        user_input = ""

        while True:
            user_input = input("User: ")
            if first_input:
                user_input = user_input
                first_input = False

            # Add user input to messages
            messages.append({"role": "user", "content": user_input})

            # Get response from OpenAI
            response = self.openai_request(messages)

            # Add AI response to messages
            messages.append({"role": "assistant", "content": response})

            # Print AI response
            print("\nAI: ", response)


if __name__ == "__main__":
    handler = AIHandler()
    handler.chat()
