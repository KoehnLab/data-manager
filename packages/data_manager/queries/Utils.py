from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import not_
from sqlalchemy import exists
from sqlalchemy import func


def nextFreeID(session: Session, table) -> int:
    lastID = session.scalars(
        func.coalesce(
            select(table.id).where(not_(exists(table.id + 1))).scalar_subquery(), 0
        )
    ).first()

    assert lastID != None

    return lastID + 1
