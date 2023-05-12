from typing import Optional, Dict

from .Base import Base

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey

class MethodParameter(Base):
    __tablename__ = "method_parameters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    density_fitting: Mapped[Optional[bool]]
    active_orbtials: Mapped[Optional[int]]
    active_electrons: Mapped[Optional[int]]
    additional: Mapped[Optional[str]]
