from fastapi import APIRouter, HTTPException, Depends
from config.keys import user_cookies
from services.auth.login import login
from services.auth.session_manager import SessionManager

router = APIRouter()

@router.get("/login")
def get_session(user_name: str):
    """Authenticates and stores session."""
    if user_name not in user_cookies:
        return HTTPException(status_code=401, detail="User not recognized")
    return {"data": login(user_cookies.get(user_name))}

@router.get("/session")
def get_stored_session():
    """Returns session status."""
    return {"data": SessionManager.get_session()}


@router.get("/users")
def get_auth_users():
    return {"data": SessionManager.get_users()}



@router.post("/active_user")
def set_active_user(user_name: str):
    return {"data": SessionManager.set_active_user(user_name)}

@router.get("/active_user")
def get_active_user():
    return {"data": SessionManager.get_active_user()}


# if __name__=="__main__":
#     from utils.http import get
#     get("auth/login", {"user_name": "zach"})