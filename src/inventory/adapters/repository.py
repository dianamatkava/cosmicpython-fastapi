# The Repository pattern is an abstraction over persistent storage
from typing import List, Type

from sqlalchemy.orm import Session

from src.inventory.domain.batch_model import InventoryBatchModel
from src.shared.repository import AbstractRepository


class InventoryBatchRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get(self, reference: str) -> Type[InventoryBatchModel]:
        return (
            self.session.query(InventoryBatchModel).filter_by(reference=reference).one()
        )

    def add(self, batch: InventoryBatchModel) -> None:
        self.session.add(batch)

    def list(self) -> List[Type[InventoryBatchModel]]:
        return self.session.query(InventoryBatchModel).all()

    def delete(self, reference: str) -> None:
        self.session.query(InventoryBatchModel).filter_by(reference=reference).delete()
