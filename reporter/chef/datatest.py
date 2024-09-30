import json
import os

import requests

# Fetching environment variables for API key
openai_api_key = os.environ['OPENAI_API_KEY']

print("DEBUG: openai_api_key: ", openai_api_key)

# Example JSON dictionary
# user_data = {
#     "username":
#     "Greg",
#     "food_preferences":
#     "meat, dairy",
#     "sweetener_preference":
#     "raw honey only if sugar is needed. the recipe cannot cook the honey but can add after cooking or if cooking is belwo 100 degrees"
# }

user_data = """NA"""

# Convert the dictionary to a string
# user_data_string = json.dumps(user_data)

user_data_string = user_data


def generate_response(prompt):
    try:
        headers = {
            'Authorization': f'Bearer {openai_api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model':
            'gpt-4o-mini',
            'messages': [{
                "role":
                "system",
                "content":
                "You are a helpful assistant that provides information based on user preferences."
            }, {
                "role": "user",
                "content": prompt
            }],
            'temperature':
            0.5,
            'max_tokens':
            4096,
            'stream':
            True
        }

        print("DEBUG: Payload sent to OpenAI:", json.dumps(data, indent=2))

        response = requests.post('https://api.openai.com/v1/chat/completions',
                                 headers=headers,
                                 json=data,
                                 stream=True)
        response.raise_for_status()

        full_response = ""
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
                    except json.JSONDecodeError:
                        pass
        return full_response

    except requests.RequestException as e:
        return f"An error occurred: {str(e)}"


# Main script


def main(prompt):
    print("User Data:", user_data_string)

    prompt = prompt
    

    print("\nAI Response:")
    response = generate_response(prompt)
    print("\nFull Response:", response)
    return response


if __name__ == "__main__":
    main()
