from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, exists, delete
from sqlalchemy.orm import Session
import json
from datetime import datetime, timezone
from starlette.concurrency import run_in_threadpool
from ..database import get_db
from ..models.lead import Lead
from ..models.lead_batch import LeadBatch
from ..models.call_record import CallRecord
from ..schemas.lead import LeadsRequest, LeadReinstate, LeadLog
from ..auth_utils import get_current_user
from scraper.scraper import scraper
from ..dependencies import get_browser
from ..utils import make_changes
import time

batch_router = APIRouter()

@batch_router.get("/batches")
def get_batches(current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    if current_user.role != "boss":
        raise HTTPException(status_code=403, detail="Need to be the manager to view batches")

    query = select(LeadBatch).where(LeadBatch.team_id == current_user.team_id)
    batches = db.execute(query).scalars().all()

    return {"success": True, "batches": batches}