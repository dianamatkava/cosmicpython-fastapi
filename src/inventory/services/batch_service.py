"""business logic, Accepts only primitives or a minimal DTO"""

from typing import List

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
        self, batch: BatchSchemaDTO
    ) -> BatchSchemaDTO:
        batch_model = BatchModel(**batch.model_dump())
        with self.uow as uow:
            uow.batch_repo.add(batch_model)
            uow.commit()
            pass
            # TODO: IntegrityError
            # TODO: UniqueViolation
            # TODO: ForeignKeyViolation
        return transform_batch_model_to_dto(batch_model)

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
