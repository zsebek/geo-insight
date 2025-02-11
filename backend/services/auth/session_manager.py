import requests
from config.keys import user_cookies
import logging

class SessionManager:
    """Manages a singleton requests session."""
    _session = None
    _user = None
    
    @classmethod
    def get_session(cls):
        """Returns the existing session or creates a new one."""
        if cls._session is None:
            cls._session = requests.Session()
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
        cls._user = user
    
    @classmethod
    def get_active_user(cls):
        if cls._user is None:
            cls._user = "Zach"
        return cls._user