from pydantic import BaseModel
from typing import Optional
from datetime import date

class DeadlineRequest(BaseModel):
    deadline: Optional[date]