import pytest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy_utils import database_exists, create_database
from starlette.testclient import TestClient

from src.adapters.orm_mappers import start_mappers
from src.allocations.adapters.orm import metadata
from src.app import app
from src.settings import get_settings
from src.shared.repository import AbstractRepository

settings = get_settings()


@pytest.fixture(scope="session")
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")  # in memory db, or sqlite://
    # create all tables
    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def session(in_memory_db: Engine):
    start_mappers()
    connection = in_memory_db.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    clear_mappers()


@pytest.fixture(name="client")
def setup_client(postgres_db):
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def postgres_db():
    engine = create_engine(settings.DB_URL)

    if not database_exists(engine.url):
        create_database(engine.url)

    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(name="pg_session", scope="function")
def pg_session(postgres_db):
    start_mappers()
    connection = postgres_db.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    clear_mappers()


class FakeSession:
    committed = False
    rolledback = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolledback = True


class FakeRepository(AbstractRepository):
    def __init__(self, batches=(), *args, **kwargs):
        self._batches = set(batches)

    def build(self, batches):
        self._batches = set(batches)

    def add(self, reference):
        self._batches.add(reference)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)

    def delete(self, reference):
        batch = next(b for b in self._batches if b.reference == reference)
        return self._batches.remove(batch)


@pytest.fixture(name="fake_repository")
def get_fake_repository() -> FakeRepository:
    return FakeRepository()


@pytest.fixture(name="fake_session")
def get_fake_session() -> FakeSession:
    return FakeSession()
