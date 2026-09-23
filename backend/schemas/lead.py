from pydantic import BaseModel, model_validator
from typing import Optional

class LeadsRequest(BaseModel):
    query: str
    n_leads: int

class LeadReinstate(BaseModel):
    lead_id: Optional[int] = None
    flag: Optional[int] = None

    @model_validator(mode= "after")
    def validate_inputs(self):
        if self.lead_id is not None and self.flag is not None:
            raise ValueError("Provide either lead_id or flag, not both")
        return self