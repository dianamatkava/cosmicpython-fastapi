from datetime import date, timedelta
import pytest

from src.allocation.services.batch_service import BatchService, OutOfStock
from src.allocation.domain.model import ProductModel, BatchModel, OrderLineModel


def make_batch_and_line(batch_qty: int, line_qty: int, batch_eta: date = date.today()):
    product = ProductModel('1', "BLUE-VASE")
    batch = BatchModel('1', product, qty=batch_qty, eta=batch_eta)
    order_line = OrderLineModel('1', product, qty=line_qty)

    return batch, order_line


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, order_line = make_batch_and_line(20, 2)
    batch.allocate(order_line)
    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    batch, order_line = make_batch_and_line(20, 2)
    assert batch.can_allocate(order_line) is True


def test_cannot_allocate_if_available_smaller_than_required():
    batch, order_line = make_batch_and_line(20, 22)
    assert batch.can_allocate(order_line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, order_line = make_batch_and_line(20, 20)
    assert batch.can_allocate(order_line) is True


def test_can_not_allocate_if_sku_dont_match():
    product = ProductModel(1, "BLUE-VASE")
    product_2 = ProductModel(2, "WHITE-CHAIR")
    batch = BatchModel('1', product, qty=20, eta=date.today())
    order_line = OrderLineModel(1, product_2, qty=2)

    assert batch.can_allocate(order_line) is False


def test_allocation_is_idempotent():
    batch, order_line = make_batch_and_line(20, 2)
    batch.allocate(order_line)
    batch.allocate(order_line)
    assert batch.available_quantity == 18


def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line(20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20


def test_deallocate_allocated_lines():
    batch, order_line = make_batch_and_line(20, 2)
    batch.allocate(order_line)
    batch.deallocate(order_line)
    assert batch.available_quantity == 20


def test_prefers_current_stock_batches_to_shipments(batch_service):
    product = ProductModel("1", "BLUE-VASE")
    in_stock_batch = BatchModel("1", product, qty=100, eta=None)
    shipment_batch = BatchModel("2", product, qty=100, eta=date.today())
    line = OrderLineModel(1, product, 10)

    batch_service.allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches(batch_service: BatchService):
    product = ProductModel("1", "BLUE-VASE")
    earlier = BatchModel("1", product, qty=100, eta=date.today())
    medium = BatchModel("1", product, qty=100, eta=date.today() + timedelta(days=2))
    latest = BatchModel("2", product, qty=100, eta=date.today() + timedelta(days=4))
    line = OrderLineModel('1', product, 10)

    batch_service.allocate(line, [latest, medium, earlier])

    assert earlier.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref(batch_service: BatchService):
    product = ProductModel("1", "BLUE-VASE")
    in_stock_batch = BatchModel("1", product, qty=100, eta=None)
    shipment_batch = BatchModel("2", product, qty=100, eta=date.today())
    line = OrderLineModel('1', product, 10)

    allocation = batch_service.allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.ref


def test_raises_out_of_stock_exception_if_cannot_allocate(batch_service: BatchService):
    product = ProductModel("1", "BLUE-VASE")
    batch = BatchModel("1", product, qty=10, eta=None)
    order_line = OrderLineModel('1', product, 10)

    batch_service.allocate(order_line, [batch])

    with pytest.raises(OutOfStock):
        batch_service.allocate(OrderLineModel('1', product, 1), [batch])