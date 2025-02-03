from backend.nlp.GPTClient import GPTClient
from backend.nlp.PromptTemplates import PromptTemplates

class GPTWorkoutGenerator:
    def __init__(self):
        self.gpt_client = GPTClient()

    def generate_workout(self, user_input, recommendation_level):
        """Generates a workout plan using GPT."""
        prompt = PromptTemplates.workout_plan_prompt(user_input, recommendation_level)
        return self.gpt_client.generate_response(prompt)

    def generate_nutrition_tips(self, user_data):
        """Generates nutrition tips using stored session data."""
        prompt = PromptTemplates.nutrition_tips_prompt(user_data)
        return self.gpt_client.generate_response(prompt)
    
    