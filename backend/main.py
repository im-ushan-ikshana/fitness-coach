from fastapi import FastAPI, HTTPException, Header, Path
from pydantic import BaseModel

import os
import asyncio

import uuid  # Generate unique session IDs
from backend.models.RuleBasedRecommender import RuleBasedRecommender
from backend.nlp.GPTWorkoutGenerator import GPTWorkoutGenerator
from backend.utils.SessionManager import SessionManager
from backend.nlp.PromptTemplates import PromptTemplates

from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

print("API Key:", os.getenv("OPENAI_API_KEY")) 

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize required classes
workout_generator = GPTWorkoutGenerator()
session_manager = SessionManager()

# User input model (Now includes workout_location)
class UserInput(BaseModel):
    weight: float
    height: float
    gender: int
    age: int
    hypertension: str
    diabetes: str
    fitness_goal: str  # Muscle Gain, Weight Loss, Weight Gain
    workout_preference: str  # Cardio, Strength Training, Mixed
    workout_location: str  # Home or Gym
    duration: str  # 1 week, 2 weeks, 1 month, etc.
    experience_level: str  # Beginner, Intermediate, Expert (User-defined)
    
# Define request model for user concerns
class UserConcernRequest(BaseModel):
    concern: str

@app.post("/generate-workout")
async def generate_workout(user_input: UserInput, session_id: str = Header(default=None)):
    """Process user input, use rule-based logic, and generate a GPT-based workout plan asynchronously."""

    try:
        print("Received user input:", user_input.dict())

        # Generate new session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
            print(f"New session created: {session_id}")

        # Calculate BMI dynamically inside RuleBasedRecommender
        bmi = RuleBasedRecommender.calculate_bmi(user_input.weight, user_input.height)
        print("Calculated BMI:", bmi)

        # Get recommendation level using the rule-based system
        recommendation_level = RuleBasedRecommender.get_recommendation_level(
            user_input.weight, user_input.height, user_input.age, 
            user_input.hypertension, user_input.diabetes
        )

        print("Rule-Based Recommendation Level:", recommendation_level)

        # Store user data in session (now includes calculated BMI and workout location)
        user_data = user_input.dict()
        user_data["bmi"] = bmi  # Store calculated BMI in session
        user_data["recommendation_level"] = recommendation_level
        session_manager.create_session(session_id, user_data)

        # **Generate GPT-based prompts**
        fitness_analysis_prompt = PromptTemplates.user_fitness_analysis(user_input, recommendation_level, bmi)
        workout_prompt = PromptTemplates.workout_plan_prompt(user_input)
        nutrition_prompt = PromptTemplates.nutrition_tips_prompt(user_data, bmi)

        # **Send prompts to GPT asynchronously**
        fitness_analysis, workout_plan, nutrition_tips = await asyncio.gather(
            workout_generator.generate_response_async(fitness_analysis_prompt),
            workout_generator.generate_response_async(workout_prompt),
            workout_generator.generate_response_async(nutrition_prompt)
        )

        # **Return structured JSON response**
        return {
            "session_id": session_id,
            "bmi": bmi,
            "recommendation_level": recommendation_level,
            "fitness_analysis": fitness_analysis,
            "workout_plan": workout_plan,
            "nutrition_tips": nutrition_tips
        }

    except Exception as e:
        print("ERROR in /generate-workout:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/generate-nutrition")
async def generate_nutrition(session_id: str = Header(..., alias="session_id")):
    """Generate nutrition tips based on stored session data."""
    
    try:
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")

        # Retrieve session data
        user_data = session_manager.get_session(session_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Generate GPT-based nutrition tips
        nutrition_prompt = PromptTemplates.nutrition_tips_prompt(user_data)
        nutrition_tips = workout_generator.generate_response(nutrition_prompt)

        return {
            "session_id": session_id,
            "nutrition_tips": nutrition_tips
        }

    except Exception as e:
        print("ERROR in /generate-nutrition:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/user-concerns/{session_id}")
async def user_concerns(session_id: str = Path(...), concern_request: UserConcernRequest = None):
    """
    Handles user concerns and generates a structured GPT response,
    referencing past user details if available.
    """

    # Retrieve user session data
    session_data = session_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found.")

    # Validate user concern input
    if not concern_request or not concern_request.concern:
        raise HTTPException(status_code=400, detail="User concern is required.")

    # Fetch user's previous details for GPT reference
    user_profile_summary = f"""
    **User Profile (For Context):**
    - **Fitness Goal:** {session_data.get("fitness_goal", "Not provided")}
    - **Experience Level:** {session_data.get("experience_level", "Not provided")}
    - **Workout Preference:** {session_data.get("workout_preference", "Not provided")}
    - **Workout Location:** {session_data.get("workout_location", "Not provided")}
    - **Medical Conditions:** Hypertension: {session_data.get("hypertension", "No")}, Diabetes: {session_data.get("diabetes", "No")}
    """

    # Generate GPT prompt for user concern
    concern_prompt = PromptTemplates.custom_user_concerns(concern_request.concern)

    # Combine user context with concern prompt
    final_prompt = f"""
    {user_profile_summary}

    {concern_prompt}
    """

    # Send prompt to GPT asynchronously for response generation
    gpt_response = await workout_generator.generate_response_async(final_prompt)

    return {
        "session_id": session_id,
        "user_concern": concern_request.concern,
        "response": gpt_response
    }

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Retrieve user session data."""
    session_data = session_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"session_id": session_id, "user_data": session_data}


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear user session data."""
    session_manager.delete_session(session_id)
    return {"message": "Session cleared", "session_id": session_id}


