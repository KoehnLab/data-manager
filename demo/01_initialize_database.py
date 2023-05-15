#!/usr/bin/env python3

from sqlalchemy import create_engine

from data_manager.orm import Base


def main():
    ################################
    # Step 1: Create the SQL engine
    ################################

    # More detailed info on used DB URL scheme (can also include username, password, etc.):
    # https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
    
    # Could be one a remote machine:
    # engine = create_engine("mysql://username@host:/database_name")

    # For playing around, we can create an in-memory DB that only exists for
    # as long as our program is running
    # engine = create_engine("sqlite://")

    # Create DB at absolute file path (4 leading slashes):
    # engine = create_engine("sqlite:////home/user/Documents/MyDB.sqlite")

    # Create DB using a relative path (3 leading slashes)
    engine = create_engine("sqlite:///sampleDB.sqlite")

    # Note: SQLite is the only DB where the DB itself is stored as a file. All other
    # backends require a daemon process to run on the target machine and those won't
    # create simple files for individual DBs


    ################################
    # Step 2: Initialize our DB
    ################################
    
    # Note: All the tables contained in data-manager are registered to this Base class
    # Therefore, it knows what tables shall exist and is able to (and responsible for)
    # create all tables that we need
    Base.metadata.create_all(engine)




if __name__ == "__main__":
    main()
