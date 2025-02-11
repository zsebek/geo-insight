from fastapi import APIRouter, HTTPException
import requests
from config import BASE_URL_V4

router = APIRouter()

@router.get("/session")
def get_session(ncfa: str):
    """Creates an authenticated session using the provided NCFA cookie."""
    session = requests.Session()
    session.cookies.set("_ncfa", ncfa, domain="www.geoguessr.com")
    
    # Test authentication
    response = session.get(f"{BASE_URL_V4}/user")
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid NCFA Cookie")
    
    return {"message": "Authenticated successfully"}
