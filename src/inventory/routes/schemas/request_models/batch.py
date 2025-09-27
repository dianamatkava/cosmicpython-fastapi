from datetime import date
from typing import Optional, Annotated

from pydantic import BaseModel, Field


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
    ] = None
    qty: Annotated[int, Field(description="Quantity of the product.")]
