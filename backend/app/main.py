from fastapi import FastAPI, HTTPException, Header, Path
from pydantic import BaseModel, Field
from typing import List, Optional

import os
import asyncio
import logging

import uuid  # Generate unique session IDs
from models.RuleBasedRecommender import RuleBasedRecommender
from nlp.GPTWorkoutGenerator import GPTWorkoutGenerator
from utils.SessionManager import SessionManager
from nlp.PromptTemplates import PromptTemplates
from models.youtube_search import YouTubeSearch


from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("API Key:", os.getenv("OPENAI_API_KEY")) 

# Initialize FastAPI
app = FastAPI(
    title="AI Fitness Coach API",
    description="""Revolutionary AI-powered fitness coaching backend featuring:
    
    🤖 **Advanced AI Features:**
    - Voice-powered workout coaching with real-time feedback
    - AI companion chat with multiple personalities
    - Mood-adaptive training recommendations
    - Performance prediction and analytics
    - Smart goal setting with dynamic adjustments
    - Progress photo analysis (simulated)
    - Personalized motivational content generation
    - AI workout video concept creation
    - Comprehensive fitness dashboard with insights
    
    🏋️ **Core Fitness Features:**
    - Personalized workout plan generation
    - Nutrition planning with recipes
    - Progress tracking and logging
    - YouTube workout video search
    - User concern handling
    - Session management
    
    💪 **Powered by GPT-4 and advanced AI algorithms**""",
    version="2.0.0"
)

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

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if the API is running and dependencies are available."""
    health_status = {
        "status": "healthy",
        "openai_api": "available" if os.getenv("OPENAI_API_KEY") else "missing",
        "youtube_api": "available" if os.getenv("YOUTUBE_API_KEY") else "missing",
        "ai_features": {
            "voice_coaching": "enabled",
            "progress_photos": "enabled", 
            "mood_adaptation": "enabled",
            "companion_chat": "enabled",
            "performance_prediction": "enabled",
            "smart_goals": "enabled",
            "realtime_feedback": "enabled",
            "motivational_content": "enabled",
            "workout_companion": "enabled",
            "video_generation": "enabled",
            "ai_dashboard": "enabled"
        },
        "cache_status": f"{len(workout_generator.cache)} cached responses"
    }
    return health_status

# User input model (Now includes workout_location)
class UserInput(BaseModel):
    weight: float = Field(..., gt=0, le=500, description="Weight in kg")
    height: float = Field(..., gt=0, le=300, description="Height in cm")
    gender: int = Field(..., ge=0, le=2, description="Gender: 0=Female, 1=Male, 2=Other")
    age: int = Field(..., gt=0, le=120, description="Age in years")
    hypertension: str = Field(..., pattern="^(yes|no)$", description="Hypertension: yes or no")
    diabetes: str = Field(..., pattern="^(yes|no)$", description="Diabetes: yes or no")
    fitness_goal: str = Field(..., description="Fitness goal")
    workout_preference: str = Field(..., description="Workout preference")
    workout_location: str = Field(..., description="Workout location")
    duration: str = Field(..., description="Duration")
    experience_level: str = Field(..., description="Experience level")
    
# Define request model for user concerns
class UserConcernRequest(BaseModel):
    concern: str

# Progress tracking models
class WorkoutLog(BaseModel):
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    exercise: str
    sets: int
    reps: int
    weight: Optional[float] = None
    duration: Optional[int] = None  # in minutes
    notes: Optional[str] = None

class ProgressEntry(BaseModel):
    date: str
    weight: Optional[float] = None
    measurements: Optional[dict] = None  # e.g., {"chest": 40, "waist": 32}
    notes: Optional[str] = None

# Meal planning models
class MealPlanRequest(BaseModel):
    dietary_restrictions: Optional[List[str]] = None  # e.g., ["vegetarian", "gluten-free"]
    cuisine_preferences: Optional[List[str]] = None  # e.g., ["mediterranean", "asian"]
    meals_per_day: int = Field(default=3, ge=1, le=5)
    calories_per_day: Optional[int] = None

# AI Innovation models
class VoiceCommand(BaseModel):
    command: str
    audio_data: Optional[str] = None  # Base64 encoded audio

class ProgressPhoto(BaseModel):
    photo_data: str  # Base64 encoded image
    photo_type: str  # "before", "after", "progress"
    date: str

class MoodInput(BaseModel):
    mood: str  # happy, tired, motivated, etc.
    energy_level: int = Field(..., ge=1, le=10)
    stress_level: int = Field(..., ge=1, le=10)

class AICompanionMessage(BaseModel):
    message: str
    companion_personality: str = "motivational"  # motivational, strict, friendly, humorous

# Real-time workout feedback models
class WorkoutFeedback(BaseModel):
    exercise: str
    sets_completed: int
    reps_completed: int
    weight_used: Optional[float] = None
    perceived_difficulty: int = Field(..., ge=1, le=10)  # 1-10 scale
    form_quality: Optional[str] = None  # "good", "needs_work", "excellent"

class MotivationalContent(BaseModel):
    content_type: str = "quote"  # quote, story, challenge, affirmation
    theme: Optional[str] = None  # strength, consistency, recovery, etc.

# Advanced AI features
class VideoGenerationRequest(BaseModel):
    workout_type: str
    duration: int  # minutes
    intensity: str = "moderate"  # beginner, moderate, advanced
    equipment: Optional[List[str]] = None

class DashboardRequest(BaseModel):
    include_predictions: bool = True
    include_recommendations: bool = True
    time_range: str = "30_days"  # 7_days, 30_days, 90_days

@app.post("/generate-workout")
async def generate_workout(user_input: UserInput, session_id: str = Header(default=None)):
    """Process user input, use rule-based logic, and generate a GPT-based workout plan asynchronously."""

    try:
        logger.info(f"Received workout generation request for session: {session_id}")
        print("Received user input:", user_input.dict())

        # Generate new session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
            logger.info(f"New session created: {session_id}")

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

        logger.info(f"Successfully generated workout plan for session: {session_id}")
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
        logger.error(f"Error in /generate-workout for session {session_id}: {str(e)}")
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


# Progress tracking endpoints
@app.post("/progress/workout/{session_id}")
async def log_workout(session_id: str, workout_log: WorkoutLog):
    """Log a completed workout for progress tracking."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Initialize progress data if not exists
        if "progress" not in session_data:
            session_data["progress"] = {"workouts": [], "measurements": []}

        # Add workout log
        session_data["progress"]["workouts"].append(workout_log.dict())
        session_manager.create_session(session_id, session_data)

        return {"message": "Workout logged successfully", "session_id": session_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging workout: {str(e)}")

@app.post("/progress/measurement/{session_id}")
async def log_measurement(session_id: str, progress_entry: ProgressEntry):
    """Log body measurements and weight for progress tracking."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Initialize progress data if not exists
        if "progress" not in session_data:
            session_data["progress"] = {"workouts": [], "measurements": []}

        # Add measurement log
        session_data["progress"]["measurements"].append(progress_entry.dict())
        session_manager.create_session(session_id, session_data)

        return {"message": "Measurement logged successfully", "session_id": session_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging measurement: {str(e)}")

@app.get("/progress/{session_id}")
async def get_progress(session_id: str):
    """Get user's progress data."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        progress_data = session_data.get("progress", {"workouts": [], "measurements": []})
        return {
            "session_id": session_id,
            "progress": progress_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving progress: {str(e)}")

@app.post("/meal-plan/{session_id}")
async def generate_meal_plan(session_id: str, meal_request: MealPlanRequest):
    """Generate a detailed meal plan with recipes based on user preferences."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Generate meal plan prompt
        meal_plan_prompt = PromptTemplates.meal_plan_prompt(session_data, meal_request)
        
        # Get GPT response
        meal_plan = await workout_generator.generate_response_async(meal_plan_prompt)
        
        return {
            "session_id": session_id,
            "meal_plan": meal_plan
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating meal plan: {str(e)}")

@app.post("/admin/clear-cache")
async def clear_gpt_cache():
    """Clear the GPT response cache (admin endpoint)."""
    try:
        result = workout_generator.clear_cache()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")

# AI Innovation Endpoints

@app.post("/ai/voice-coach/{session_id}")
async def ai_voice_coach(session_id: str, voice_command: VoiceCommand):
    """AI-powered voice interaction for workout coaching."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Generate voice response prompt
        voice_prompt = PromptTemplates.voice_coach_prompt(voice_command.command, session_data)
        
        # Get AI response
        ai_response = await workout_generator.generate_response_async(voice_prompt)
        
        return {
            "session_id": session_id,
            "voice_command": voice_command.command,
            "ai_response": ai_response,
            "suggested_action": "continue_workout"  # Could be parsed from AI response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing voice command: {str(e)}")

@app.post("/ai/progress-photo/{session_id}")
async def analyze_progress_photo(session_id: str, progress_photo: ProgressPhoto):
    """AI analysis of progress photos for visual feedback."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Generate photo analysis prompt (simulated - in real implementation would use vision AI)
        photo_prompt = PromptTemplates.photo_analysis_prompt(progress_photo, session_data)
        
        # Get AI analysis
        analysis = await workout_generator.generate_response_async(photo_prompt)
        
        # Store photo data in session
        if "photos" not in session_data:
            session_data["photos"] = []
        session_data["photos"].append(progress_photo.dict())
        session_manager.create_session(session_id, session_data)

        return {
            "session_id": session_id,
            "photo_analysis": analysis,
            "photo_type": progress_photo.photo_type
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing photo: {str(e)}")

@app.post("/ai/mood-coaching/{session_id}")
async def ai_mood_based_coaching(session_id: str, mood_input: MoodInput):
    """AI coaching that adapts based on user's current mood and energy."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Generate mood-based coaching prompt
        mood_prompt = PromptTemplates.mood_coaching_prompt(mood_input, session_data)
        
        # Get personalized coaching
        coaching = await workout_generator.generate_response_async(mood_prompt)
        
        return {
            "session_id": session_id,
            "mood": mood_input.mood,
            "energy_level": mood_input.energy_level,
            "personalized_coaching": coaching
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating mood-based coaching: {str(e)}")

@app.post("/ai/companion-chat/{session_id}")
async def ai_companion_chat(session_id: str, companion_message: AICompanionMessage):
    """Conversational AI workout companion with personality."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Generate companion response prompt
        companion_prompt = PromptTemplates.ai_companion_prompt(
            companion_message.message, 
            companion_message.companion_personality, 
            session_data
        )
        
        # Get companion response
        response = await workout_generator.generate_response_async(companion_prompt)
        
        return {
            "session_id": session_id,
            "companion_personality": companion_message.companion_personality,
            "user_message": companion_message.message,
            "companion_response": response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with AI companion: {str(e)}")

@app.post("/ai/predict-performance/{session_id}")
async def predict_performance(session_id: str):
    """AI prediction of future performance based on current progress."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        progress_data = session_data.get("progress", {"workouts": [], "measurements": []})
        
        # Generate performance prediction prompt
        prediction_prompt = PromptTemplates.performance_prediction_prompt(session_data, progress_data)
        
        # Get AI prediction
        prediction = await workout_generator.generate_response_async(prediction_prompt)
        
        return {
            "session_id": session_id,
            "performance_prediction": prediction
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting performance: {str(e)}")

@app.post("/ai/smart-goals/{session_id}")
async def ai_smart_goals(session_id: str):
    """AI-powered dynamic goal setting and adjustment."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        progress_data = session_data.get("progress", {"workouts": [], "measurements": []})
        
        # Generate smart goals prompt
        goals_prompt = PromptTemplates.smart_goals_prompt(session_data, progress_data)
        
        # Get AI-generated goals
        goals = await workout_generator.generate_response_async(goals_prompt)
        
        return {
            "session_id": session_id,
            "smart_goals": goals
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating smart goals: {str(e)}")

@app.post("/ai/realtime-feedback/{session_id}")
async def ai_realtime_feedback(session_id: str, feedback: WorkoutFeedback):
    """AI-powered real-time workout feedback and form correction."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Generate real-time feedback prompt
        feedback_prompt = PromptTemplates.realtime_feedback_prompt(feedback, session_data)
        
        # Get AI feedback
        ai_feedback = await workout_generator.generate_response_async(feedback_prompt)
        
        return {
            "session_id": session_id,
            "exercise": feedback.exercise,
            "realtime_feedback": ai_feedback,
            "performance_score": feedback.perceived_difficulty  # Could be calculated by AI
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating real-time feedback: {str(e)}")

@app.post("/ai/motivational-content/{session_id}")
async def generate_motivational_content(session_id: str, content_request: MotivationalContent):
    """AI-generated personalized motivational content."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Generate motivational content prompt
        motivation_prompt = PromptTemplates.motivational_content_prompt(content_request, session_data)
        
        # Get AI-generated content
        content = await workout_generator.generate_response_async(motivation_prompt)
        
        return {
            "session_id": session_id,
            "content_type": content_request.content_type,
            "theme": content_request.theme,
            "motivational_content": content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating motivational content: {str(e)}")

@app.post("/ai/workout-companion/{session_id}")
async def ai_workout_companion(session_id: str, action: str = "start"):
    """AI workout companion that guides through entire workout sessions."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Generate workout companion prompt
        companion_prompt = PromptTemplates.workout_companion_prompt(action, session_data)
        
        # Get AI companion guidance
        guidance = await workout_generator.generate_response_async(companion_prompt)
        
        return {
            "session_id": session_id,
            "action": action,
            "companion_guidance": guidance
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with workout companion: {str(e)}")

@app.post("/ai/generate-workout-video/{session_id}")
async def generate_workout_video_idea(session_id: str, video_request: VideoGenerationRequest):
    """AI-generated workout video concepts and scripts."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Generate video concept prompt
        video_prompt = PromptTemplates.workout_video_prompt(video_request, session_data)
        
        # Get AI-generated video concept
        video_concept = await workout_generator.generate_response_async(video_prompt)
        
        return {
            "session_id": session_id,
            "workout_type": video_request.workout_type,
            "video_concept": video_concept
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating video concept: {str(e)}")

@app.post("/ai/dashboard/{session_id}")
async def ai_personal_dashboard(session_id: str, dashboard_request: DashboardRequest):
    """AI-powered comprehensive fitness dashboard with insights and predictions."""
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        progress_data = session_data.get("progress", {"workouts": [], "measurements": []})
        
        # Generate comprehensive dashboard prompt
        dashboard_prompt = PromptTemplates.dashboard_prompt(session_data, progress_data, dashboard_request)
        
        # Get AI dashboard summary
        dashboard = await workout_generator.generate_response_async(dashboard_prompt)
        
        return {
            "session_id": session_id,
            "time_range": dashboard_request.time_range,
            "ai_dashboard": dashboard
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating dashboard: {str(e)}")


class YouTubeSearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 5
    video_duration: Optional[str] = 'medium'
    relevance_keywords: Optional[List[str]] = None

@app.post("/youtube-search")
async def search_workout_videos(
    search_request: YouTubeSearchRequest,
    session_id: str = Header(default=None)
):
    """
    Search for workout videos on YouTube based on user preferences and session data.
    """
    try:
        # Initialize YouTube search
        youtube_search = YouTubeSearch()
        
        # If session exists, enhance search with user preferences
        if session_id:
            session_data = session_manager.get_session(session_id)
            if session_data:
                # Add relevant keywords based on user preferences
                relevance_keywords = [
                    session_data.get('fitness_goal', ''),
                    session_data.get('experience_level', ''),
                    session_data.get('workout_preference', '')
                ]
                # Filter out empty strings
                relevance_keywords = [kw for kw in relevance_keywords if kw]
                if relevance_keywords:
                    search_request.relevance_keywords = relevance_keywords

        # Perform search
        videos = await youtube_search.search_workout_videos(
            query=search_request.query,
            max_results=search_request.max_results,
            relevance_keywords=search_request.relevance_keywords,
            video_duration=search_request.video_duration
        )

        return {
            "session_id": session_id,
            "videos": videos
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching YouTube: {str(e)}")

@app.get("/youtube-video/{video_id}")
async def get_video_details(video_id: str):
    """
    Get detailed information about a specific YouTube video.
    """
    try:
        youtube_search = YouTubeSearch()
        video_details = await youtube_search.get_video_details(video_id)
        return video_details

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching video details: {str(e)}")

# Run the server
if __name__ == "__main__":
    import uvicorn
    # Add current directory to path for relative imports when running directly
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    uvicorn.run(app, host="0.0.0.0", port=8000)
