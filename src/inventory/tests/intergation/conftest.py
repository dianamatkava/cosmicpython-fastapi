import pytest
from requests import Session

from src.inventory.adapters.repositories.batch_repository import BatchRepository
from src.inventory.adapters.repositories.product_repository import ProductAggregateRepository


@pytest.fixture(name="product_repository")
def get_product_repository(session: Session) -> ProductAggregateRepository:
    return ProductAggregateRepository(session)


@pytest.fixture(name="batch_repository")
def get_batch_repository(session: Session) -> BatchRepository:
    return BatchRepository(session)

