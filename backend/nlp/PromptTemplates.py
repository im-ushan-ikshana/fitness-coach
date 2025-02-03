class PromptTemplates:
    @staticmethod
    def workout_plan_prompt(user_input, recommendation_level):
        return f"""
        Create a structured {user_input.duration} workout plan for an individual based on the following details:

        - Gender: {user_input.gender}
        - Age: {user_input.age}
        - BMI: {user_input.bmi}
        - Hypertension: {user_input.hypertension} (Specify adjustments needed)
        - Diabetes: {user_input.diabetes} (Mention necessary modifications)
        - Fitness Goal: {user_input.fitness_goal} (Muscle Gain, Weight Loss, Weight Gain)
        - Workout Preference: {user_input.workout_preference} (Cardio, Strength Training, Mixed)
        - Experience Level: {recommendation_level} (scale 0-5, 0=Beginner, 5=Expert)
        
        **Additional Considerations:**
        - If hypertension is present, ensure heart-rate-friendly exercises.
        - If diabetes is present, provide recommendations on insulin-sensitive workouts.
        - Suggest pre- and post-workout meal ideas based on diabetes/hypertension.
        
        Structure the plan with:
        - Daily workouts including exercises, sets, reps, and durations
        - Cardio or stretching routines (if necessary)
        - Rest days and recovery tips
        - Dietary and hydration recommendations to complement the fitness goal

        Provide a **comprehensive** response, formatted clearly for easy readability.
        """

    @staticmethod
    def nutrition_tips_prompt(user_data):
        return f"""
        Generate personalized nutrition tips based on the following user profile:

        - Gender: {user_data['gender']}
        - Age: {user_data['age']}
        - BMI: {user_data['bmi']}
        - Hypertension: {user_data['hypertension']}
        - Diabetes: {user_data['diabetes']}
        - Fitness Goal: {user_data['fitness_goal']}
        - Workout Preference: {user_data['workout_preference']}

        **Key Focus Areas:**
        - **Daily meal suggestions** tailored to the fitness goal.
        - **Macronutrient breakdown** (Protein, Carbs, Fats) based on their activity level.
        - **Foods to avoid** (if hypertension/diabetes is present).
        - **Hydration & Supplement Recommendations**.

        Provide a **structured and detailed** response.
        """
        
