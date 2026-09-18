from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.team import Team
from ..models.user import User
from ..models.lead import Lead
from ..security import hash_password, verify_password
from ..auth_utils import create_access_token, get_current_user

lead_router = APIRouter()

@lead_router.get("/leads")
def get_leads(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    team_id = current_user.team_id

    query = select(Lead).where(Lead.team_id == team_id)
    leads = db.execute(query).scalars().all()

    return {"success": True, "leads": leads}