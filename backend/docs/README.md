# AI Fitness Coach Backend

A revolutionary AI-powered fitness coaching backend featuring voice-powered workout coaching, AI companion chat, mood-adaptive training, and comprehensive fitness analytics.

## Project Structure

```
backend/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI application
│   ├── models/                   # Data models and business logic
│   │   ├── __init__.py
│   │   ├── RuleBasedRecommender.py
│   │   └── youtube_search.py
│   ├── nlp/                      # Natural language processing components
│   │   ├── __init__.py
│   │   ├── GPTClient.py
│   │   ├── GPTWorkoutGenerator.py
│   │   └── PromptTemplates.py
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── SessionManager.py
├── docs/                         # Documentation
├── api-doc/                      # API documentation
│   └── AI_Fitness_Coach_API.postman_collection.json
├── .env                          # Environment variables (create from .env.example)
├── .env.example                  # Environment variables template
├── requirements.txt              # Python dependencies
├── run.py                        # Application entry point
└── README.md                     # This file
```

## Features

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

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fitness-coach/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   python app/main.py
   ```

   Or use the alternative entry point:
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:8000`

## API Documentation

- **Postman Collection**: Import `api-doc/AI_Fitness_Coach_API.postman_collection.json`
- **Interactive API Docs**: Visit `http://localhost:8000/docs` when running
- **Health Check**: `GET /health`

## Environment Variables

Required environment variables (see `.env.example` for details):

- `OPENAI_API_KEY`: OpenAI API key for AI features
- `YOUTUBE_API_KEY`: YouTube Data API key for video search

## Development

- **Code Style**: Follow PEP 8
- **Testing**: Add tests in appropriate test directories
- **Security**: All code is scanned with Snyk for vulnerabilities

## Contributing

1. Create a feature branch
2. Make your changes
3. Run security scans
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]