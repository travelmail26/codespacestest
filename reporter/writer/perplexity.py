from openai import OpenAI
import json

YOUR_API_KEY = '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'


#tools object is in a separate file
with open('tools.txt', 'r') as file:
    tools = json.load(file)

messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant and you need to "
            "engage in a helpful, detailed, polite conversation with a user."
        ),
    },
    {
        "role": "user",
        "content": (
            """find two reddit comments that give tips for making a small brisken pound of meat less than 2 pounds
            give a url of the comment and the user names with actual quotes."""
        ),
    },
]

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="llama-3.1-sonar-large-128k-online",
    messages=messages,
    tools=tools
)
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    if tool_call['function']['name'] == "call_perplexity_ai":
        query = json.loads(tool_call['function']['arguments'])['query']
        # Call the Perplexity AI function
        perplexity_result = call_perplexity_ai(query)
        print(perplexity_result)
else:
    # If no function call is needed, just print the model's response
    print(response.choices[0].message.content)
print(response.choices[0].message.content)
print (type(response))
