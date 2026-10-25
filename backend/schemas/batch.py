from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeadlineRequest(BaseModel):
    deadline: Optional[datetime]