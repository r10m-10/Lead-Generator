from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session
import json
from starlette.concurrency import run_in_threadpool
from ..database import get_db
from ..models.lead import Lead
from ..schemas.lead import LeadsRequest, LeadReinstate
from ..auth_utils import get_current_user
from scraper.scraper import scraper
from ..dependencies import get_browser
from ..utils import make_changes

lead_router = APIRouter()

@lead_router.get("/leads")
def get_leads(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    team_id = current_user.team_id

    query = select(Lead).where(Lead.team_id == team_id)
    leads = db.execute(query).scalars().all()

    return {"success": True, "leads": leads}

@lead_router.post("/leads/generate")
async def generate_leads(payload: LeadsRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db), browser = Depends(get_browser)):
    team_id = current_user.team_id

    if current_user.role != "boss":
        raise HTTPException(status_code=401, detail="Need to be the manager to generate leads for this team")

    scraped = await scraper(browser, payload.query, payload.n_leads)

    if scraped["error"]:
        raise HTTPException(status_code=400, detail=scraped["error"])

    for i in scraped["leads"]:
        query = select(Lead).where(and_(Lead.phone_number == i["phone_number"], Lead.team_id == team_id))
        lead = await run_in_threadpool(
            lambda: db.execute(query).scalar_one_or_none()
            )

        if lead is not None:
            if lead.name != i["name"] and lead.website != i["website"]:
                lead.flag = 0
                lead.changes = json.dumps({"name": i["name"], "website": i["website"]})
            elif lead.name != i["name"]:
                lead.flag = 1
                lead.changes = json.dumps({"name": i["name"]})
            elif lead.website != i["website"]:
                lead.flag = 2
                lead.changes = json.dumps({"website": i["website"]})
            else:
                lead.flag = 3
        else:
            new_lead = Lead(team_id= team_id,
                            name= i["name"],
                            phone_number= i["phone_number"],
                            website= i["website"],
                            rating= i["rating"])
            db.add(new_lead)
    await run_in_threadpool(db.commit)

    return {"success": True}

@lead_router.patch("/leads/reinstate")
def reinstate(payload: LeadReinstate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    team_id = current_user.team_id

    if payload.flag is not None:
        query = select(Lead).where(Lead.flag == payload.flag, Lead.team_id == team_id)
        lead = db.execute(query).scalars().all()

        for i in lead:
            i.flag = None
            make_changes(i)
    elif payload.lead_id is not None:
        query = select(Lead).where(Lead.id == payload.lead_id, Lead.team_id == team_id)
        lead = db.execute(query).scalar_one_or_none()

        if lead is None:
            raise HTTPException(status_code=400, detail="Could not find lead")

        lead.flag = None
        make_changes(lead)
    else:
        query = select(Lead).where(Lead.flag.isnot(None), Lead.team_id == team_id)
        lead = db.execute(query).scalars().all()

        for i in lead:
            i.flag = None
            make_changes(i)
    db.commit()

    return {"success": True}