import requests
import anthropic
import os

class AIHandler:
    def __init__(self, openai_key=None, anthropic_key=None):
        self.openai_key = openai_key or os.environ.get('OPENAI_API_KEY')
        self.anthropic_key = anthropic_key or os.environ.get('ANTHROPIC_API_KEY')
        
        # Initialize Anthropic client
        self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)
        
        # Placeholder for extended context
        self.extended_context = """
        Here are a few articles written about the current state of 
        psychedelics policy in the United States. Draw from each one when writing your own article from the prompt.
        """

    def openai_request(self, prompt):
        # Combine the extended context with the user prompt
        full_prompt = self.extended_context + "\n\nUser Prompt: " + prompt
        
        messages = [
            {"role": "system", "content": "You are an expert writer specializing in psychedelics policy."},
            {"role": "user", "content": full_prompt}
        ]
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={'Authorization': f'Bearer {self.openai_key}'},
            json={'model': 'gpt-4-turbo', 'messages': messages, 'temperature': 0.5, 'max_tokens': 256},
            timeout=30
        )
        
        print('DEBUG: OpenAI response code', response.status_code)
        
        response_data = response.json()
        message_content = response_data.get('choices', [{}])[0].get('message', {}).get('content', "Sorry, I couldn't process your request.")
        return message_content
    
    def claude_request(self, prompt):
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
        
        response = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0,
            messages=messages
        )
        
        return response.content
    
    def get_combined_responses(self, prompt):
        openai_response = self.openai_request(prompt)
        claude_response = self.claude_request(prompt)
        
        return {
            "OpenAI": openai_response,
            "Claude": claude_response
        }

# Example usage
handler = AIHandler(openai_key="your_openai_api_key", anthropic_key="your_anthropic_api_key")
user_input = "Write a 200-word news article about the state of congressional policy for psychedelics, including background on current state policies."

responses = handler.get_combined_responses(user_input)
print("OpenAI Response:\n", responses["OpenAI"])
print("\nClaude Response:\n", responses["Claude"])
