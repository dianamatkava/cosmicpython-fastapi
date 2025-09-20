from typing import List, Type, Tuple, Set

import pytest
from sqlalchemy.exc import NoResultFound

from src.inventory.domain.batch import BatchModel
from src.inventory.domain.product_aggregate import ProductAggregate
from src.inventory.services.batch_service import BatchService
from src.inventory.services.product_service import ProductService
from src.orders.domain.order_line_model import OrderLineModel
from src.shared.repository import AbstractRepository
from src.shared.uow import AbstractUnitOfWork


class FakeProductRepository(AbstractRepository):
    seen: Set

    def __init__(self, products: Tuple[ProductAggregate] = (), *args, **kwargs):
        self._products = set(products)
        self.seen = set()

    def build(self, products: List[ProductAggregate]) -> None:
        self._products = set(products)

    def add(self, product: ProductAggregate) -> None:
        self._products.add(product)

    def get(self, **kwargs) -> ProductAggregate:
        if sku := kwargs.get('sku'):
            return self.get_by_sku(sku=sku)
        elif ref := kwargs.get('ref'):
            return self.get_by_batch_ref(ref=ref)
        else:
            raise TypeError(f"{self}.get() got an unexpected keyword argument/s {kwargs.keys()}")

    def get_by_sku(self, sku: str) -> ProductAggregate:
        return next(p for p in self._products if p.sku == sku)

    def get_by_batch_ref(self, ref: str) -> ProductAggregate:
        return next(p for p in self._products if ref in set(b.reference for b in p.batches))

    def list(self) -> List[ProductAggregate]:
        return list(self._products)

    def delete(self, sku) -> None:
        product = next(b for b in self._products if b.sku == sku)
        self._products.remove(product)


class FakeBatchRepository(AbstractRepository):
    def __init__(self, batches=(), *args, **kwargs):
        self._batches = set(batches)

    def build(self, batches: List[BatchModel]) -> None:
        self._batches = set(batches)

    def add(self, batch: BatchModel) -> None:
        self._batches.add(batch)

    def get(self, reference: str) -> BatchModel:
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> List[BatchModel]:
        return list(self._batches)

    def delete(self, reference: str) -> None:
        batch = next(b for b in self._batches if b.reference == reference)
        self._batches.remove(batch)


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


class FakeUoW(AbstractUnitOfWork):
    committed: bool | None = False
    product_aggregate_repo: Type[AbstractRepository]
    order_line_repo: Type[AbstractRepository]
    batch_repo: Type[AbstractRepository]

    def __init__(
        self,
        session_factory,
        product_aggregate_repo: FakeProductRepository,
        order_line_repo: FakeOrderLineRepository,
        batch_repo: FakeBatchRepository,
    ) -> None:
        self.session_factory = session_factory
        self.product_aggregate_repo: AbstractRepository = product_aggregate_repo
        self.order_line_repo: AbstractRepository = order_line_repo
        self.batch_repo: AbstractRepository = batch_repo

    def __enter__(self):
        self.session = self.session_factory()
        return super().__enter__()

    def __exit__(self, *args, **kwargs):
        pass

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.committed = None

    def collect_events(self):
        events = []
        for product in self.product_aggregate_repo.seen:
            while product.events:
                events.append(product.events.pop(0))
        return events


class FakeSession:
    committed = False
    rolledback = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolledback = True


@pytest.fixture(name="fake_session")
def get_fake_session() -> FakeSession:
    return FakeSession()


@pytest.fixture(name="fake_uof")
def get_fake_uof(fake_session: FakeSession) -> FakeUoW:
    return FakeUoW(session_factory=lambda: fake_session)


@pytest.fixture(name="uow")
def get_fake_uow(fake_session: FakeSession, batch_repo: FakeBatchRepository, product_aggregate_repo: FakeProductRepository, order_line_repo: FakeOrderLineRepository):
    return FakeUoW(
        session_factory=lambda: fake_session,
        product_aggregate_repo=product_aggregate_repo,
        batch_repo=batch_repo,
        order_line_repo=order_line_repo,
    )


@pytest.fixture(name="batch_repo")
def get_batch_repo():
    return FakeBatchRepository()


@pytest.fixture(name="order_line_repo")
def get_order_line_repo():
    return FakeOrderLineRepository()


@pytest.fixture(name="product_aggregate_repo")
def get_product_aggregate_repo():
    return FakeProductRepository()


@pytest.fixture(name="batch_service")
def get_batch_service(uow: FakeUoW):
    return BatchService(uow=uow)


@pytest.fixture(name="product_service")
def get_product_service(uow: FakeUoW):
    return ProductService(uow=uow)
