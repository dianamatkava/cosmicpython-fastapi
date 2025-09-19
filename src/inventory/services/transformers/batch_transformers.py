from src.inventory.domain.batch import BatchModel
from src.inventory.services.schemas.batch_dto import BatchSchemaDTO


def transform_batch_model_to_dto(batch: BatchModel) -> BatchSchemaDTO:
    return BatchSchemaDTO(
        reference=batch.reference,
        sku=batch.sku,
        eta=batch.eta,
        available_quantity=batch.available_quantity,
        allocations=batch.allocations
    )
