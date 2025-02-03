from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import os
import pandas as pd
import numpy as np
import uuid  # To generate unique session IDs
from backend.models.InferencePipeline import InferencePipeline
from backend.models.PreprocessorPipeline import PreprocessorPipeline
from backend.models.ModelTrainer import ModelTrainer
from backend.nlp.GPTWorkoutGenerator import GPTWorkoutGenerator
from backend.utils.SessionManager import SessionManager

from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
MODEL_PATH = os.path.join('backend', 'models', 'recommend_model.pkl')
PIPELINE_PATH = os.path.join('backend', 'models', 'recommend_preprocessor_pipeline.pkl')

# Load model and pipeline
trainer = ModelTrainer()
model = trainer.load_model(MODEL_PATH)

pipeline = PreprocessorPipeline()
pipeline.load_pipeline(PIPELINE_PATH)

inference = InferencePipeline(pipeline=pipeline, model=model)
workout_generator = GPTWorkoutGenerator()
session_manager = SessionManager()  # Session management instance

# User input model
class UserInput(BaseModel):
    weight: float
    height: float
    bmi: float
    gender: int
    age: int
    hypertension: str
    diabetes: str
    fitness_goal: str  # Muscle Gain, Weight Loss, Weight Gain
    workout_preference: str  # Cardio, Strength Training, Mixed
    duration: str  # 1 week, 2 weeks, 1 month, etc.

@app.post("/generate-workout")
async def generate_workout(user_input: UserInput, session_id: str = Header(default=None)):
    """Process user input, predict recommendation level, and generate a workout plan."""
    
    try:
        print("Received user input:", user_input.dict())  # Debugging

        # If no session ID is provided, generate a new one
        if not session_id:
            session_id = str(uuid.uuid4())  # Generate a new unique session ID
            print(f"New session created: {session_id}")

        # Store user input in session
        session_manager.create_session(session_id, user_input.dict())

        # Convert to dictionary
        user_dict = user_input.dict()

        # Ensure input only contains the necessary numeric columns
        numeric_columns = ['weight', 'height', 'bmi', 'age']
        user_data = {key: user_dict[key] for key in numeric_columns}

        print("Formatted Data for Prediction:", user_data)  # Debugging

        # Predict recommendation level
        recommendation_level = inference.predict([user_data], numeric_columns=numeric_columns)
        print("Raw Prediction Output:", recommendation_level)  # Debugging

        # If recommendation_level is a scalar value, directly use it
        if isinstance(recommendation_level, (int, np.int64)):
            recommendation_level = int(recommendation_level)

        print("Converted recommendation level:", recommendation_level)  # Debugging

        # Generate workout plan
        workout_plan = workout_generator.generate_workout(user_input, recommendation_level)
        print("Generated workout plan:", workout_plan)  # Debugging

        return {
            "session_id": session_id,  # Return session ID to remember user
            "recommendation_level": recommendation_level,
            "workout_plan": workout_plan
        }

    except Exception as e:
        print("ERROR in /generate-workout:", str(e))  # Debugging
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/generate-nutrition")
async def generate_nutrition(session_id: str = Header(..., alias="session_id")):
    """Generate nutrition tips based on stored session data."""
    
    try:
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")

        # Retrieve user session data
        user_data = session_manager.get_session(session_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Generate nutrition tips
        nutrition_tips = workout_generator.generate_nutrition_tips(user_data)

        return {
            "session_id": session_id,
            "nutrition_tips": nutrition_tips
        }

    except Exception as e:
        print("ERROR in /generate-nutrition:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



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



