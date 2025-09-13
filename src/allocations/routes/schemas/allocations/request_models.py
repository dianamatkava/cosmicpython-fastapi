from typing import Annotated

from pydantic import Field

from src.allocations.services.schemas import AllocationSchemaDTO


class AllocationRequestModel(AllocationSchemaDTO):
    """Order line schema request model."""

    order_line_id: Annotated[int, Field(description="Order line unique ID.")]


class DeAllocationRequestModel(AllocationSchemaDTO):
    """Order line schema request model."""

    order_line_id: Annotated[int, Field(description="Order line unique ID.")]
