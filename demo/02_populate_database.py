#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from data_manager.orm import (
    Calculation,
    Project,
    Author,
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
        # Note: We are assuming that our DB is completely empty to begin with

        ################################
        # Step 3: Create data objects
        ################################

        # Create a project to which the calculation belongs
        myProject = Project(name="Sample project", authors=[Author(name="Alan Turing")])

        # Assume we did a CCSD calculation on methane
        calc = Calculation(
            project=myProject,
            output_path="/path/to/calculation.out",
            host=Host(
                name="orpheus42",
                cpu="Intel(R) Xeon(R) CPU E5-2640 v4 @ 2.40GHz",
                cluster="orpheus",
            ),
        )

        assert len(myProject.calculations) == 1

        methane = System(name="Methane", charge=0, multiplicity=0)
        ccpVDZ = BasisSet(name="cc-pVDZ")
        rhfMethod = Method(name="RHF")

        # First thing we had to do was a RHF calculation
        rhfResult = Result(
            calculation=calc,  # Associate this result with calc
            method=rhfMethod,
            method_parameter=MethodParameter(symmetry="Td", density_fitting=True),
            system=methane,
            basis_set=ccpVDZ,
            energies=[
                Energy(value=-12.5, state="1.1"),
                Energy(value=-12.6, state="2.1"),
            ],
        )

        # Since we associated the rhfResult with calc above, the rhfResult itself has automatically
        # been added to the list of results in calc
        assert len(calc.results) == 1

        # Followed by the actual CCSD calculation
        ccsdMethod = Method(name="CCSD")
        ccsdResult = Result()
        ccsdResult.method = ccsdMethod
        ccsdResult.method_parameter = MethodParameter(
            symmetry="Td", density_fitting=True, additional="special_parameter=42"
        )
        ccsdResult.basis_set = ccpVDZ
        ccsdResult.system = methane
        ccsdResult.energies = [Energy(value=-12.55)]

        # This is the alternative of associating a calculation and a result
        calc.results.append(ccsdResult)
        # The syncing of the association is bidirectional
        assert ccsdResult.calculation == calc

        ################################
        # Step 4: Add data to DB
        ################################

        session.add(rhfResult)
        session.add(ccsdResult)
        # or: session.add_all([rhfResult, ccsdResult])

        ################################
        # Step 5: Commit changes
        ################################

        # IMPORTANT: Only after you commit your changes, will they actually be stored in the DB
        # Without the commit, everything you have changed (since the last commit) will be undone
        # -> very handy for error handling as errors will automatically undo all changes that led
        #    to the error
        session.commit()


if __name__ == "__main__":
    main()
