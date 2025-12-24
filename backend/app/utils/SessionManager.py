class SessionManager:
    """Handles user session storage."""
    def __init__(self):
        self.sessions = {}  # Store user data (keyed by session_id)

    def create_session(self, session_id, user_data):
        """Create or update a session."""
        self.sessions[session_id] = user_data

    def get_session(self, session_id):
        """Retrieve session data if exists."""
        return self.sessions.get(session_id, None)

    def delete_session(self, session_id):
        """Clear session data (new user starts fresh)."""
        if session_id in self.sessions:
            del self.sessions[session_id]

