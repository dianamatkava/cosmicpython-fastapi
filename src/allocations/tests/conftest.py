import pytest
from sqlalchemy.orm import Session

from src.allocations.adapters.repository import (
    ProductStockRepository,
    AbstractRepository,
)
from src.allocations.adapters.uow import UnitOfWork
from src.allocations.services.batch_service import BatchService


@pytest.fixture(name="sql_repository")
def get_sql_repository(session: Session):
    return ProductStockRepository(session)


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


@pytest.fixture(name="fake_uof")
def get_fake_uof(fake_session: FakeSession) -> UnitOfWork:
    return UnitOfWork(session_factory=lambda: fake_session, batch_repo=FakeRepository)


@pytest.fixture(name="batch_service")
def get_batch_service(fake_uof: UnitOfWork) -> BatchService:
    return BatchService(uow=fake_uof)
