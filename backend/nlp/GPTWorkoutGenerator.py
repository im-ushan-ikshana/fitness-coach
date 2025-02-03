import asyncio
from backend.nlp.GPTClient import GPTClient

class GPTWorkoutGenerator:
    def __init__(self):
        self.gpt_client = GPTClient()

    async def generate_response_async(self, prompt):
        """Asynchronous GPT response generation"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.gpt_client.generate_response, prompt)
