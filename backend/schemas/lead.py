from pydantic import BaseModel
from typing import Optional

class LeadsRequest(BaseModel):
    query: str
    n_leads: int

class Leads(BaseModel):
    name: str
    phone_number: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[str] = None