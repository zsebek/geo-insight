from fastapi import APIRouter, HTTPException
from config.keys import J_COOKIE
from services.auth.login import login

router = APIRouter()

@router.get("/login")
def get_session():
    response = login(J_COOKIE)
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid NCFA Cookie")
    
    return {"message": "Authenticated successfully"}
