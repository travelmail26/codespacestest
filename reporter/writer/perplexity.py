import json
import os
from sheetscall import add_chatlog_entry

from openai import OpenAI

YOUR_API_KEY = openai_api_key = os.environ['PERPLEXITY_KEY']

try:
    with open('tools.txt', 'r') as file:
        tools = json.load(file)
except Exception:
    None

messages = [{
    "role":
    "system",
    "content":
    ("""You are an artificial intelligence assistant. Just say hi back to me."""
     ),
}]


def perplexitychat():
    print('**DEBUG: persplexitychat triggered**')

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
        response = perplexitycall(messages)

        # Add AI response to messages
        messages.append({"role": "assistant", "content": response})
        print('**DEBUG: message after response**', messages)

        # Print AI response
        print("\nAI: ", response)


def perplexitycall(messages):
    print('**DEBUG: perplexitycall triggered**')

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    print ('**DEBUG: messages sent perplexity api**', messages)

    # chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3.1-sonar-large-128k-online", messages=messages)

    add_chatlog_entry(str(response))
    # If no function call is needed, just print the model's response
    print('DEBUG RAW RESPONSE', response)

    print(response.choices[0].message.content)
    print(type(response))

    content = response.choices[0].message.content
    print(content)
    print(type(response))
    return content  # Return the content of the response


if __name__ == "__main__":
    handler = perplexitychat()
