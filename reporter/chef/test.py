from chefwriter import AIHandler
from perplexitychef import perplexitycall

# handler = AIHandler()

# # handler.agentchat("""name one random dessert from the provided context then search reddit for desserts that may meet greg's preferences. give a url and user name in your answer and give an explanation.""")

# successful_message = [
#     {
#         'role': 'user',
#         'content': "\n    You're getting user information. \n    browse brisket\n    "
#     }
# ]

# failed_message = [
#     {
#         'role': 'user',
#         'content': """
#     You're getting user information. 
#     browse brisket
#     """
#     },
#     {
#         'role': 'assistant',
#         'content': None,
#         'tool_calls': [
#             {
#                 'id': 'call_tuwqXZwIuJOomdkestaGK9Hc',
#                 'type': 'function',
#                 'function': {
#                     'name': 'perplexitycall',
#                     'arguments': '{"query":"brisket recipe"}'
#                 }
#             }
#         ],
#         'refusal': None
#     },
#     {
#         'role': 'assistant',
#         'content': 'Here’s a detailed guide on how to prepare a smoked brisket, which aligns well with your preferences for recipes that include meat:\n\n### Selecting the Brisket\n1. **Fat Cap**: Choose a brisket with an evenly trimmed fat cap; avoid ones with deep cuts into the fat side.\n2. **Marbling**: Look for briskets that have good intramuscular fat ("marbling") in the flat to ensure tenderness and flavor.\n3. **Shape**: Ensure that the brisket is pliable and uniformly thick.\n\n### Trimming\n- Trim any oxidized edges and create a uniform shape for even cooking.\n\n### Seasoning\n- Use a simple seasoning blend (salt, pepper, garlic powder) and a binder like mustard or pickle juice to help the seasonings adhere.\n\n### Smoking Temperature and Position\n1. **Initial Cooking**: Start smoking at a low temperature (225°F to 250°F). Position the brisket fat side up to protect the meat.\n2. **Adjustment**: Monitor cooking and adjust temperatures as needed to prevent drying.\n\n### Wrapping\n- Wrap the brisket in foil or butcher paper when it reaches the stall phase (160-170°F). Make sure to wrap tightly to retain moisture.\n\n### Resting and Finishing\n- Finish cooking until an internal temperature of 199°F to 200°F is reached. Let it rest for a few hours before slicing to allow juices to redistribute.\n\n### Additional Tips\n- Use temperature probes for accurate monitoring.\n- Cover any quickly darkening areas with foil to prevent overcooking.\n- Consider wrapping in tallow for additional moisture and flavor.\n\n### Cooking Equipment\nYou can use your smoker or even an Instant Pot for a different style of brisket. However, for traditional smoking, a dedicated smoker would yield the best results.\n\nEnjoy your cooking, and let me know if you need more specific recipes or variations!',
#         'refusal': None
#     },
#     {
#         'role': 'user',
#         'content': """
#     You're getting user information. 
#     browse a modification of this recipe from a reddit user within the last year. tell
# me the user name and link. it should align with greg’s preferences. explain your answer
#     """
#     }
# ]




query = "find me a recipe for sweet potatoes."

message = [{"role": "user", "content": query}]

print(perplexitycall(message))
