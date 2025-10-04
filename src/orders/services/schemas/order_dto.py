from typing import Optional

from pydantic import BaseModel

from src.orders.adapters.orm import OrderStatus


class OrderSchemaDTO(BaseModel):
    id: Optional[int] = None
    status: OrderStatus = None
