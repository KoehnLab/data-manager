from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


from .Base import Base


class Method(Base):
    __tablename__ = "methods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
