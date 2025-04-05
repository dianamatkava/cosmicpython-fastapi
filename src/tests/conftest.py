import sqlite3
import time
from sqlite3 import OperationalError

import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.adapters.repository import BatchRepository, AbstractRepository
from src.adapters.uow import UnitOfWork
from src.app import app
from src.config import get_sqlite_uri
from src.services.batch_service import BatchService
from src.adapters.orm import metadata


@pytest.fixture(name="client")
def setup_client(sqlite_db):
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def sqlite_db():
    engine = create_engine(get_sqlite_uri(), connect_args={"check_same_thread": False}, poolclass=StaticPool)
    metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def session(sqlite_db):
    SessionLocal = sessionmaker(bind=sqlite_db)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def wait_for_db_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("DB never came up")


@pytest.fixture(name="sql_repository")
def get_sql_repository(session):
    return BatchRepository(session)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


class FakeRepository(AbstractRepository):

    def __init__(self, batches=()):
        self._batches = set(batches)

    def build(self, batches):
        self._batches = set(batches)

    def add(self, reference):
        self._batches.add(reference)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)


@pytest.fixture(name='fake_repository')
def get_fake_repository() -> FakeRepository:
    return FakeRepository()


@pytest.fixture(name='fake_session')
def get_fake_session() -> FakeSession:
    return FakeSession()


@pytest.fixture(name='fake_uof')
def get_fake_uof(fake_session: FakeSession, fake_repository: FakeRepository) -> UnitOfWork:
    return UnitOfWork(session_factory=lambda: fake_session, batch_repo=fake_repository)


@pytest.fixture(name='batch_service')
def get_batch_service(fake_uof: UnitOfWork) -> BatchService:
    return BatchService(uof=fake_uof)
