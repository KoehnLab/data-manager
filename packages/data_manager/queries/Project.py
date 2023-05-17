from typing import Optional, List
from data_manager.orm import Project, Author

from sqlalchemy.orm import Session
from sqlalchemy.orm import outerjoin
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import any_

from .Utils import nextFreeID


def countProjects(session: Session, name: str, authors: Optional[List[str]]) -> int:
    if authors is None:
        authors = []

    count = session.scalars(
        select(func.count())
        .select_from(Project)
        .where(Project.name == name)
        .where(
            *[Project.authors.contains(Author.name == current) for current in authors]
        )
    ).first()

    assert count != None

    return count


def projectExists(session: Session, name: str, authors: Optional[List[str]]) -> bool:
    return countProjects(session=session, name=name, authors=authors) > 0


def getProject(
    session: Session,
    name: str,
    authors: List[str],
) -> Project:
    # First ensure that all authors exist
    authorObjects: List[Author] = []
    for currentAuthorName in authors:
        currentAuthor = session.scalars(
            select(Author).where(Author.name == currentAuthorName)
        ).first()

        if currentAuthor is None:
            currentAuthor = Author(name=currentAuthorName)

        authorObjects.append(currentAuthor)

    # Then query for the project
    authorCountSubQuery = session.query(
        func.count(Project.authors).label("author_count")
    ).subquery()

    project = session.scalars(
        select(Project)
        .where(*[Project.authors.any(Author.name == current) for current in authors])
        .where(Project.name == name)
        .where(Project.author_count == len(authors))
    ).first()

    if project is None:
        # Create project, if it doesn't exist yet
        project = Project(
            id=nextFreeID(session, Project), name=name, authors=authorObjects
        )

    return project
