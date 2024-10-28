import json
import os

from openai import OpenAI

YOUR_API_KEY = openai_api_key = os.environ['PERPLEXITY_KEY']


def perplexitychat():
    print('**DEBUG: persplexitychat triggered**')

    user_input = ""

    while True:
        user_input = input("User: ")

        # Add user input to messages
        messages.append({"role": "user", "content": 'instructions just for the perplexity agent: when answering give a URL and name of author or commenter if getting an answer from the internet. Give a brief verbatim quote for each citation. User query follows:' + user_input})

        # Get response from OpenAI
        response = perplexitycall(messages)

        # Print AI response
        #print("\nAI: ", response)


def perplexitycall(messages):
    print('**DEBUG: perplexitycall triggered**')
    instruction = " instructions just for the perplexity agent: when answering give a URL and name of author or commenter if getting an answer from the internet. Give a brief verbatim quote for each citation. Don't forget to paste the full URL in the answer. User query follows:"

    # Append the instruction to the content of the last message
    messages[-1]['content'] = instruction + messages[-1]['content']

    

    try:
        client = OpenAI(api_key=YOUR_API_KEY,
                        base_url="https://api.perplexity.ai")
        #print('**DEBUG: messages sent perplexity api**', messages,
        #      '**DEBUG END**')
        #print('**DEBUG: type messages sent perplexity api**', type(messages))
        #print('**DEBUG: messages sent perplexity api**', messages)

        response = client.chat.completions.create(
            model="llama-3.1-sonar-large-128k-online", messages=messages)

        #print('**DEBUG: Response received from perplexity**' if response else '**DEBUG: No response received**')

        content = 'DEBUG: FROM PERPLEXITY: ' + str(
            response.choices[0].message.content)
        #print('**DEBUG: from perplexitycall content**', content)
        return content

    except Exception as e:
        print(f"**PERPLEXITY API ERROR**: {str(e)}")
        raise  # Re-raise the exception after printing the error message


if __name__ == "__main__":
    handler = perplexitychat()
