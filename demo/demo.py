#!/usr/bin/env python3

from data_manager.orm import Base, Project, Author, ProcessingStep, Result
from data_manager.utils import open_database

from sqlalchemy import select, exists, func, delete
from sqlalchemy.orm import Session


def add_data(session: Session):
    # New data is added by first creating the corresponding Python objects

    project = Project(name="Sample project")
    project.authors.add(Author(name="Jane Doe", affiliation="Hollywood"))

    # Adding an author to a project automatically back-populates the projects attribute of that Author
    assert project in next(iter(project.authors)).projects

    step1 = ProcessingStep(kind="RHF", project=project)
    step1.results.append(
        Result(kind="Energy", data=-738.735229, properties={"state": "1.1"})
    )

    step2 = ProcessingStep(kind="CCSD", project=project)
    step2.preceding_steps.add(step1)
    step2.results.append(
        Result(kind="Energy", data=-738.945872, properties={"state": "1.1"})
    )

    # Again, we have an automatic back-population where adding step A as the preceding step
    # of step B, will automatically add B to the dependent_steps of A
    assert step2 in step1.dependent_steps

    # Now we have to add the corresponding objects to the database explicitly
    # Note that we only have to add the top-level object explicitly. All referenced
    # objects are also added automatically. But adding them explicitly doesn't hurt either
    session.add(project)

    # And finally - very important - we have to commit our changes.
    # If we don't commit, our changes are rolled back automatically as soon
    # as the current session gets closed. This is handy in case there is an
    # error (exception) as this prevents a partial write where only a part of
    # your changes are reflected in the database, but not all of it.
    # So really, this makes the changes all or nothing.
    session.commit()


def select_data(session: Session):
    # Data is retrieved by means of SELECT statements
    # A select yields a result set of which we can then select what we want. That is,
    # a select always yields ALL elements that fulfill the search criteria.

    # If we are only interested in the FIRST result, then we can use the first() function
    # Note that this returns None, if the result set was empty
    firstProject = session.scalars(
        select(Project).where(Project.name == "Sample project")
    ).first()

    # If we wanted ALL elements of the result set, we can use the all() function
    projectList = session.scalars(
        select(Project).where(Project.name == "Sample project")
    ).all()

    # If we know that the result set must have exactly ONE element in it, we can use the one() function
    # Note that this function will raise an exception if the result set is empty or contains more than
    # one element
    exactlyOneProject = session.scalars(
        select(Project).where(Project.name == "Sample project")
    ).one()

    # If we know that the result set can have at most one element (that is, it is empty or it contains a single
    # element), we can use the one_or_none() function.
    # This function raises an exception if the result set contains more than one element and returns None if the
    # result set contained exactly one element
    atMostOneProject = session.scalars(
        select(Project).where(Project.name == "Sample project")
    ).one_or_none()


def check_for_existence(session: Session):
    # In order to check whether the database contains a given data, we can use the exists query
    # Note that the where clause needs to be added to the exists() and not to the select()
    projectExists = session.scalars(
        select(exists(Project).where(Project.name == "Dummy project"))
    ).one()


def count_occurrences(session: Session):
    # For counting we have to use a slightly different syntax as with e.g. checking for existence
    amountOfMatches = session.scalars(
        select(func.count())
        .select_from(Project)
        .filter(Project.name == "Sample project")
    ).one()

    # We can also count all projects, regardless of their name by omitting the where clause
    # (same applies for SELECT queries)
    amountOfProjects = session.scalars(select(func.count()).select_from(Project)).one()


def modify_objects(session: Session):
    # In order to modify, we first have to obtain an object from the DB
    project = session.scalars(
        select(Project).where(Project.name == "Sample project")
    ).one()

    # Then modify the object using regular Python
    project.authors.add(Author(name="Other author"))

    # And finally - as required for all changes to be persistent - we commit the changes
    session.commit()


def delete_data(session: Session):
    # If you want to remove an element from the database, you have to use a delete query

    # Note that deleting non-existent elements is a no-op
    session.execute(delete(Project).where(Project.name == "Horst"))

    # Be very careful with delete statements! If you omit the where clause, the statement
    # will delete ALL elements of the given kind. E.g.
    # session.scalars(delete(Project))
    # would delete ALL projects.

    # Furthermore, note that deleting an element deletes all other elements that are uniquely
    # associated with that object. For instance, every processing step is assigned to exactly
    # one project. Therefore, deleting the project a step belongs to, implicitly also deletes
    # this step (and every other step associated with this project).
    # To illustrate:
    assert session.scalars(select(func.count()).select_from(ProcessingStep)).one() == 2
    session.execute(delete(Project))
    assert session.scalars(select(func.count()).select_from(ProcessingStep)).one() == 0

    # As with all changes, we have to explicitly commit in order for the changes to become persistent
    session.commit()


def main():
    with open_database("sample_db") as session:
        add_data(session)
        select_data(session)
        check_for_existence(session)
        count_occurrences(session)
        modify_objects(session)
        delete_data(session)


if __name__ == "__main__":
    main()
