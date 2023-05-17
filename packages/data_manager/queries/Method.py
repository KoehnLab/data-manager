from data_manager.orm import Method

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import exists


def methodExists(session: Session, name: str) -> bool:
    return session.query(exists(Method).where(Method.name == name)).scalar()


def getMethod(session: Session, name: str) -> Method:
    method = session.scalars(select(Method).where(Method.name == name)).first()

    if method is None:
        method = Method(name=name)

    return method
