from typing import Annotated

from pydantic import Field, BaseModel

from src.inventory.services.schemas import AllocationSchemaDTO


class AllocationRequestModel(AllocationSchemaDTO):
    """Order line schema request model."""

    order_line_id: Annotated[int, Field(description="Order line unique ID.")]


class DeAllocationRequestModel(AllocationSchemaDTO):
    """Order line schema request model."""

    order_line_id: Annotated[int, Field(description="Order line unique ID.")]


class ChangeBatchQuantityRequestModel(BaseModel):
    """Change batch quantity schema request model."""

    qty: Annotated[int, Field(description="New batch quantity")]
