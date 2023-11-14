#!/usr/bin/env python3

import unittest

import sqlalchemy.orm

from data_manager.orm import Base, Project, ProcessingStep, Result
from data_manager.utils import insert_collection_result, get_collection_result


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = sqlalchemy.create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sqlalchemy.orm.sessionmaker(bind=cls.engine)

    def test_collection_results(self):
        with self.Session() as session:
            project = Project(name="Dummy")
            step = ProcessingStep(kind="Example", project=project)

            listResult = [1, "test", 0.25]
            matrixResult = [[1, 2, 3], ["4", 5, "6"]]

            insert_collection_result(
                session=session, kind="ListTest", processing_step=step, data=listResult
            )
            insert_collection_result(
                session=session,
                kind="MatrixTest",
                processing_step=step,
                data=matrixResult,
            )

            session.add(project)
            session.commit()

            fetchedList = get_collection_result(
                session=session, kind="ListTest", processing_step=step
            )
            fetchedMatrix = get_collection_result(
                session=session, kind="MatrixTest", processing_step=step
            )

            self.assertEqual(listResult, fetchedList)
            self.assertEqual(matrixResult, fetchedMatrix)


if __name__ == "__main__":
    unittest.main()
