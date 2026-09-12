from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from .base import Base

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))