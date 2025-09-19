"""business logic, Accepts only primitives or a minimal DTO"""

from datetime import date
from typing import Optional, List

from src.inventory.adapters.uow import ProductAggregateUnitOfWork
from src.inventory.domain.batch import BatchModel
from src.inventory.services.schemas.batch_dto import BatchSchemaDTO
from src.inventory.services.transformers.batch_transformers import (
    transform_batch_model_to_dto,
)


class OutOfStock(Exception):
    """OutOfStock Exception"""


class BatchService:
    uow: ProductAggregateUnitOfWork

    def __init__(self, uow: ProductAggregateUnitOfWork):
        self.uow = uow

    def add_batch(
        self, ref: str, sku: str, qty: int, eta: Optional[date] = None
    ) -> BatchSchemaDTO:
        with self.uow as uow:
            uow.batch_repo.add(BatchModel(ref, sku, eta, qty))
            created_batch = uow.batch_repo.get(ref)
            uow.commit()
            # TODO: IntegrityError
            # TODO: UniqueViolation
            # TODO: ForeignKeyViolation
        return transform_batch_model_to_dto(created_batch)

    def get_batche_by_ref(self, ref: str) -> BatchSchemaDTO:
        with self.uow as uow:
            batch = uow.batch_repo.get(reference=ref)
        return transform_batch_model_to_dto(batch)

    def get_batches(self) -> List[BatchSchemaDTO]:
        with self.uow as uow:
            batches = uow.batch_repo.list()
        return [transform_batch_model_to_dto(batch) for batch in batches]

    def delete_batch(self, ref: str) -> None:
        with self.uow as uow:
            uow.batch_repo.delete(reference=ref)
            uow.commit()
