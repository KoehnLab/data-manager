from typing import Optional

from .Base import Base

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class System(Base):
    __tablename__ = "systems"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    charge: Mapped[int]
    multiplicity: Mapped[int]
    used_symmetry: Mapped[str]
