import requests
from config.keys import user_cookies
import logging

class SessionManager:
    """Manages a singleton requests session with per-user authentication."""
    _session = None
    _user = None
    
    @classmethod
    def get_session(cls):
        """Returns the existing session or creates a new one for the active user."""
        if cls._session is None or cls._user is None:
            active_user = cls.get_active_user()
            cls._session = cls._authenticate_user(active_user)
        return cls._session

    @classmethod
    def set_session(cls, session):
        """Stores the authenticated session."""
        cls._session = session

    @classmethod
    def get_users(cls):
        return list(user_cookies.keys())

    @classmethod
    def set_active_user(cls, user: str):
        """Sets the active user and refreshes session if needed."""
        if user not in user_cookies:
            return
        
        if cls._user != user:
            cls._user = user
            cls._session = cls._authenticate_user(user)  # Refresh session when user changes

    @classmethod
    def get_active_user(cls):
        """Returns the active user, defaulting to 'Zach' if none is set."""
        if cls._user is None:
            cls._user = "Zach"
        return cls._user

    @classmethod
    def _authenticate_user(cls, user: str):
        """Creates a session and logs in the user."""
        session = requests.Session()
        ncfa_token = user_cookies.get(user)

        if not ncfa_token:
            logging.error(f"❌ No authentication token found for user: {user}")
            return session  # Return empty session
        
        session.cookies.set("_ncfa", ncfa_token, domain="www.geoguessr.com")
        response = session.get("https://www.geoguessr.com/api/v4/notifications")

        if response.ok:
            logging.info(f"✅ Successfully authenticated session for user: {user}")
        else:
            logging.error(f"❌ Authentication failed for {user}. Status: {response.status_code}")
        
        return session
