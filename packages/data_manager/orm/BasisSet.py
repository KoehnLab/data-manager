from .Base import Base

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class BasisSet(Base):
    __tablename__ = "basis_sets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
