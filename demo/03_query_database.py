#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import asc
from sqlalchemy import desc

from data_manager.orm import (
    Calculation,
    Result,
    Method,
    BasisSet,
    System,
    MethodParameter,
    Energy,
    Host,
)


def main():
    ################################
    # Step 1: Create the SQL engine
    ################################

    # See the create_table.py script for more options to create the engine
    engine = create_engine("sqlite:///sampleDB.sqlite")

    ################################
    # Step 2: Connect to existing DB
    ################################

    with Session(engine) as session:
        ################################
        # Step 3: Perform desired queries
        ################################

        # More info about querying:
        # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-selecting-data

        # Note: All queries return rows, where each row may contain multiple entries
        # However, in some cases we know for sure that the returned rows will only contain
        # a single entry in which case, we can make use of session.scalars instead of session.execute

        # Iterate over all results stored in DB
        for row in session.execute(select(Result)):
            print("Found result for method '{}'".format(row[0].method.name))

        # The order of the returned rows is a priori undefined, but we can specify the desired order:
        print(
            "First method when sorting ascending: {}".format(
                session.scalars(select(Method).order_by(asc(Method.name))).first().name
            )
        )
        print(
            "First method when sorting descending: {}".format(
                session.scalars(select(Method).order_by(desc(Method.name))).first().name
            )
        )

        # Get all energies of methane that are > -12.59
        for energy in session.scalars(select(Energy).where(Energy.value > -12.59)):
            print(
                "Result of {} is {} (state: {}) and thus > -12.59".format(
                    energy.result.method.name,
                    energy.value,
                    (energy.state if energy.state else "Unknown"),
                )
            )

        # Note the slightly non-pythonic syntax inside the where clause. In particular note that only a single "&" is used
        # and if its arguments consist of multiple operands, they have to be put inside parenthesis
        result = session.scalars(
            select(Host).where(Host.cpu.contains("Intel") & (Host.cluster == "orpheus"))
        ).first()
        assert result != None
        print(result.name)

        # More information on what can be done inside the where clause:
        # https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#relationship-where-operators


if __name__ == "__main__":
    main()
