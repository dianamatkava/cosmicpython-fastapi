# The Repository pattern is an abstraction over persistent storage
from typing import List, Type

from sqlalchemy.orm import Session

from src.inventory.domain.product_aggregate import ProductAggregate
from src.shared.repository import AbstractRepository


class ProductRepository(AbstractRepository[ProductAggregate]):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get(self, sku: str) -> Type[ProductAggregate]:
        return self.session.query(ProductAggregate).filter_by(sku=sku).one()

    def add(self, product: ProductAggregate) -> None:
        self.session.add(product)

    def list(self) -> List[Type[ProductAggregate]]:
        return self.session.query(ProductAggregate).all()

    def delete(self, sku: str) -> None:
        self.session.query(ProductAggregate).filter_by(sku=sku).delete()
