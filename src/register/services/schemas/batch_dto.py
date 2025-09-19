from datetime import date

from pydantic import BaseModel


class BatchSchemaDTO(BaseModel):
    reference: str
    sku: str
    eta: date | None
    available_quantity: int
    allocated_quantity: int
