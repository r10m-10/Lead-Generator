from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.signup import Signup
from ..models.team import Team
from ..models.user import User
from ..security import pwd_context

auth_router = APIRouter()

@auth_router.post("/signup")
def signup(payload: Signup, db: Session = Depends(get_db)):

    if payload.team_name is not None:
        new_team = Team(name= payload.team_name)
    else:
        new_team = Team(name= f"{payload.username}'s Team")
    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    hashed_password = pwd_context.hash(payload.password)

    new_user = User(full_name= payload.full_name,
                    username= payload.username,
                    email= payload.email,
                    hashed_password= hashed_password,
                    role= "boss",
                    team_id= new_team.id,
                    solo_team_id= new_team.id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)