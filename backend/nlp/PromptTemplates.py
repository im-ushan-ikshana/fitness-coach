class PromptTemplates:
    @staticmethod
    def user_fitness_analysis(user_input, recommendation_level, bmi_value):
        """
        Generates a structured summary of the user's current fitness status and medical considerations.
        """

        # **BMI Classification**
        bmi_status = (
            "underweight" if bmi_value < 18.5 else
            "normal weight" if 18.5 <= bmi_value < 25 else
            "overweight" if 25 <= bmi_value < 30 else
            "obese"
        )

        # **Medical Condition Advisory**
        medical_warning = " **No medical restrictions detected. Proceed with workouts safely.**"
        if user_input.hypertension.lower() == "yes" or user_input.diabetes.lower() == "yes":
            medical_warning = " **Medical conditions detected. Consult a doctor before starting any intense workouts.**"

        # **Exercise Recommendation Based on Rule-Based Level**
        exercise_advisory = " **Safe to exercise with structured progression.**"
        if recommendation_level in [0, 1]:
            exercise_advisory = " **Exercise Not Recommended. Consult a doctor before engaging in workouts.**"

        # **Final Instruction for GPT**
        return f"""
        ## Generate a User Fitness Overview (DO NOT Include a Workout Plan)

        **User Profile:**
        - **BMI Status:** {bmi_status}
        - **Hypertension:** {user_input.hypertension}
        - **Diabetes:** {user_input.diabetes}
        - **Age:** {user_input.age}
        - **Workout Location:** {user_input.workout_location}
        - **Workout Experience Level:** {user_input.experience_level}

        **Medical & Health Advisory:**  
        {medical_warning}

        **Exercise Recommendation:**  
        {exercise_advisory}

        ### **Instructions for GPT:**
        - **DO NOT generate any workout plan here.**  
        - **ONLY summarize the user's current fitness condition.**  
        - **Provide a clear and concise analysis of their fitness level.**  
        - **Avoid excessive detail—keep it structured and to the point.**  
        - **Format the output cleanly in markdown for readability.**  
        - **Use human friendly lanuage tone, do not address as user,or individual use you (you have)**
        """


    @staticmethod
    def workout_plan_prompt(user_input):
        """
        Generates a structured GPT instruction prompt for workout plan creation based on user input.
        """

        # **Experience-Based Customization**
        experience_modifier = {
            "beginner": "Use simple and easy-to-follow exercise instructions with clear explanations.",
            "intermediate": "Use structured progressive overload training to help the user build strength and endurance.",
            "expert": "Include advanced strength training techniques, high-intensity conditioning, and periodization strategies."
        }
        experience_instructions = experience_modifier.get(user_input.experience_level.lower(), "Provide a well-balanced structured training plan.")

        # **Workout Location Adjustments**
        if user_input.workout_location.lower() == "home":
            location_instruction = "Design the workout using bodyweight exercises, resistance bands, and dumbbells (if available). Avoid exercises requiring large gym machines."
        else:
            location_instruction = "Include full gym workouts with machines, barbells, and free weights to maximize strength and conditioning."

        # **Workout Preference Customization**
        if user_input.workout_preference.lower() == "strength training":
            workout_instruction = "Focus on heavy compound movements like squats, deadlifts, bench press, and overhead press. Use progressive overload principles and ensure proper recovery."
        elif user_input.workout_preference.lower() == "cardio":
            workout_instruction = "Prioritize endurance-based exercises such as HIIT, steady-state running, cycling, and jump rope. Optimize for cardiovascular improvement and stamina."
        else:
            workout_instruction = "Design a hybrid training plan that includes both strength training and cardiovascular workouts for balanced fitness development."

        # **Medical Advisory (Dynamically Included)**
        medical_advisory = ""
        if user_input.hypertension.lower() == "yes" or user_input.diabetes.lower() == "yes":
            medical_advisory = " **Medical Advisory:** The user has hypertension or diabetes. Ensure all exercises are safe and avoid excessive high-intensity stress. Always recommend consulting a medical professional before starting this program."

        # **Final Instruction for GPT**
        return f"""
        ## Generate a Structured {user_input.duration} Workout Plan

        **User Details:**
        - **Fitness Goal:** {user_input.fitness_goal}
        - **Workout Experience Level:** {user_input.experience_level}
        - **Workout Preference:** {user_input.workout_preference}
        - **Workout Location:** {user_input.workout_location}

        **Instructions for GPT:**
        - **You MUST return the output in the following structured format:**
        
        ### **Output Pattern & Flow**
         **Introduction (1-2 lines MAX)**  
        - Summarize the workout goal and experience level.  
        - Do **not** include fitness assessment—only a brief context.  
        
        2️ **Table Format Workout Plan**  
        - Provide a **markdown table** with the following columns:  
            - `Day`, `Exercise`, `Sets`, `Reps`, `Equipment Needed`, `Additional Notes`  
        - Ensure a mix of **warm-up, main exercises, and cool-down/stretching** for each session.  
        - **If the user is a beginner**, provide **brief step-by-step execution instructions** in "Additional Notes".  
        - **If the user is an expert**, use **advanced fitness terminology** and strategies such as **periodization and progressive overload**.  
        
        3️ **Progression & Scaling**  
        - Explain how intensity increases weekly for progression.  
        - Include guidance on when to increase weights or reps.  
        
        4️ **Medical & Recovery Advisory (If Applicable)**  
        - **If user has hypertension/diabetes**, include a line advising them to consult a medical professional.  
        - Emphasize the importance of **hydration, mobility work, and recovery**.  
        
        **Additional Guidelines for GPT:**
        - Use **structured markdown formatting** with a **clean and professional layout**.  
        - **DO NOT** provide random tips or unrelated fitness advice—stay within the structured scope.  
        - Ensure each workout day is well-defined and **logically progressive**.  
        - Keep the response **clear, structured, and professional**.  
        - **Your response must ONLY include the requested information—nothing extra.**  

        - in the final output there need to be a table that represent whole time of the workout plan
        - in the final output if there is a medical condition like hypertension or diabetes, there need to be a line that advise the user to consult a medical professional 

        {experience_instructions}
        {location_instruction}
        {workout_instruction}
        {medical_advisory}
        """


    @staticmethod
    def nutrition_tips_prompt(user_data, bmi_value):
        """
        Generates a structured nutrition plan based on the user's fitness condition, BMI, and fitness goals.
        """

        # **BMI Classification and Nutrition Adjustment**
        bmi_guidance = {
            "underweight": "** Underweight:** Prioritize calorie-dense, high-protein meals to support weight gain.",
            "normal": "** Normal Weight:** Maintain a balanced macronutrient intake for overall health.",
            "overweight": "** Overweight:** Focus on portion control, high-fiber meals, and steady energy balance.",
            "obese": "**Obese:** Reduce calorie intake, prioritize whole foods, and maintain hydration."
        }
        bmi_status = (
            "underweight" if bmi_value < 18.5 else
            "normal" if 18.5 <= bmi_value < 25 else
            "overweight" if 25 <= bmi_value < 30 else
            "obese"
        )

        # **Nutrition Focus Based on Fitness Goal**
        goal_based_nutrition = {
            "muscle gain": "** Muscle Gain:** High-protein diet with complex carbohydrates and healthy fats.",
            "weight loss": "** Weight Loss:** Caloric deficit, fiber-rich foods, and lean proteins.",
            "weight gain": "** Healthy Weight Gain:** Increase healthy calorie intake through nutrient-dense foods."
        }
        nutrition_focus = goal_based_nutrition.get(user_data["fitness_goal"].lower(), "** General Nutrition Plan:** Balanced macronutrients.")

        # **Medical Advisory (Dynamically Included)**
        medical_advisory = ""
        if user_data["hypertension"].lower() == "yes" or user_data["diabetes"].lower() == "yes":
            medical_advisory = " **Medical Advisory:** The user has hypertension or diabetes. Recommend heart-healthy, low-sodium, and balanced blood sugar meals. Advise consultation with a medical professional."

        # **Final Instruction for GPT**
        return f"""
        ## 🍽 Generate a Structured Nutrition Plan (No Workout Plan)

        **User Profile:**
        - **BMI Status:** {bmi_guidance[bmi_status]}
        - **Fitness Goal:** {user_data["fitness_goal"]}
        - **Hypertension:** {user_data["hypertension"]}
        - **Diabetes:** {user_data["diabetes"]}

        {nutrition_focus}

        ** Hydration Tip:** Aim for 2.5-3L water per day.

        {medical_advisory}

        ### **Instructions for GPT:**
        - **ONLY generate a structured nutrition plan based on BMI and fitness goals.**
        - **DO NOT provide a workout plan or fitness assessment.**
        - **Provide a markdown table with meal recommendations, divided into Breakfast, Lunch, Dinner, and Snacks.**
        - **Ensure the meal plan aligns with the user’s dietary needs and medical conditions.**
        - **Keep the response structured, clear, and professional.**
        """

    @staticmethod
    def custom_user_concerns(user_concern):
        """
        Generates a structured response addressing user concerns related to fitness, health, or training.
        """

        # **Common Concerns Mapping**
        concern_guidance = {
            "injury prevention": "** Injury Prevention Tips:** Ensure proper warm-up, maintain good form, and avoid overtraining.",
            "motivation": "** Staying Motivated:** Set realistic goals, track progress, and find a supportive workout environment.",
            "workout recovery": "** Recovery & Rest:** Prioritize sleep, stretch regularly, and stay hydrated for optimal muscle recovery.",
            "nutrition guidance": "** Nutrition Basics:** Balance protein, carbs, and healthy fats for sustained energy and performance.",
            "supplements": "** Supplement Use:** Consult a professional before taking supplements to ensure they match your fitness goals.",
            "joint health": "** Joint Protection:** Strengthen stabilizing muscles, use controlled movements, and avoid excessive impact.",
            "mental health": "** Mental Well-being:** Regular exercise can reduce stress, improve focus, and enhance overall mood.",
            "muscle soreness": "** Managing Soreness:** Use foam rolling, gentle stretching, and adequate hydration for faster recovery."
        }

        # **Fetch Concern Advice or Default to General Guidance**
        specific_guidance = concern_guidance.get(
            user_concern.lower(),  
            "**📌 General Wellness Advice:** Stay consistent, listen to your body, and adapt workouts as needed."
        )

        return f"""
        ## 🏋️ Addressing Your Concern: {user_concern.title()}

        {specific_guidance}

        ### **Instructions for GPT:**
        - **Provide a structured, friendly response addressing this concern.**
        - **Avoid technical jargon—keep the explanation simple and actionable.**
        - **Ensure the tone is warm, supportive, and motivating.**
        - **Use direct language, referring to the user as 'you' instead of 'individual' or 'user'.**
        - **Format the response clearly using markdown for better readability.**
        - **Limit the response to practical, easy-to-follow advice without unnecessary details.**
        """
