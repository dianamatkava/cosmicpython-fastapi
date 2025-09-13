from typing import Optional

from pydantic import BaseModel


class OrderLineSchemaDTO(BaseModel):
    id: Optional[int] = None
    order_id: str
    sku: str
    qty: int
