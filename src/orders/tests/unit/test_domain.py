from contextlib import nullcontext

import pytest

from src.orders.domain.order_line_model import OrderLineModel


def test_init_object_ok():
    with nullcontext():
        OrderLineModel(id=1, order_id="order1", sku="RED_CHAIR", qty=10)
        OrderLineModel(order_id="order1", sku="RED_CHAIR", qty=10)


def test_init_object_qty_can_not_be_lower_then_1():
    with pytest.raises(ValueError):
        OrderLineModel(order_id="order1", sku="RED_CHAIR", qty=0)

    with pytest.raises(ValueError):
        OrderLineModel(order_id="order1", sku="RED_CHAIR", qty=-1)
