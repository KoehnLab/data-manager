from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .Base import Base

class Energy(Base):
    __tablename__ = "energies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    energy: Mapped[float]
    state: Mapped[Optional[str]]
    result_id: Mapped[int] = mapped_column(ForeignKey("results.id"))
