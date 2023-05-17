from data_manager.orm import BasisSet

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import exists


def basisSetExists(session: Session, name: str) -> bool:
    return session.query(exists(BasisSet).where(BasisSet.name == name)).scalar()


def getBasisSet(session: Session, name: str) -> BasisSet:
    basisSet = session.scalars(select(BasisSet).where(BasisSet.name == name)).first()

    if basisSet is None:
        basisSet = BasisSet(name=name)

    return basisSet
