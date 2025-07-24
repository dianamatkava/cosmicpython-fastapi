# The Repository pattern is an abstraction over persistent storage
from typing import List, Type

from sqlalchemy.orm import Session

from src.allocations.domain.batch_domain_model import BatchModel
from src.shared.repository import AbstractRepository


class BatchAllocationsRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get(self, reference: str) -> Type[BatchModel]:
        return self.session.query(BatchModel).filter_by(reference=reference).one()

    # def add(self, product: domain.ProductAggregate) -> None:
    #     self.session.add(product)

    def list(self) -> List[Type[BatchModel]]:
        return self.session.query(BatchModel).all()

    # def delete(self, sku: str) -> None:
    #     self.session.query(domain.ProductAggregate).filter_by(sku=sku).delete()
