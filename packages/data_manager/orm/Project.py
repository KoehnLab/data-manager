from .Base import Base

from typing import Optional, Set

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, Integer, ForeignKey


project_author_association = Table(
    "project_author_association",
    Base.metadata,
    Column(
        "project_id",
        Integer,
        ForeignKey("projects.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "author_id",
        Integer,
        ForeignKey("authors.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]

    authors: Mapped[Set["Author"]] = relationship(
        secondary=project_author_association,
        back_populates="projects",
        passive_deletes=True,
    )

    processing_steps: Mapped[Set["ProcessingStep"]] = relationship(  # type: ignore
        back_populates="project", passive_deletes=True
    )


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    affiliation: Mapped[Optional[str]]

    projects: Mapped[Set[Project]] = relationship(
        secondary=project_author_association,
        back_populates="authors",
        passive_deletes=True,
    )
