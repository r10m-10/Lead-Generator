from pydantic import BaseModel, model_validator, Field, ConfigDict
from datetime import datetime
from typing import Optional, List

class QueryBatch(BaseModel):
    query: str
    n_leads: int

class LeadsRequest(BaseModel):
    batches: List[QueryBatch]

class LeadReinstate(BaseModel):
    lead_id: Optional[int] = None
    flag: Optional[int] = None

    @model_validator(mode= "after")
    def validate_inputs(self):
        if self.lead_id is not None and self.flag is not None:
            raise ValueError("Provide either lead_id or flag, not both")
        return self

class LeadLog(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    log: str = Field(min_length=3, max_length=1000)