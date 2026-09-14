from fastapi import APIRouter, Depends
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import UserCreate
from ..models.team import Team
from ..models.user import User
from ..security import hash_password

auth_router = APIRouter()

@auth_router.post("/users")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):

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
    db.refresh(new_team)
    db.refresh(new_user)