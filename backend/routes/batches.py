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

@batch_router.patch("/batches/{batch_id}/publish")
def publish_batch(batch_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    if current_user.role != "boss":
        raise HTTPException(status_code=403, detail="Need to be the manager to publish batch")

    query = select(LeadBatch).where(LeadBatch.id == batch_id, LeadBatch.team_id == current_user.team_id)
    batch = db.execute(query).scalar_one_or_none()

    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")

    batch.published = True

    db.commit()

    return {"success": True}

@batch_router.delete("/batches/{batch_id}/delete")
def delete_batch(batch_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    if current_user.role != "boss":
        raise HTTPException(status_code=403, detail="Need to be the manager to delete batch")

    query = select(LeadBatch).where(LeadBatch.id == batch_id, LeadBatch.team_id == current_user.team_id)
    batch = db.execute(query).scalar_one_or_none()

    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")

    lead_ids = select(Lead.id).where(Lead.batch_id == batch_id, Lead.team_id == current_user.team_id)

    db.execute(delete(CallRecord).where(CallRecord.lead_id.in_(lead_ids)))
    db.execute(delete(Lead).where(Lead.batch_id == batch_id, Lead.team_id == current_user.team_id))
    db.execute(delete(LeadBatch).where(LeadBatch.id == batch_id, LeadBatch.team_id == current_user.team_id))

    db.commit()

    return {"success": True}