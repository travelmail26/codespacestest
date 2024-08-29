import requests
import os

# Your OpenAI API key
API_KEY = os.environ['OPENAI_API_KEY']

print (os.environ['OPENAI_API_KEY'])

# Placeholder for extended text, like reports and articles
extended_context = """
Here are a few articles written about the current state of 
psychedelics policy in the United States. Draw from each one when writing your own article from the prompt
"""

def openAI(prompt):
    # Compose the input for the API
    messages = [
        {"role": "user", "content": prompt}
    ]

    # Make the API call
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={'model': 'gpt-4', 'messages': messages, 'temperature': 0.7, 'max_tokens': 256},
        timeout=30
    )

    print ('DEBUG: response code', response.status_code)

    # Extract the assistant's message from the API response
    response_data = response.json()
    message_content = response_data.get('choices', [{}])[0].get('message', {}).get('content', "Sorry, I couldn't process your request.")
    return message_content

# Example usage
user_input = "Write a 200-word news article about the state of congressional policy for psychedelics, including background on current state policies."

response = openAI(user_input)
print(response)