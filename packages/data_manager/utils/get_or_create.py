from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from data_manager.orm import Project, Author, System, Keyword, Host


def get_or_create_project(session: Session, name: str) -> Project:
    """Gets the Project object with the given name. If no such object exists yet, a new one will be created
    and added to the given session. If more than one project with the same name exist, this function will error
    as disambiguation has to be done by the user (and then the desired project can be selected via its ID)
    """
    project = session.scalars(select(Project).where(Project.name == name)).one_or_none()

    if project is None:
        project = Project(name=name)
        session.add(project)

    return project


def get_or_create_author(
    session: Session, name: str, affiliation: Optional[str]
) -> Author:
    """Gets the Author with the given name (and affiliation). If no such object exists yet, a new one will
    be created and added to the session. In case the search yields more than a single existing result, this
    function will error as disambiguation has to be done by the user (and then the desired author can be selected
    via its ID)"""
    if affiliation is None:
        author = session.scalars(
            select(Author).where(Author.name == name)
        ).one_or_none()
    else:
        author = session.scalars(
            select(Author)
            .where(Author.name == name)
            .where(Author.affiliation == affiliation)
        ).one_or_none()

    if author is None:
        author = Author(name=name, affiliation=affiliation)
        session.add(author)

    return author


def get_or_create_system(session: Session, name: str, variant: Optional[str]) -> System:
    """Gets the Session with the given name (in the given variant). If no such object exists yet, a new one will
    be created and added to the session. In case the search yields more than a single existing result, this
    function will error as disambiguation has to be done by the user (and then the desired system can be selected
    via its ID)"""
    if variant is None:
        system = session.scalars(
            select(System).where(System.name == name)
        ).one_or_none()
    else:
        system = session.scalars(
            select(System).where(System.name == name).where(System.variant == variant)
        ).one_or_none()

    if system is None:
        system = System(name=name, variant=variant)
        session.add(system)

    return system


def get_or_create_keyword(session: Session, name: str) -> Keyword:
    """Gets the Keyword with the given name. If no such object exists yet, a new one will be created
    and added to the session. In case the search yields more than a single existing result, this function
    will error as disambiguation has to be done by the user (and then the desired keyword can be selected via its ID)
    """
    keyword = session.scalars(select(Keyword).where(Keyword.name == name)).one_or_none()

    if keyword is None:
        keyword = Keyword(name=name)
        session.add(keyword)

    return keyword


def get_or_create_host(session: Session, name: str) -> Host:
    """Gets the Host with the given name. If no such object exists yet, a new one will be created
    and added to the session. In case the search yields more than a single existing result, this function
    will error as disambiguation has to be done by the user (and then the desired host can be selected via its ID)
    """
    host = session.scalars(select(Host).where(Host.name == name)).one_or_none()

    if host is None:
        host = Host(name=name)
        session.add(host)

    return host
