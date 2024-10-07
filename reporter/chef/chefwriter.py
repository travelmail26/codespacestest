import json
import os

import requests
from perplexitychef import perplexitycall
from sheetscallchef import add_chatlog_entry, sheets_call

# Note for LLM agents: this is how the token secret is getting
openai_api_key = os.environ['OPENAI_API_KEY']

print("DEBUG: openai_api_key: ", openai_api_key)

sheets_call_data = sheets_call()

extended_context = f"Here is the extended context: \n{sheets_call_data}"

print(extended_context)


class AIHandler:

    def __init__(self, openai_key=None):
        self.openai_key = openai_key or openai_api_key
        self.messages = self.initialize_messages()

    def initialize_messages(self):
        content = (
            "You are a helpful assistant, especially around recipes and food. This is extended context: \n"
            f"{extended_context}\n"
            """Extended context is from an important key database of recipes.
            It will include recipes, equipment and, user preferences. 
            Prioritize first using this information in your response.
            Additionally, if you are asked to "browse" for an answer, 
            you will use a function tools call that uses another LLM agent to return information"""
        )
        return [{"role": "system", "content": content}]

    def openai_request(self):
        if not self.openai_key:
            return "OpenAI API key is missing."

        headers = {
            'Authorization': f'Bearer {self.openai_key}',
            'Content-Type': 'application/json'
        }

        tools = [{
            "type": "function",
            "function": {
                "name": "perplexitycall",
                "description":
                "Browse the internet for an answer to the user's query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user's query to search for"
                        }
                    },
                    "required": ["query"],
                    "additionalProperties": False
                },
                "strict": False
            }
        }]

        data = {
            'model': 'gpt-4o',
            'messages': self.messages,
            'temperature': 0.5,
            'max_tokens': 4096,
            'stream': False,
            'tools': tools
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

            # Check if the assistant wants to call a function (tool)
            if 'tool_calls' in assistant_message:
                tool_calls = assistant_message['tool_calls']
                for tool_call in tool_calls:
                    function_name = tool_call['function']['name']
                    function_args = json.loads(tool_call['function'].get(
                        'arguments', '{}'))
                    tool_call_id = tool_call['id']

                    if function_name == 'perplexitycall':
                        query = function_args.get('query')
                        if query:
                            print(
                                "Agent is searching the internet for an answer..."
                            )

                            # Prepare the conversation history for perplexitycall
                            structured_message = []

                            # Include user and assistant messages from the conversation
                            for msg in self.messages:
                                if msg['role'] in ['user', 'assistant']:
                                    if msg['content'] is None:
                                        msg['content'] = 'empty'
                                    structured_message.append(msg)

                            # No need to append the query again if it's already in self.messages
                            def filter_messages(messages):
                                filtered = []
                                for i, msg in enumerate(messages):
                                    if msg['role'] == 'assistant' and 'tool_calls' in msg:
                                        continue  # Skip this message
                                    if i > 0 and msg['role'] == filtered[-1][
                                            'role']:
                                        # Combine with previous message of same role
                                        filtered[-1][
                                            'content'] += "\n" + msg['content']
                                    else:
                                        filtered.append(msg)
                                return filtered

                            # Use this function before sending messages to Perplexity
                            perplexity_messages_filtered = filter_messages(
                                structured_message)
                            # Call Perplexity with the conversation history
                            response_content = perplexitycall(
                                perplexity_messages_filtered)

                            # Ensure response_content is a string
                            if isinstance(response_content, dict):
                                response_content = json.dumps(response_content)

                            # Properly format and send the function result back to the model
                            function_call_result_message = {
                                "role": "tool",
                                "content": response_content,
                                "tool_call_id": tool_call_id
                            }

                            # Add the assistant's message and function result to the conversation
                            self.messages.append(assistant_message)
                            print('DEBUG: assistant_message: ',
                                  assistant_message)
                            self.messages.append(function_call_result_message)
                            print('DEBUG: function_call_result_message: ',
                                  function_call_result_message)

                            # Prepare the payload for the second API call
                            completion_payload = {
                                "model": 'gpt-4o-mini',
                                "messages": self.messages
                            }

                            # Make the second API call
                            second_response = requests.post(
                                'https://api.openai.com/v1/chat/completions',
                                headers=headers,
                                json=completion_payload)
                            second_response.raise_for_status()

                            # Process the final response after the function call
                            second_response_json = second_response.json()
                            final_assistant_message = second_response_json[
                                'choices'][0]['message']

                            # Add the assistant's final response to the conversation
                            self.messages.append(final_assistant_message)

                            # Return the assistant's final response content
                            return final_assistant_message.get(
                                'content', 'No content in the response.')
                        else:
                            return "Error: No query provided for browsing."
                    else:
                        return f"Unknown function called: {function_name}"

            else:
                # If no function call, add the assistant's message to the conversation
                self.messages.append(assistant_message)
                return assistant_message.get('content',
                                             'No content in the response.')

        except requests.RequestException as e:
            return f"Error in OpenAI request: {str(e)}"

    def agentchat(self, prompt=None):
        print('DEBUG: agent chat triggered')

        # Add user input to messages
        self.messages.append({"role": "user", "content": prompt})

        # Get response from OpenAI
        response = self.openai_request()

        # Add AI response to messages
        #self.messages.append({"role": "assistant", "content": response})

        # Print AI response
        print("\nAI: ", response)
        try:
            add_chatlog_entry(response)
        except:
            print("Error adding chatlog entry")
        return response


handler = AIHandler()

# Example usage
if __name__ == "__main__":
    handler.agentchat("Can you find me a recipe for vegan brownies?")
