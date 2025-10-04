from typing import Annotated

from pydantic import Field

from src.orders.adapters.orm import OrderStatus
from src.orders.routes.schemas.shared import BaseResponseModel


class OrderResponseModel(BaseResponseModel):
    id: Annotated[int, Field(description="Order ID")]
    status: Annotated[OrderStatus, Field(description="Order status")]
