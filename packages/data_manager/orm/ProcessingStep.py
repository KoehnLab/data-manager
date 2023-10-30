from .Base import Base
from .Host import Host
from .Result import Result
from .System import System
from .Project import Project

from typing import Optional, Set, List, Dict

from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict
from sqlalchemy import ForeignKey, Table, Column, Integer, CheckConstraint
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy

step_hierarchy = Table(
    "processing_step_hierarchy",
    Base.metadata,
    Column(
        "preceding_step_id",
        Integer,
        ForeignKey("processing_steps.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "dependent_step_id",
        Integer,
        ForeignKey("processing_steps.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    CheckConstraint(
        "preceding_step_id != dependent_step_id", name="check_no_self_dependence"
    ),
)

keyword_step_association = Table(
    "keyword_processing_step_association",
    Base.metadata,
    Column(
        "processing_step_id",
        Integer,
        ForeignKey("processing_steps.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "keyword_id",
        Integer,
        ForeignKey("keywords.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class ProcessingStep(Base):
    __tablename__ = "processing_steps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kind: Mapped[str]
    host_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(Host.id, onupdate="CASCADE", ondelete="CASCADE")
    )
    system_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(System.id, onupdate="CASCADE", ondelete="CASCADE")
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey(Project.id, ondelete="CASCADE", onupdate="CASCADE")
    )
    output_path: Mapped[Optional[str]]

    host: Mapped[Optional[Host]] = relationship(passive_deletes=True)
    system: Mapped[Optional[System]] = relationship(passive_deletes=True)
    project: Mapped[Project] = relationship(
        back_populates="processing_steps", passive_deletes=True
    )

    results: Mapped[List[Result]] = relationship(
        back_populates="processing_step", passive_deletes=True
    )

    dependent_steps: Mapped[Set["ProcessingStep"]] = relationship(
        secondary=step_hierarchy,
        primaryjoin=id == step_hierarchy.c.preceding_step_id,
        secondaryjoin=id == step_hierarchy.c.dependent_step_id,
        back_populates="preceding_steps",
        passive_deletes=True,
    )
    preceding_steps: Mapped[Set["ProcessingStep"]] = relationship(
        secondary=step_hierarchy,
        primaryjoin=id == step_hierarchy.c.dependent_step_id,
        secondaryjoin=id == step_hierarchy.c.preceding_step_id,
        back_populates="dependent_steps",
        passive_deletes=True,
    )

    _properties: Mapped[Dict[str, "ProcessingStepProperty"]] = relationship(
        collection_class=attribute_keyed_dict("keyword"), passive_deletes=True
    )

    properties: AssociationProxy[Dict[str, str]] = association_proxy(
        target_collection="_properties",
        attr="value",
        creator=lambda k, v: ProcessingStepProperty(keyword=k, value=v),
    )

    keywords: Mapped[Set["Keyword"]] = relationship(
        secondary=keyword_step_association,
        passive_deletes=True,
        back_populates="processing_steps",
    )


class ProcessingStepProperty(Base):
    __tablename__ = "processing_step_properties"

    step_id: Mapped[int] = mapped_column(
        ForeignKey(ProcessingStep.id, onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    keyword: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]


class Keyword(Base):
    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    processing_steps: Mapped[List["ProcessingStep"]] = relationship(
        secondary=keyword_step_association,
        passive_deletes=True,
        back_populates="keywords",
    )
