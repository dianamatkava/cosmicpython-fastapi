# The Repository pattern is an abstraction over persistent storage
from typing import List, Type
import sqlalchemy as sa
from sqlalchemy.orm import Session
from src.adapters.orm_mappers import product as _product
from src.allocations.domain.product_agregate_model import ProductAggregate
from src.shared.repository import AbstractRepository


class ConcurrencyError(Exception):
    pass


class ProductAggregateRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get(self, sku: str) -> Type[ProductAggregate]:
        return self.session.query(ProductAggregate).filter_by(sku=sku).one()

    def add(self, sku: str) -> None:
        raise NotImplementedError

    def update_version(self, product: ProductAggregate) -> None:
        old = product.version_number
        query = (
            sa.update(_product)
            .where(_product.c.sku == product.sku, _product.c.version_number == old)
            .values(version_number=old + 1)
        )
        if self.session.execute(query).rowcount == 0:
            raise ConcurrencyError(f"Concurrent update for product {product.sku}")

    def list(self) -> List[Type[ProductAggregate]]:
        return self.session.query(ProductAggregate).all()

    def delete(self, sku: str) -> None:
        raise NotImplementedError
