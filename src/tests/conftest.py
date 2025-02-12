import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from starlette.testclient import TestClient

from src.adapters.orm import metadata
from src.adapters.repository import BatchRepository, AbstractRepository
from src.app import app
from src.services.batch_service import BatchService


@pytest.fixture(name='client')
def setup_db() -> TestClient:
    client = TestClient(app)
    return client


@pytest.fixture()
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture(name="sql_repository")
def get_sql_repository(session):
    return BatchRepository(session)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


class FakeRepository(AbstractRepository):

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


@pytest.fixture(name='batch_service')
def get_batch_service(fake_repository: FakeRepository, fake_session: FakeSession) -> BatchService:
    return BatchService(fake_session, batch_repository=fake_repository)  # type: ignore
