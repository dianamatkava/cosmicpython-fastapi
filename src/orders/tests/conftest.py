from typing import Type, List

import pytest
from sqlalchemy.exc import NoResultFound

from src.orders.adapters.uow import OrderLineUnitOfWork
from src.orders.domain.order_line_model import OrderLineModel
from src.orders.services.order_line_service import OrderLineService
from src.shared.repository import AbstractRepository
from src.shared.uow import AbstractUnitOfWork


class FakeOrderLineRepository(AbstractRepository):
    def __init__(self, order_lines=(), *args, **kwargs):
        self._order_lines = set(order_lines)

    def build(self, order_lines: List[OrderLineModel]) -> None:
        self._order_lines = set(order_lines)

    def add(self, order_line: OrderLineModel) -> None:
        self._order_lines.add(order_line)

    def get(self, id: int) -> OrderLineModel:
        try:
            return next(ol for ol in self._order_lines if ol.id == id)
        except StopIteration:
            raise NoResultFound()

    def list(self) -> List[OrderLineModel]:
        return list(self._order_lines)

    def delete(self, id: int) -> None:
        try:
            order_line = next(ol for ol in self._order_lines if ol.id == id)
        except StopIteration:
            raise NoResultFound()
        self._order_lines.remove(order_line)


class FakeProductRepository(AbstractRepository):
    def __init__(self, products=(), *args, **kwargs):
        self._products = set(products)

    def get(self, sku: str):
        if sku == "NONEXISTENT_SKU":
            from sqlalchemy.exc import NoResultFound

            raise NoResultFound()
        return type("Product", (), {"sku": sku})()

    def add(self, product) -> None:
        self._products.add(product)

    def list(self):
        return list(self._products)

    def delete(self, sku: str) -> None:
        pass


class FakeOrderLineUnitOfWork(AbstractUnitOfWork):
    committed: bool | None = False
    order_line_repo: Type[AbstractRepository]
    product_repo: Type[AbstractRepository]

    def __init__(
        self,
        order_line_repo: AbstractRepository = FakeOrderLineRepository,
        product_repo: AbstractRepository = FakeProductRepository,
    ) -> None:
        self.order_line_repo = order_line_repo
        self.product_repo = product_repo

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.committed = None


@pytest.fixture(name="fake_order_line_repo")
def get_fake_order_line_repo() -> FakeOrderLineRepository:
    return FakeOrderLineRepository()


@pytest.fixture(name="fake_product_repo")
def get_fake_product_repo() -> FakeProductRepository:
    return FakeProductRepository()


@pytest.fixture(name="fake_order_line_uow")
def get_fake_order_line_uow(
    fake_order_line_repo: FakeOrderLineRepository,
    fake_product_repo: FakeProductRepository,
) -> FakeOrderLineUnitOfWork:
    return FakeOrderLineUnitOfWork(
        order_line_repo=fake_order_line_repo, product_repo=fake_product_repo
    )


@pytest.fixture(name="order_line_service")
def get_order_line_service(
    fake_order_line_uow: OrderLineUnitOfWork,
) -> OrderLineService:
    return OrderLineService(uow=fake_order_line_uow)
