import pytest
from sqlalchemy.orm import Session

from src.conftest import FakeRepository, FakeSession
from src.inventory.adapters.repository import ProductRepository
from src.inventory.adapters.uow import ProductUnitOfWork
from src.inventory.services.product_service import ProductService


@pytest.fixture(name="sql_repository")
def get_sql_repository(session: Session) -> ProductRepository:
    return ProductRepository(session)


@pytest.fixture(name="fake_uof")
def get_fake_uof(fake_session: FakeSession) -> ProductUnitOfWork:
    return ProductUnitOfWork(
        session_factory=lambda: fake_session, product_repo=FakeRepository
    )


@pytest.fixture(name="product_service")
def get_batch_service(fake_uof: ProductUnitOfWork) -> ProductService:
    return ProductService(uow=fake_uof)
