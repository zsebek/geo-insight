import requests
from config.api_urls import BASE_URL_V4
from config.keys import J_COOKIE

def login(ncfa: str) -> requests.Response:
    """Creates an authenticated session using the provided NCFA cookie."""
    session = requests.Session()
    session.cookies.set("_ncfa", ncfa, domain="www.geoguessr.com")
    
    # Test authentication by getting notification list
    return session.get(f"{BASE_URL_V4}/notifications")

if __name__=="__main__":
    login(J_COOKIE)