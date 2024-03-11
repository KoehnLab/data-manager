from typing import Type, Optional

import inspect

from sqlalchemy import select, distinct, and_, or_
from sqlalchemy.orm import Session

from data_manager.orm import Base


def get_property_class(object) -> Type:
    if not inspect.isclass(object):
        object = type(object)

    assert inspect.isclass(object)

    module = inspect.getmodule(object)
    assert module is not None

    property_cls = getattr(module, object.__name__ + "Property")

    assert property_cls is not None
    assert inspect.isclass(property_cls)

    return property_cls


def get_id_member(cls):
    members = [
        value
        for key, value in inspect.getmembers(cls)
        if "id" in key and not key.startswith("_")
    ]
    assert len(members) == 1
    return members[0]


def get_property_keys(session: Session, object):
    property_cls = get_property_class(object)

    query = select(distinct(property_cls.keyword))  # type: ignore

    if not inspect.isclass(object):
        query = query.where(get_id_member(property_cls) == object.id)  # type: ignore

    return session.scalars(query).all()


def get_property_values(session: Session, object, key: Optional[str] = None):
    property_cls = get_property_class(object)

    query = select(distinct(property_cls.value))  # type: ignore

    if not inspect.isclass(object):
        query = query.where(get_id_member(property_cls) == object.id)  # type: ignore

    if key is not None:
        query = query.where(property_cls.keyword == key)  # type: ignore

    return session.scalars(query).all()


def has_properties(object, require_all=True, **properties):
    property_cls = get_property_class(object)

    join_condition = and_ if require_all else or_

    conditions = [
        object.properties.any(
            and_(property_cls.keyword == key, property_cls.value == str(value)) # type: ignore
        )
        for key, value in properties.items()
    ]

    return join_condition(*conditions)
