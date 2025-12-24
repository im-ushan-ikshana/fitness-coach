import asyncio
import hashlib
from nlp.GPTClient import GPTClient

class GPTWorkoutGenerator:
    def __init__(self):
        self.gpt_client = GPTClient()
        self.cache = {}  # Simple in-memory cache

    def _get_cache_key(self, prompt):
        """Generate a cache key from the prompt."""
        return hashlib.sha256(prompt.encode()).hexdigest()

    async def generate_response_async(self, prompt):
        """Asynchronous GPT response generation with caching."""
        cache_key = self._get_cache_key(prompt)
        
        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Generate new response
        response = await loop.run_in_executor(None, self.gpt_client.generate_response, prompt)
        
        # Cache the response
        self.cache[cache_key] = response
        
        return response

    def clear_cache(self):
        """Clear the response cache."""
        self.cache.clear()
        return {"message": "Cache cleared successfully"}
