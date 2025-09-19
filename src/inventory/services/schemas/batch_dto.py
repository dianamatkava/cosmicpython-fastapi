from datetime import date
from typing import Any

from pydantic import BaseModel


class BatchSchemaDTO(BaseModel):
    reference: str
    sku: str
    eta: date | None
    available_quantity: int
    allocations: Any
