#!/usr/bin/env python3

import unittest

from datetime import datetime, timedelta

from sqlalchemy import select
import sqlalchemy.orm
import sqlalchemy.exc

from data_manager.orm import Base, Host, ProcessingStep, Result, System, Project


class TestORM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = sqlalchemy.create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sqlalchemy.orm.sessionmaker(bind=cls.engine)

    def test_host(self):
        with self.Session() as session:
            host1 = Host(name="host1")
            host2 = Host(
                name="host2",
                date=datetime(year=2011, month=5, day=13, hour=12, minute=0, second=0),
            )
            host1.properties["cpu"] = "Intel Xeon"

            session.add_all([host1, host2])

            session.commit()

        with self.Session() as session:
            host1 = session.scalars(select(Host).where(Host.name == "host1")).one()
            self.assertEqual(host1.name, "host1")
            self.assertLessEqual(
                datetime.utcnow() - host1.date,
                timedelta(days=0, hours=0, minutes=0, seconds=15),
            )
            self.assertEqual(len(host1.properties), 1)
            self.assertEqual(host1.properties["cpu"], "Intel Xeon")

            host2 = session.scalars(select(Host).where(Host.name == "host2")).one()
            self.assertEqual(host2.name, "host2")
            self.assertEqual(
                host2.date,
                datetime(year=2011, month=5, day=13, hour=12, minute=0, second=0),
            )
            self.assertEqual(len(host2.properties), 0)

    def test_result(self):
        with self.Session() as session:
            project = Project(name="Dummy")
            step = ProcessingStep(kind="Dummy", project=project)

            res1 = Result(kind="Energy", data=-21.34)
            res1.processing_step = step

            res2 = Result(kind="Spin symmetry", data="Doublet")
            res2.processing_step = step

            res1.properties["state"] = "1.1"

            session.add_all([res1, res2])

            session.commit()

        with self.Session() as session:
            res1 = session.scalars(select(Result).where(Result.kind == "Energy")).one()
            self.assertEqual(res1.kind, "Energy")
            self.assertAlmostEqual(res1.data, -21.34)  # type: ignore
            self.assertEqual(len(res1.properties), 1)
            self.assertEqual(res1.properties["state"], "1.1")

            res2 = session.scalars(
                select(Result).where(Result.kind == "Spin symmetry")
            ).one()
            self.assertEqual(res2.kind, "Spin symmetry")
            self.assertEqual(res2.data, "Doublet")
            self.assertEqual(len(res2.properties), 0)

    def test_system(self):
        with self.Session() as session:
            sys1 = System(name="Methane", properties={"geometry_type": "XYZ"})
            sys2 = System(name="Water", variant="distorted")

            session.add_all([sys1, sys2])
            session.commit()

        with self.Session() as session:
            sys1 = session.scalars(select(System).where(System.name == "Methane")).one()
            sys2 = session.scalars(select(System).where(System.name == "Water")).one()

            self.assertEqual(sys1.name, "Methane")
            self.assertEqual(sys1.variant, None)
            self.assertEqual(len(sys1.properties), 1)
            self.assertEqual(sys1.properties["geometry_type"], "XYZ")

            self.assertEqual(sys2.name, "Water")
            self.assertEqual(sys2.variant, "distorted")
            self.assertEqual(len(sys2.properties), 0)

    def test_processing_step(self):
        with self.Session() as session:
            project = Project(name="Dummy")

            step1 = ProcessingStep(kind="RHF", project=project)
            step2 = ProcessingStep(
                kind="CCSD", project=project, preceding_steps={step1}
            )

            step1.properties["basis"] = "cc-pVTZ"

            session.add_all([step1, step2])
            session.commit()

        with self.Session() as session:
            step1 = session.scalars(
                select(ProcessingStep).where(ProcessingStep.kind == "RHF")
            ).one()
            step2 = session.scalars(
                select(ProcessingStep).where(ProcessingStep.kind == "CCSD")
            ).one()

            self.assertEqual(step1.kind, "RHF")
            self.assertEqual(len(step1.preceding_steps), 0)
            self.assertEqual(len(step1.dependent_steps), 1)
            self.assertEqual(next(iter(step1.dependent_steps)), step2)
            self.assertEqual(len(step1.properties), 1)
            self.assertEqual(step1.properties["basis"], "cc-pVTZ")

            self.assertEqual(step2.kind, "CCSD")
            self.assertEqual(len(step2.preceding_steps), 1)
            self.assertEqual(next(iter(step2.preceding_steps)), step1)
            self.assertEqual(len(step2.dependent_steps), 0)


if __name__ == "__main__":
    unittest.main()
