from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import UserCreate, UserLogin
from ..models.team import Team
from ..models.user import User
from ..security import hash_password, verify_password
from ..auth_utils import create_access_token, get_current_user

auth_router = APIRouter()

@auth_router.post("/users")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):

    query = select(User).where(or_(User.email == payload.email, User.username == payload.username))
    existing_user = db.execute(query).scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    if payload.team_name is not None:
        new_team = Team(team_name= payload.team_name)
    else:
        new_team = Team(team_name= f"{payload.username}'s Team")
    db.add(new_team)
    db.flush()

    hashed_password = hash_password(payload.password)

    new_user = User(full_name= payload.full_name,
                    username= payload.username,
                    email= payload.email,
                    hashed_password= hashed_password,
                    role= "boss",
                    team_id= new_team.id,
                    solo_team_id= new_team.id)
    db.add(new_user)
    db.commit()

    token = create_access_token(new_user.id)

    return {"success": True, 
            "team_name": new_team.team_name, 
            "username": new_user.username, 
            "access_token": token, 
            "token_type": "bearer"}

@auth_router.get("/users/check-username")
def check_username(username: str, db: Session = Depends(get_db)):
    query = select(User).where(User.username == username)
    username_taken = db.execute(query).scalar_one_or_none()

    if username_taken is not None:
        raise HTTPException(status_code=400, detail="username taken")

    return {"available": True}

@auth_router.get("/users/check-email")
def check_email(email: str, db: Session = Depends(get_db)):
    query = select(User).where(User.email == email)
    email_taken = db.execute(query).scalar_one_or_none()

    if email_taken is not None:
        raise HTTPException(status_code=400, detail="email taken")

    return {"available": True}

@auth_router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    query = select(User).where(User.email == payload.email)
    found_user = db.execute(query).scalar_one_or_none()

    if found_user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if verify_password(payload.password, found_user.hashed_password) == False:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    query = select(Team).where(Team.id == found_user.team_id)
    team = db.execute(query).scalar_one_or_none()

    token = create_access_token(found_user.id)

    return {"success": True, 
            "team_name": team.team_name, 
            "username": found_user.username,
            "access_token": token, 
            "token_type": "bearer"}

@auth_router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return {"username": current_user.username}