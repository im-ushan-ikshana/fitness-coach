import openai
import os

class GPTClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
        openai.api_key = self.api_key

    def generate_response(self, prompt, model="gpt-4o", temperature=0.7, max_tokens=500):
        """Handles OpenAI API requests using the updated OpenAI client"""
        try:
            client = openai.OpenAI(api_key=self.api_key)  # New API usage
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content  # New response format
        except Exception as e:
            return f"Error generating response: {str(e)}"
