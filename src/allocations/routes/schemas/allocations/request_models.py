from datetime import date
from typing import Optional, Annotated

from pydantic import BaseModel, Field

from src.allocations.services.schemas import AllocationSchemaDTO


class BatchesCreationModelRequestModel(BaseModel):
    """Batch creation schema request model."""

    ref: Annotated[str, Field(description="Batch unique ID.")]
    sku: Annotated[
        str, Field(description="A product is identified by a SKU (Stock Keeping Unit).")
    ]
    eta: Annotated[
        Optional[date],
        Field(
            description="ETA ((Estimated Time of Arrival). Batches have an ETA if they are currently shipping. We allocate to shipment batches in order of which has the earliest ETA."
        ),
    ]
    qty: Annotated[int, Field(description="Quantity of the product.")]


class OrderLineModelRequestModel(AllocationSchemaDTO):
    """Order line schema request model."""

    order_id: Annotated[str, Field(description="Order unique ID.")]
    sku: Annotated[
        str, Field(description="SKU (Stock Keeping Unit) of the product to allocate.")
    ]
    qty: Annotated[int, Field(description="Quantity of the product to allocate.")]
