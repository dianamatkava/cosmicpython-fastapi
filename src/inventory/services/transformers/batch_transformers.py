from src.inventory.domain.batch import BatchModel
from src.inventory.services.schemas.batch_dto import BatchSchemaDTO, BatchOutDTO


def transform_batch_model_to_dto(batch: BatchModel) -> BatchSchemaDTO:
    return BatchSchemaDTO(
        ref=batch.reference,
        sku=batch.sku,
        eta=batch.eta,
        qty=batch.available_quantity,
    )


def transform_batch_model_to_dto_out(batch: BatchModel) -> BatchOutDTO:
    return BatchOutDTO(
        reference=batch.reference,
        sku=batch.sku,
        eta=batch.eta,
        available_quantity=batch.available_quantity,
        allocations=batch.allocations
    )
