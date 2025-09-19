# The Repository pattern is an abstraction over persistent storage
from typing import List

from sqlalchemy.orm import Session

from src.inventory.domain.batch import BatchModel
from src.shared.repository import AbstractRepository


class BatchRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get(self, reference: str) -> BatchModel:
        return (
            self.session.query(BatchModel).filter_by(reference=reference).one()
        )

    def add(self, batch: BatchModel) -> None:
        self.session.add(batch)

    def list(self) -> List[BatchModel]:
        return self.session.query(BatchModel).all()

    def delete(self, reference: str) -> None:
        raise NotImplementedError
