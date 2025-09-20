from datetime import date
from typing import List, Annotated

from pydantic import BaseModel, Field

from src.inventory.services.schemas.allocations_dto import AllocationSchemaDTO
from src.inventory.services.schemas.batch_dto import BatchOutDTO


class BatchesListResponseModel(BatchOutDTO):
    """Model represent list of batches."""

    reference: Annotated[str, Field(description="Batch unique ID.")]
    sku: Annotated[str, Field(description="SKU (Stock Keeping Unit) of the product.")]
    eta: Annotated[
        date | None,
        Field(
            description="ETA ((Estimated Time of Arrival). Batches have an ETA if they are currently shipping. We allocate to shipment batches in order of which has the earliest ETA."
        ),
    ]
    available_quantity: Annotated[
        int, Field(description="Quantity of the product available in the batch.")
    ]
    allocations: Annotated[
        List[AllocationSchemaDTO], Field(description="List of inventory.")
    ]


class AllocationsAllocateResponseModel(BaseModel):
    """Model represent allocation response."""

    reference: Annotated[str, Field(description="Allocated batch unique ID.")]
    order_id: Annotated[str, Field(description="Allocated order unique ID.")]
