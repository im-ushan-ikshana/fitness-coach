from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import openai  # Install via 'pip install openai'
import pickle
import pandas as pd
from backend.models.InferencePipeline import InferencePipeline
from backend.models.PreprocessorPipeline import PreprocessorPipeline
from backend.models.ModelTrainer import ModelTrainer

from fastapi.middleware.cors import CORSMiddleware

# Load environment variables for OpenAI API Key
OPENAI_API_KEY = "your-openai-api-key"

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Change this to ["http://localhost:3000"] for better security
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allows all headers
)

# Paths
MODEL_PATH = os.path.join('backend', 'models', 'recommend_model.pkl')
PIPELINE_PATH = os.path.join('backend', 'models', 'recommend_preprocessor_pipeline.pkl')

# Load the trained model and preprocessing pipeline
trainer = ModelTrainer()
model = trainer.load_model(MODEL_PATH)

pipeline = PreprocessorPipeline()
pipeline.load_pipeline(PIPELINE_PATH)

inference = InferencePipeline(pipeline=pipeline, model=model)


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


def generate_workout_plan(recommendation_level, user_input):
    """Generate workout plan using GPT based on recommendation level and user data."""

    prompt = f"""
    Create a {user_input.duration} workout plan for a person with the following details:
    - Gender: {user_input.gender}
    - Age: {user_input.age}
    - BMI: {user_input.bmi}
    - Hypertension: {user_input.hypertension}
    - Diabetes: {user_input.diabetes}
    - Fitness Goal: {user_input.fitness_goal}
    - Workout Preference: {user_input.workout_preference}
    - Recommendation Level: {recommendation_level} (scale 0-5, 0=Beginner, 5=Expert)

    Provide a structured plan with a daily breakdown of exercises, including sets, reps, and duration.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error generating workout plan: {str(e)}"


@app.post("/generate-workout")
async def generate_workout(user_input: UserInput):
    """Process user input, predict recommendation level, and generate a workout plan."""

    # Prepare user data correctly
    user_dict = user_input.dict()
    user_data = pd.DataFrame([user_dict])  # Convert to DataFrame properly
    user_data = user_data[['weight', 'height', 'bmi', 'age']]  # Keep only numeric columns

    print("User Data Before Prediction:", user_data)  # Debugging line

    # Predict recommendation level
    try:
        recommendation_level = inference.predict(user_data, numeric_columns=['weight', 'height', 'bmi', 'age'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in model prediction: {str(e)}")

    # Generate GPT workout plan
    workout_plan = generate_workout_plan(recommendation_level, user_input)

    return {
        "recommendation_level": int(recommendation_level),
        "workout_plan": workout_plan
    }
