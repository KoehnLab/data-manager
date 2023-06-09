from typing import List
from typing import Optional

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import UniqueConstraint
from sqlalchemy import SQLColumnExpression
from sqlalchemy import func
from sqlalchemy import select


class Base(DeclarativeBase):
    pass


class BasisSet(Base):
    __tablename__ = "basis_sets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)


class Host(Base):
    __tablename__ = "hosts"

    __table_args__ = (UniqueConstraint("name", "cpu", "cluster"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    cpu: Mapped[Optional[str]]
    cluster: Mapped[Optional[str]]


class Method(Base):
    __tablename__ = "methods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)


class MethodParameter(Base):
    __tablename__ = "method_parameters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symmetry: Mapped[str]
    density_fitting: Mapped[bool]
    active_orbitals: Mapped[Optional[int]]
    active_electrons: Mapped[Optional[int]]
    additional: Mapped[Optional[str]]


class System(Base):
    __tablename__ = "systems"
    __table_args__ = (UniqueConstraint("name", "charge", "multiplicity"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    charge: Mapped[int]
    multiplicity: Mapped[int]


author_project_association = Table(
    "author_project_associations",
    Base.metadata,
    Column(
        "author_id",
        ForeignKey("authors.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "project_id",
        primary_key=True,
    ),
    Column(
        "project_name",
        primary_key=True,
    ),
    ForeignKeyConstraint(
        ["project_id", "project_name"], ["projects.id", "projects.name"]
    ),
)


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)

    projects: Mapped[List["Project"]] = relationship(
        back_populates="authors", secondary=author_project_association
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(primary_key=True)

    authors: Mapped[List[Author]] = relationship(
        back_populates="projects", secondary=author_project_association
    )
    calculations: Mapped[List["Calculation"]] = relationship(back_populates="project")

    @hybrid_property
    def author_count(self) -> int:
        return len(self.authors)

    @author_count.inplace.expression
    @classmethod
    def _author_count_expression(cls) -> SQLColumnExpression[int]:
        return (
            select(func.count())
            .select_from(author_project_association)
            .where(author_project_association.c.project_id == cls.id)
            .label("author_count")
        )


class Calculation(Base):
    __tablename__ = "calculations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    output_path: Mapped[Optional[str]]
    host_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(Host.id, onupdate="CASCADE", ondelete="CASCADE")
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey(Project.id, onupdate="CASCADE", ondelete="CASCADE")
    )

    host: Mapped[Optional["Host"]] = relationship()
    results: Mapped[List["Result"]] = relationship(back_populates="calculation")
    project: Mapped[Project] = relationship(back_populates="calculations")


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    calculation_id: Mapped[int] = mapped_column(
        ForeignKey(Calculation.id, onupdate="CASCADE", ondelete="CASCADE")
    )
    method_id: Mapped[int] = mapped_column(
        ForeignKey(Method.id, onupdate="CASCADE", ondelete="CASCADE")
    )
    method_parameter_id: Mapped[int] = mapped_column(
        ForeignKey(MethodParameter.id, onupdate="CASCADE", ondelete="CASCADE")
    )
    basis_set_id: Mapped[int] = mapped_column(
        ForeignKey(BasisSet.id, onupdate="CASCADE", ondelete="CASCADE")
    )
    system_id: Mapped[int] = mapped_column(
        ForeignKey(System.id, onupdate="CASCADE", ondelete="CASCADE")
    )

    method: Mapped["Method"] = relationship()
    method_parameter: Mapped[Optional["MethodParameter"]] = relationship()
    basis_set: Mapped["BasisSet"] = relationship()
    system: Mapped["System"] = relationship()
    energies: Mapped[List["Energy"]] = relationship(back_populates="result")
    calculation: Mapped["Calculation"] = relationship(back_populates="results")


class Energy(Base):
    __tablename__ = "energies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[float]
    state: Mapped[Optional[str]]
    result_id: Mapped[int] = mapped_column(
        ForeignKey(Result.id, onupdate="CASCADE", ondelete="CASCADE")
    )

    result: Mapped[Result] = relationship(back_populates="energies")
