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

    @staticmethod
    def progress_adjustment_prompt(user_data, progress_data):
        """
        Generates a prompt for GPT to analyze user progress and suggest workout adjustments.
        """
        
        # Extract recent workouts and measurements
        workouts = progress_data.get("workouts", [])
        measurements = progress_data.get("measurements", [])
        
        # Format progress data for GPT
        workout_summary = ""
        if workouts:
            recent_workouts = workouts[-5:]  # Last 5 workouts
            workout_summary = "\n".join([
                f"- {w['date']}: {w['exercise']} - {w['sets']} sets x {w['reps']} reps" + 
                (f" @ {w['weight']}kg" if w.get('weight') else "")
                for w in recent_workouts
            ])
        else:
            workout_summary = "No workout logs available."
            
        measurement_summary = ""
        if measurements:
            recent_measurements = measurements[-3:]  # Last 3 measurements
            measurement_summary = "\n".join([
                f"- {m['date']}: Weight: {m.get('weight', 'N/A')}kg, Measurements: {m.get('measurements', {})}"
                for m in recent_measurements
            ])
        else:
            measurement_summary = "No measurements logged."

        return f"""
        ## 📊 Analyze User Progress and Suggest Workout Adjustments

        **User Profile:**
        - **Fitness Goal:** {user_data.get("fitness_goal", "Not specified")}
        - **Experience Level:** {user_data.get("experience_level", "Not specified")}
        - **Current BMI:** {user_data.get("bmi", "Not calculated")}
        - **Medical Conditions:** Hypertension: {user_data.get("hypertension", "No")}, Diabetes: {user_data.get("diabetes", "No")}

        **Recent Workout Logs:**
        {workout_summary}

        **Recent Measurements:**
        {measurement_summary}

        ### **Instructions for GPT:**
        - **Analyze the user's progress based on workout logs and measurements.**
        - **Suggest specific adjustments to their current workout plan.**
        - **Consider their fitness goal, experience level, and any medical conditions.**
        - **Provide actionable recommendations for progression or modification.**
        - **If progress is good, suggest increasing intensity or adding variations.**
        - **If progress is slow, suggest technique improvements or recovery focus.**
        - **Keep suggestions realistic and safe.**
        - **Format the response clearly with sections for different types of adjustments.**
        """

    @staticmethod
    def meal_plan_prompt(user_data, meal_request):
        """
        Generates a prompt for GPT to create a detailed meal plan with recipes.
        """
        
        dietary_info = ""
        if meal_request.dietary_restrictions:
            dietary_info = f"**Dietary Restrictions:** {', '.join(meal_request.dietary_restrictions)}"
            
        cuisine_info = ""
        if meal_request.cuisine_preferences:
            cuisine_info = f"**Cuisine Preferences:** {', '.join(meal_request.cuisine_preferences)}"
            
        calorie_info = ""
        if meal_request.calories_per_day:
            calorie_info = f"**Target Daily Calories:** {meal_request.calories_per_day}"

        return f"""
        ## 🍽️ Generate a Detailed Meal Plan with Recipes

        **User Profile:**
        - **Fitness Goal:** {user_data.get("fitness_goal", "Not specified")}
        - **BMI:** {user_data.get("bmi", "Not calculated")}
        - **Medical Conditions:** Hypertension: {user_data.get("hypertension", "No")}, Diabetes: {user_data.get("diabetes", "No")}
        {dietary_info}
        {cuisine_info}
        {calorie_info}
        - **Meals per Day:** {meal_request.meals_per_day}

        ### **Instructions for GPT:**
        - **Create a 7-day meal plan with recipes for each meal.**
        - **Include breakfast, lunch, dinner, and snacks as appropriate.**
        - **For each meal, provide:**
          - **Recipe name**
          - **Ingredients with quantities**
          - **Simple cooking instructions**
          - **Nutritional estimates (protein, carbs, fats, calories)**
        - **Ensure meals align with fitness goals and medical conditions.**
        - **Respect dietary restrictions and cuisine preferences.**
        - **Make recipes practical and easy to prepare.**
        - **Format the response clearly with days and meal sections.**
        - **Include shopping list suggestions at the end.**
        """

    @staticmethod
    def voice_coach_prompt(voice_command, session_data):
        """
        Generates a prompt for AI voice coaching during workouts.
        """
        
        user_profile = f"""
        **User Profile:**
        - Fitness Goal: {session_data.get("fitness_goal", "Not specified")}
        - Experience Level: {session_data.get("experience_level", "Not specified")}
        - Current Workout: {session_data.get("current_workout", "Not specified")}
        - Medical Conditions: Hypertension: {session_data.get("hypertension", "No")}, Diabetes: {session_data.get("diabetes", "No")}
        """

        return f"""
        ## 🎙️ AI Voice Coach Response

        {user_profile}

        **User Voice Command:** "{voice_command}"

        ### **Instructions for AI:**
        - **Respond as a real-time workout coach** giving immediate feedback
        - **Keep responses concise and actionable** (under 30 seconds of speech)
        - **Use encouraging, motivational language**
        - **Provide specific form cues, breathing tips, or motivation**
        - **Adapt to user's experience level and current workout**
        - **If command is unclear, ask for clarification**
        - **Include timing cues or rep suggestions when relevant**
        - **End with a question to continue engagement**
        """

    @staticmethod
    def photo_analysis_prompt(progress_photo, session_data):
        """
        Generates a prompt for AI analysis of progress photos.
        """
        
        photo_context = f"""
        **Photo Context:**
        - Type: {progress_photo.photo_type}
        - Date: {progress_photo.date}
        - User Goal: {session_data.get("fitness_goal", "Not specified")}
        """

        return f"""
        ## 📸 AI Progress Photo Analysis

        {photo_context}

        **Analysis Instructions:**
        - **Note: This is a text-based simulation. In production, this would use computer vision AI.**
        - **Provide encouraging feedback** about visible progress
        - **Suggest specific improvements** in form or technique
        - **Comment on muscle definition, posture, or body composition changes**
        - **Give realistic timeline expectations** for results
        - **Motivate continued consistency**
        - **Keep analysis positive and supportive**
        """

    @staticmethod
    def mood_coaching_prompt(mood_input, session_data):
        """
        Generates a prompt for mood-based workout coaching.
        """
        
        mood_context = f"""
        **Current Mood State:**
        - Mood: {mood_input.mood}
        - Energy Level: {mood_input.energy_level}/10
        - Stress Level: {mood_input.stress_level}/10
        - User Goal: {session_data.get("fitness_goal", "Not specified")}
        """

        return f"""
        ## 😊 AI Mood-Based Coaching

        {mood_context}

        ### **Instructions for AI:**
        - **Adapt workout intensity** based on energy and stress levels
        - **Provide emotional support** and motivation tailored to current mood
        - **Suggest appropriate workout modifications** for low energy days
        - **Include mindfulness or breathing exercises** if stress is high
        - **Create a personalized workout plan** for this specific session
        - **Focus on mental benefits** of exercise for mood improvement
        - **Keep coaching empathetic and understanding**
        """

    @staticmethod
    def ai_companion_prompt(message, personality, session_data):
        """
        Generates a prompt for AI workout companion with different personalities.
        """
        
        personality_traits = {
            "motivational": "High-energy, extremely encouraging, uses lots of exclamation points and positive affirmations",
            "strict": "Disciplined, no-nonsense, focuses on consistency and pushing limits",
            "friendly": "Warm, conversational, like a supportive friend who cares about your well-being",
            "humorous": "Witty, uses jokes and sarcasm to keep things light while motivating"
        }
        
        companion_style = personality_traits.get(personality, personality_traits["motivational"])

        return f"""
        ## 🤖 AI Workout Companion ({personality.title()} Personality)

        **Personality Style:** {companion_style}

        **User Message:** "{message}"

        **User Context:**
        - Fitness Goal: {session_data.get("fitness_goal", "Not specified")}
        - Experience Level: {session_data.get("experience_level", "Not specified")}

        ### **Instructions for AI:**
        - **Stay in character** with the specified personality throughout
        - **Respond conversationally** as if chatting with a workout buddy
        - **Provide workout advice, motivation, or answers to questions**
        - **Keep responses engaging and personality-consistent**
        - **Reference user's goals and progress when relevant**
        - **End with a question to continue the conversation**
        """

    @staticmethod
    def performance_prediction_prompt(session_data, progress_data):
        """
        Generates a prompt for AI performance prediction.
        """
        
        workouts = progress_data.get("workouts", [])
        measurements = progress_data.get("measurements", [])
        
        progress_summary = f"""
        **Progress Summary:**
        - Total Workouts Logged: {len(workouts)}
        - Recent Measurements: {len(measurements)}
        - Current BMI: {session_data.get("bmi", "Not calculated")}
        - Fitness Goal: {session_data.get("fitness_goal", "Not specified")}
        """

        return f"""
        ## 🔮 AI Performance Prediction

        {progress_summary}

        ### **Instructions for AI:**
        - **Analyze workout consistency and progress patterns**
        - **Predict future performance** based on current trajectory
        - **Estimate timeline** for reaching fitness goals
        - **Identify potential plateaus** and suggest breakthroughs
        - **Provide realistic expectations** and motivational insights
        - **Suggest data-driven adjustments** to accelerate progress
        - **Focus on both short-term and long-term predictions**
        """

    @staticmethod
    def smart_goals_prompt(session_data, progress_data):
        """
        Generates a prompt for AI-powered dynamic goal setting.
        """
        
        current_goal = session_data.get("fitness_goal", "Not specified")
        progress_summary = f"""
        **Current Status:**
        - Goal: {current_goal}
        - Progress Data Points: {len(progress_data.get("workouts", []))} workouts, {len(progress_data.get("measurements", []))} measurements
        - Experience Level: {session_data.get("experience_level", "Not specified")}
        """

        return f"""
        ## 🎯 AI Smart Goal Setting

        {progress_summary}

        ### **Instructions for AI:**
        - **Analyze current progress** and goal achievement potential
        - **Set SMART goals** (Specific, Measurable, Achievable, Relevant, Time-bound)
        - **Create milestone-based progression** with intermediate goals
        - **Adjust goals dynamically** based on user's actual performance
        - **Include both outcome goals and process goals**
        - **Suggest goal categories**: fitness, nutrition, consistency, strength, etc.
        - **Provide tracking methods** and success metrics
        - **Make goals challenging but realistic**
        """

    @staticmethod
    def realtime_feedback_prompt(feedback, session_data):
        """
        Generates a prompt for real-time workout feedback.
        """
        
        feedback_context = f"""
        **Real-time Feedback Data:**
        - Exercise: {feedback.exercise}
        - Sets Completed: {feedback.sets_completed}
        - Reps Completed: {feedback.reps_completed}
        - Weight Used: {feedback.weight_used or 'Bodyweight'}
        - Perceived Difficulty: {feedback.perceived_difficulty}/10
        - Form Quality: {feedback.form_quality or 'Not assessed'}
        - User Experience: {session_data.get("experience_level", "Not specified")}
        """

        return f"""
        ## ⚡ AI Real-Time Workout Feedback

        {feedback_context}

        ### **Instructions for AI:**
        - **Provide immediate, actionable feedback** on form and technique
        - **Give specific correction cues** if form needs improvement
        - **Suggest weight/reps adjustments** based on perceived difficulty
        - **Offer encouragement** and progress acknowledgment
        - **Predict next set performance** and give preparation tips
        - **Keep feedback concise** (speakable in 15-20 seconds)
        - **End with motivation** for the next set
        """

    @staticmethod
    def motivational_content_prompt(content_request, session_data):
        """
        Generates a prompt for personalized motivational content.
        """
        
        content_context = f"""
        **Content Request:**
        - Type: {content_request.content_type}
        - Theme: {content_request.theme or "General motivation"}
        - User Goal: {session_data.get("fitness_goal", "Not specified")}
        - Experience Level: {session_data.get("experience_level", "Not specified")}
        """

        content_instructions = {
            "quote": "Create an inspiring quote about fitness and perseverance",
            "story": "Tell a short, relatable story about overcoming fitness challenges",
            "challenge": "Design a specific, achievable challenge for the next workout",
            "affirmation": "Create positive affirmations for strength and confidence"
        }
        
        instruction = content_instructions.get(content_request.content_type, "Create motivational fitness content")

        return f"""
        ## 💪 AI Motivational Content Generator

        {content_context}

        ### **Instructions for AI:**
        - **{instruction}**
        - **Personalize for user's fitness goal** and experience level
        - **Make it emotionally resonant** and inspiring
        - **Keep content concise** but impactful
        - **Include actionable elements** when appropriate
        - **Use positive, empowering language**
        """

    @staticmethod
    def workout_companion_prompt(action, session_data):
        """
        Generates a prompt for AI workout companion guidance.
        """
        
        action_context = f"""
        **Companion Action:** {action}
        **User Profile:**
        - Goal: {session_data.get("fitness_goal", "Not specified")}
        - Experience: {session_data.get("experience_level", "Not specified")}
        - Current Workout: {session_data.get("current_workout", "Not specified")}
        """

        return f"""
        ## 🏋️ AI Workout Companion Guide

        {action_context}

        ### **Instructions for AI:**
        - **Act as a knowledgeable workout companion** throughout the session
        - **Provide step-by-step guidance** for warm-up, main workout, and cool-down
        - **Give real-time cues** for form, breathing, and pacing
        - **Adapt guidance based on user's experience level**
        - **Include motivational commentary** and progress encouragement
        - **Handle different workout phases**: preparation, execution, recovery
        - **Respond appropriately to the requested action** (start, next_exercise, rest, finish)
        - **Keep guidance conversational and supportive**
        """

    @staticmethod
    def workout_video_prompt(video_request, session_data):
        """
        Generates a prompt for AI workout video concept creation.
        """
        
        video_context = f"""
        **Video Request:**
        - Workout Type: {video_request.workout_type}
        - Duration: {video_request.duration} minutes
        - Intensity: {video_request.intensity}
        - Equipment: {', '.join(video_request.equipment) if video_request.equipment else 'None required'}
        - User Level: {session_data.get("experience_level", "Not specified")}
        - User Goal: {session_data.get("fitness_goal", "Not specified")}
        """

        return f"""
        ## 🎬 AI Workout Video Concept Generator

        {video_context}

        ### **Instructions for AI:**
        - **Create a complete workout video script** with timing breakdown
        - **Include warm-up, main workout, and cool-down segments**
        - **Provide clear exercise demonstrations** with form cues
        - **Add motivational commentary** and breathing instructions
        - **Suggest camera angles and transitions** for professional feel
        - **Include modifications** for different fitness levels
        - **End with progress tracking tips** and next session preview
        - **Make the script engaging and easy to follow**
        """

    @staticmethod
    def dashboard_prompt(session_data, progress_data, dashboard_request):
        """
        Generates a prompt for comprehensive AI fitness dashboard.
        """
        
        dashboard_context = f"""
        **Dashboard Request:**
        - Time Range: {dashboard_request.time_range}
        - Include Predictions: {dashboard_request.include_predictions}
        - Include Recommendations: {dashboard_request.include_recommendations}
        
        **User Overview:**
        - Goal: {session_data.get("fitness_goal", "Not specified")}
        - Experience: {session_data.get("experience_level", "Not specified")}
        - BMI: {session_data.get("bmi", "Not calculated")}
        - Progress Points: {len(progress_data.get("workouts", []))} workouts, {len(progress_data.get("measurements", []))} measurements
        """

        return f"""
        ## 📊 AI Fitness Dashboard

        {dashboard_context}

        ### **Instructions for AI:**
        - **Create a comprehensive fitness overview** with key metrics
        - **Analyze progress trends** and highlight achievements
        - **{"Include performance predictions" if dashboard_request.include_predictions else "Skip predictions"}**
        - **{"Provide personalized recommendations" if dashboard_request.include_recommendations else "Skip recommendations"}**
        - **Include visual progress indicators** (describe charts/graphs)
        - **Highlight strengths and areas for improvement**
        - **Suggest next steps** and motivational insights
        - **Format as an interactive dashboard summary**
        """
