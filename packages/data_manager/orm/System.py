from .Base import Base


from typing import Optional, Dict

from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict
from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy


class System(Base):
    __tablename__ = "systems"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    variant: Mapped[Optional[str]]
    _properties: Mapped[Dict[str, "SystemProperty"]] = relationship(
        collection_class=attribute_keyed_dict("name"), passive_deletes=True
    )

    properties: AssociationProxy[Dict[str, str]] = association_proxy(
        target_collection="_properties",
        attr="value",
        creator=lambda k, v: SystemProperty(name=k, value=v),
    )


class SystemProperty(Base):
    __tablename__ = "system_properties"

    system_id: Mapped[int] = mapped_column(
        ForeignKey(System.id, onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    name: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]
