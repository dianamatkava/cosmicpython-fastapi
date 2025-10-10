from typing import Optional

from pydantic import BaseModel


class OrderLineSchemaDTO(BaseModel):
    id: Optional[int] = None
    order_id: Optional[int] = None
    sku: str
    qty: int
