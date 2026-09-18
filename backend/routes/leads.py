from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.lead import Lead
from ..schemas.lead import LeadsRequest, Leads
from ..auth_utils import get_current_user
from ...scraper.scraper import scraper

lead_router = APIRouter()

@lead_router.get("/leads")
def get_leads(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    team_id = current_user.team_id

    query = select(Lead).where(Lead.team_id == team_id)
    leads = db.execute(query).scalars().all()

    return {"success": True, "leads": leads}

@lead_router.post("/leads/generate-leads")
def generate_leads(payload: LeadsRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    team_id = current_user.team_id

    if current_user.role != "boss":
        raise HTTPException(status_code=401, detail="Need to be the manager to generate leads for this team")

    scraped = scraper(payload.query, payload.n_leads)

    if scraped["error"]:
        raise HTTPException(status_code=400, detail=scraped["error"])

    for i in scraped["leads"]:
        query = select(Lead.name, Lead.phone_number, Lead.website, Lead.rating).where(and_(Lead.phone_number == i["phno"], Lead.team_id == team_id))
        lead = db.execute(query).scalar_one_or_none()

        i = Leads.model_validate(i)

        if lead is not None:
            if i == lead:
                continue