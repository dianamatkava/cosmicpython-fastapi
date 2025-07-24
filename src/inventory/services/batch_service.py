"""business logic, Accepts only primitives or a minimal DTO"""

from datetime import date
from typing import Optional, List

from src.inventory.adapters.uow import InventoryBatchUnitOfWork
from src.inventory.domain.batch_model import InventoryBatchModel


class OutOfStock(Exception):
    """OutOfStock Exception"""


class BatchService:
    uow: InventoryBatchUnitOfWork

    def __init__(self, uow: InventoryBatchUnitOfWork):
        self.uow = uow

    def add_batch(
        self, ref: str, sku: str, qty: int, eta: Optional[date] = None
    ) -> None:
        with self.uow as uow:
            uow.batch_repo.add(InventoryBatchModel(ref, sku, eta, qty))
            uow.commit()

    def get_batche_by_ref(self, ref: str) -> InventoryBatchModel:
        with self.uow as uow:
            return uow.batch_repo.get(reference=ref)

    def get_batches(self) -> List[InventoryBatchModel]:
        with self.uow as uow:
            return uow.batch_repo.list()

    def delete_batch(self, ref: str) -> None:
        with self.uow as uow:
            uow.batch_repo.delete(reference=ref)
            uow.commit()
