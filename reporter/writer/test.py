# import os
# import requests

# # Load the API key from the environment variable
# api_key = os.environ.get("OPENAI_API_KEY")

# # Check if the API key is set
# if not api_key:
#     raise ValueError("OPENAI_API_KEY environment variable is not set")

# # Define the API endpoint for GPT-4
# url = "https://api.openai.com/v1/chat/completions"

# # Set up the headers including the Authorization with the API key
# headers = {
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }

# # Define the data payload
# data = {
#     "model": "gpt-4",
#     "messages": [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Write a short story about a brave knight and a dragon."}
#     ],
#     "max_tokens": 50,
#     "temperature": 0.7
# }

# # Make the POST request to the GPT-4 API
# response = requests.post(url, headers=headers, json=data)

# # Check if the request was successful
# if response.status_code == 200:
#     response_data = response.json()
#     print(response_data['choices'][0]['message']['content'].strip())
# else:
#     print(f"Request failed with status code {response.status_code}")
#     print(response.text)


from sheetscall import sheets_call 
data = [['id', 'billname', 'billnumber', 'writingtitle', 'lawexplanation', 'test column'], 
        ['1', 'billnametest1', 'billnumbertest1', 'this is a working title and an explanation', '', 'test column value'], 
        ['2', 'billnametest2', '', '', '', 'test columnn value 2']]

# Extract headers
headers = data[0]

# Initialize a list to hold all row dictionaries
all_rows = []

# Loop through each row (skipping the header row)
for row in data[1:]:
    row_dict = {}  # Initialize an empty dictionary for each row
    for i in range(len(headers)):
        print (headers[i])
        print (row[i])
        row_dict[headers[i]] = row[i]  # Assign each header as a key and the corresponding row value as the value
    all_rows.append(row_dict)  # Append the row dictionary to the list

# Print the result
print(all_rows)

print (sheets_call())