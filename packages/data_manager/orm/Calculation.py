from typing import List
from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from .Base import Base
from .Host import Host
from .Method import Method
from .BasisSet import BasisSet
from .MethodParameter import MethodParameter
from .System import System
from .Energy import Energy


class Calculation(Base):
    __tablename__ = "calculations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    output_path: Mapped[Optional[str]]
    project: Mapped[Optional[str]]

    host: Mapped[Optional["Host"]] = relationship()
    results: Mapped[List["Result"]] = relationship(back_populates="calculation")


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    calculation_id: Mapped[int] = mapped_column(ForeignKey("calculations.id"))
    method_id: Mapped[int] = mapped_column(ForeignKey("methods.id"))
    method_parameter_id: Mapped[int] = mapped_column(ForeignKey("method_parameters.id"))
    basis_set_id: Mapped[int] = mapped_column(ForeignKey("basis_sets.id"))
    system_id: Mapped[int] = mapped_column(ForeignKey("systems.id"))
    calculation_id: Mapped[int] = mapped_column(ForeignKey("calculations.id"))

    method: Mapped["Method"] = relationship()
    method_parameter: Mapped[Optional["MethodParameter"]] = relationship()
    basis_set: Mapped["BasisSet"] = relationship()
    system: Mapped["System"] = relationship()
    energies: Mapped[List["Energy"]] = relationship()
    calculation: Mapped["Calculation"] = relationship(back_populates="results")
