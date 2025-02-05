from typing import Any

import pytest

from src.adapters.repository import AbstractRepository
from src.services.batch_service import BatchService


@pytest.fixture(name='fake_repository')
def get_fake_repository() -> AbstractRepository:
    return AbstractRepository()


class FakeRepository(AbstractRepository):

    def add(self, reference):
        pass

    def get(self, reference):
        pass

    def list(self):
        pass


@pytest.fixture(name='batch_service')
def get_batch_service(fake_repository: AbstractRepository) -> BatchService:
    return BatchService(Any, batch_repository=fake_repository)


def test_allocate():
    pass
