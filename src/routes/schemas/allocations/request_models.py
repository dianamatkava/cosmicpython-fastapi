from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.services.schemas import AllocationSchemaDTO


class BatchesCreationModelRequestModel(BaseModel):
    ref: str
    sku: str
    eta: Optional[date]
    qty: int


class OrderLineModelRequestModel(AllocationSchemaDTO):
    """Order line schema request model."""
