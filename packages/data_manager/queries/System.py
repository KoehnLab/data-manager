from data_manager.orm import System

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import exists


def systemExists(session: Session, name: str, charge: int, multiplicity: int) -> bool:
    return session.query(
        exists(System)
        .where(System.name == name)
        .where(System.charge == charge)
        .where(System.multiplicity == multiplicity)
    ).scalar()


def getSystem(session: Session, name: str, charge: int, multiplicity: int) -> System:
    system = session.scalars(
        select(System)
        .where(System.name == name)
        .where(System.charge == charge)
        .where(System.multiplicity == multiplicity)
    ).first()

    if system is None:
        system = System(name=name, charge=charge, multiplicity=multiplicity)

    return system
