# The Repository pattern is an abstraction over persistent storage
from typing import List, Type

from sqlalchemy.orm import Session

from src.allocations.domain import batch_domain_model as domain


class ProductStockRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get(self, sku: str) -> Type[domain.ProductAggregate]:
        return self.session.query(domain.ProductAggregate).filter_by(sku=sku).one()

    def add(self, product: domain.ProductAggregate) -> None:
        self.session.add(product)

    def list(self) -> List[Type[domain.ProductAggregate]]:
        return self.session.query(domain.ProductAggregate).all()

    def delete(self, sku: str) -> None:
        self.session.query(domain.ProductAggregate).filter_by(sku=sku).delete()


class BatchRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get(self, reference: str) -> Type[domain.BatchModel]:
        return (
            self.session.query(domain.BatchModel).filter_by(reference=reference).one()
        )

    def add(self, batch: domain.BatchModel) -> None:
        self.session.add(batch)

    def list(self) -> List[Type[domain.BatchModel]]:
        return self.session.query(domain.BatchModel).all()

    def delete(self, reference: str) -> None:
        self.session.query(domain.BatchModel).filter_by(reference=reference).delete()
