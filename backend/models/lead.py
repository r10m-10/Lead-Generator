from sqlalchemy import DateTime, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from typing import Optional
from .base import Base

class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    name: Mapped[str] = mapped_column(String(225))
    phone_number: Mapped[Optional[str]] = mapped_column(String(225), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(225), nullable=True)
    rating: Mapped[Optional[str]] = mapped_column(String(225), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("team_id", "phone_number", name="uq_team_phone"),
    )