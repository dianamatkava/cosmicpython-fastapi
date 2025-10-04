from dataclasses import dataclass
from typing import Optional, Union, List

from src.inventory.domain.commands import Command
from src.orders.adapters.orm import OrderStatus
from src.orders.domain.events import OrderCreated
from src.shared.domain.events import Event


# TODO: AT-710 Excellent candidate for root aggregate
@dataclass(unsafe_hash=True)
class OrderModel:
    id: int
    status: OrderStatus
    events: List[Union[Event, Command]]

    def __init__(self, id: Optional[int] = None):
        self.id = id
        self.events = []

    def created(self) -> None:
        if not self.id:
            raise ValueError(
                "Order ID must be assigned before recording the 'created' event."
            )

        self.events.append(
            OrderCreated(
                order_id=self.id, order_status=self.status, aggregate_id=str(self.id)
            )
        )
