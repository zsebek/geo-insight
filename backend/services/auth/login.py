from requests import Response
from config.api_urls import BASE_URL_V4
from services.auth.session_manager import SessionManager

def login(ncfa: str) -> Response:
    """Creates and stores an authenticated session using the NCFA cookie."""
    session = SessionManager.get_session()
    session.cookies.set("_ncfa", ncfa, domain="www.geoguessr.com")

    # Verify authentication by fetching notifications
    response = session.get(f"{BASE_URL_V4}/notifications")
    
    if response.ok:
        SessionManager.set_session(session)  # Store session globally
    return response

if __name__ == "__main__":
    login("2vpPRmpWvQndQOwGc64acDkM0ZeGE5LQnwaRdqJ11%2Bc%3DPmea5NC7KbJh2tv3vaWyo8uc4HQfJyHKyLyzSdep%2BtvkLTa2ak7d8%2F3XrIkvKzKK6B79dO9xH4IvVc6PTsCsf15uyIjSC88aZueMvpN2N4o%3D")