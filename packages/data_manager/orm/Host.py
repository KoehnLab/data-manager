from typing import Optional

from .Base import Base

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Host(Base):
    __tablename__ = "hosts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    cpu: Mapped[Optional[str]]
    cluster: Mapped[Optional[str]]
