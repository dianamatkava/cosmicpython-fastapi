from dataclasses import dataclass
from datetime import date
from typing import NewType, Set, Optional


class ProductModel:
    sku: str
    name: str

    def __init__(self, sku: str, name: str) -> None:
        self.sku = sku
        self.name = name


@dataclass(frozen=True)
class OrderLineModel:
    # value object
    # dataclasses or named tuples are idempotent

    order_id: str
    product: ProductModel  # FK
    qty: int

    def __str__(self):
        return f'{self.qty} units of {self.product.name}'

# new OrderLine() == new OrderLine()  // true


class CustomerModel:
    id: int
    address: str


class OrderModel:
    customer: CustomerModel | None  # FK
    ref: str
    order_line: list

    def __init__(self, ref: str, order_line: list, customer: CustomerModel = None):
        self.ref = ref
        self.order_line = order_line
        self.customer = customer


class BatchModel:
    ref: str
    product: ProductModel
    eta: date | None
    _purchased_quantity: int  # initial quantity
    _allocations: Set[OrderLineModel]

    def __init__(self, ref: str, product: ProductModel, qty: int, eta: Optional[date]):
        self.ref = ref
        self.product = product
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()

    def __str__(self):
        return f'{self.available_quantity} {self.product.name}'

    # Batch is entity object
    # Entity described by ref
    # batch entity is not described by its values, likewise value object
    def __eq__(self, other):
        if not isinstance(other, BatchModel):
            return False
        return other.ref == self.ref

    def __hash__(self):
        return hash(self.ref)

    def __gt__(self, other: 'BatchModel') -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    @property
    def allocated_quantity(self) -> int:
        return sum([allocation.qty for allocation in self._allocations])

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def allocate(self, order_line: OrderLineModel):
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    def can_allocate(self, order_line: OrderLineModel) -> bool:
        if self.product == order_line.product and self.available_quantity >= order_line.qty:
            return True
        return False

    def deallocate(self, order_line: OrderLineModel):
        if self.can_deallocate(order_line):
            self._allocations.remove(order_line)

    def can_deallocate(self, order_line: OrderLineModel) -> bool:
        if order_line in self._allocations:
            return True
        return False
