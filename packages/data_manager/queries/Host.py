from typing import Optional

from data_manager.orm import Host

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import func


def countHosts(
    session: Session, name: str, cpu: Optional[str], cluster: Optional[str]
) -> int:
    query = select(func.count()).select_from(Host).where(Host.name == name)
    if not cpu is None:
        query = query.where(Host.cpu == cpu)
    if not cluster is None:
        query = query.where(Host.cluster == cluster)

    count = session.scalars(query).first()

    assert count != None

    return count


def hostExists(
    session: Session, name: str, cpu: Optional[str], cluster: Optional[str]
) -> bool:
    return countHosts(session=session, name=name, cpu=cpu, cluster=cluster) > 0


def getHost(
    session: Session,
    name: str,
    cpu: Optional[str] = None,
    cluster: Optional[str] = None,
) -> Host:
    query = select(Host).where(Host.name == name)

    if not cpu is None:
        query = query.where(Host.cpu == cpu)

    if not cluster is None:
        query = query.where(Host.cluster == cluster)

    host = session.scalars(query).first()

    if host is None:
        host = Host(name=name, cpu=cpu, cluster=cluster)

    return host
