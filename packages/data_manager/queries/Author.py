from data_manager.orm import Author

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import exists


def authorExists(session: Session, name: str) -> bool:
    return session.query(exists(Author).where(Author.name == name)).scalar()


def getAuthor(session: Session, name: str) -> Author:
    author = session.scalars(select(Author).where(Author.name == name)).first()

    if author is None:
        author = Author(name=name)

    return author
