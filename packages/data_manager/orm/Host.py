from .Base import Base

from typing import Dict

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict
from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy


class Host(Base):
    __tablename__ = "hosts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    date: Mapped[datetime] = mapped_column(server_default=func.now())

    _properties: Mapped[Dict[str, "HostProperty"]] = relationship(
        collection_class=attribute_keyed_dict("keyword"), passive_deletes=True
    )

    properties: AssociationProxy[Dict[str, str]] = association_proxy(
        target_collection="_properties",
        attr="value",
        creator=lambda k, v: HostProperty(keyword=k, value=v),
    )


class HostProperty(Base):
    __tablename__ = "host_properties"

    host_id: Mapped[int] = mapped_column(
        ForeignKey(Host.id, onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    keyword: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]
