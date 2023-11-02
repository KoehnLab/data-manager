from typing import Optional
from enum import Enum
from pathlib import Path

from sqlalchemy import create_engine, event, Engine, event
from sqlalchemy.orm import Session

from data_manager.orm import Base


class Backend(Enum):
    SQLite = 1


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # For SQLite we have to explicitly enable foreign keys
    # Once we also support different backends, this has to be made backend-agnostic
    # Taken from https://stackoverflow.com/a/12770354
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def open_database(
    database: str,
    backend: Backend = Backend.SQLite,
    host: Optional[str] = None,
    port: Optional[int] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    create_as_needed: bool = True,
) -> Session:
    if backend == Backend.SQLite:
        assert host is None
        assert port is None
        assert user is None
        assert password is None

        if not database.endswith(".sqlite"):
            database += ".sqlite"

        engine = create_engine("sqlite:///%s" % database)

        path = Path(database)
        if path.exists():
            if not path.is_file():
                raise RuntimeError(
                    "Can't create SQLite database at '%s' - path exists and is not a file"
                    % database
                )
        elif create_as_needed:
            Base.metadata.create_all(engine)
        else:
            raise RuntimeError(
                "Database '%s' does not exist and create_as_needed == False" % database
            )

        return Session(engine)

    else:
        raise RuntimeError("(Currently) unsupported database backend '%s'" % backend)
