import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from starlette.testclient import TestClient

from src.adapters.orm import metadata, start_mappers
from src.adapters.repository import BatchRepository, AbstractRepository
from src.adapters.uow import UnitOfWork
from src.app import app
from src.services.batch_service import BatchService


@pytest.fixture(name="client")
def setup_client(in_memory_db):
    with TestClient(app) as client:
        yield client


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    # create all tables
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db):
    yield sessionmaker(bind=in_memory_db)
    clear_mappers()


@pytest.fixture
def session(session_factory):
    return session_factory()


@pytest.fixture(name="sql_repository")
def get_sql_repository(session):
    return BatchRepository(session)


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


@pytest.fixture(name='fake_repository')
def get_fake_repository() -> FakeRepository:
    return FakeRepository()


@pytest.fixture(name='fake_session')
def get_fake_session() -> FakeSession:
    return FakeSession()


@pytest.fixture(name='fake_uof')
def get_fake_uof(fake_session: FakeSession) -> UnitOfWork:
    return UnitOfWork(session_factory=lambda: fake_session, batch_repo=FakeRepository)


@pytest.fixture(name='batch_service')
def get_batch_service(fake_uof: UnitOfWork) -> BatchService:
    return BatchService(uof=fake_uof)
