from pydantic import BaseModel
from typing import Optional

class LeadsRequest(BaseModel):
    query: str
    n_leads: int