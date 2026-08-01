from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)
class Release(Base):
    __tablename__="releases"
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    service: Mapped[str]=mapped_column(String(80),index=True)
    version: Mapped[str]=mapped_column(String(40))
    environment: Mapped[str]=mapped_column(String(20),index=True)
    status: Mapped[str]=mapped_column(String(20))
    strategy: Mapped[str]=mapped_column(String(30),default="rolling")
    commit_sha: Mapped[str]=mapped_column(String(12))
    created_at: Mapped[datetime]=mapped_column(DateTime,default=utc_now)
