#!/usr/bin/env python3

from sqlalchemy import create_engine

from data_manager.orm import Base

def main():
    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
