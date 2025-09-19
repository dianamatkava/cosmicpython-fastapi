# The Repository pattern is an abstraction over persistent storage
from typing import Set

import sqlalchemy as sa
from sqlalchemy.orm import Session

from src.adapters.orm_mappers import product as _product
from src.inventory.domain.product_aggregate import ProductAggregate
from src.shared.repository import AbstractRepository


class ConcurrencyError(Exception):
    pass


class ProductAggregateRepository(AbstractRepository):
    session: Session
    seen: Set[ProductAggregate]

    def __init__(self, session: Session):
        self.session = session
        self.seen = set()

    def get(self, sku: str) -> ProductAggregate:
        res = self.session.query(ProductAggregate).filter_by(sku=sku).one()
        if res:
            self.seen.add(res)
        return res

    def get_by_batch_ref(self, ref: str) -> ProductAggregate:
        res = self.session.query(ProductAggregate).filter_by(batches__ref=ref).one()
        if res:
            self.seen.add(res)
        return res

    def add(self, sku: str) -> None:
        raise NotImplementedError

    def cas(self, product: ProductAggregate) -> None:
        old = product.version_number
        query = (
            sa.update(_product)
            .where(_product.c.sku == product.sku, _product.c.version_number == old)
            .values(version_number=old + 1)
        )
        if self.session.execute(query).rowcount == 0:
            raise ConcurrencyError(f"Concurrent update for product {product.sku}")

    def list(self) -> None:
        raise NotImplementedError

    def delete(self, sku: str) -> None:
        raise NotImplementedError
