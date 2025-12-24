#!/usr/bin/env python3
"""
Entry point for the AI Fitness Coach API.
This script runs the FastAPI application directly.
"""

import uvicorn
import sys
import os

if __name__ == "__main__":
    # Add the app directory to Python path so we can import from it
    app_dir = os.path.join(os.path.dirname(__file__), "app")
    sys.path.insert(0, app_dir)

    # Import the app
    from main import app

    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)