from typing import List

from models.allocation import OrderLineModel, BatchModel


class OutOfStock(Exception):
    """OutOfStock Exception"""


class BatchService:

    @staticmethod
    def allocate(order_line: OrderLineModel, batches: List[BatchModel]) -> str:
        try:
            batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
        except StopIteration as e:
            print(f"Error allocating batches: {e}")
            raise OutOfStock() from e

        batch.allocate(order_line)
        return batch.ref
