from src.inventory.services.schemas import BatchSchemaDTO
from src.register.domain.batch_model import InventoryBatchModel


def transform_batch_model_to_dto(batch: InventoryBatchModel) -> BatchSchemaDTO:
    return BatchSchemaDTO(
        reference=batch.reference,
        sku=batch.sku,
        eta=batch.eta,
        qty=batch._purchased_quantity,
    )
