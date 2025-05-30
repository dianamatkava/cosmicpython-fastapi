from datetime import date

from src.domain.batch_domain_model import BatchModel, OrderLineModel


def make_batch_and_line(batch_qty: int, line_qty: int, batch_eta: date = date.today()):
    batch = BatchModel('1', "BLUE-VASE", qty=batch_qty, eta=batch_eta)
    order_line = OrderLineModel('1', "BLUE-VASE", qty=line_qty)

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
    batch = BatchModel('1', "BLUE-VASE", qty=20, eta=date.today())
    order_line = OrderLineModel("1", "WHITE-CHAIR", qty=2)

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


def test_deallocate():
    batch, order_line = make_batch_and_line(20, 2)
    batch.allocate(order_line)
    batch.deallocate(order_line)
    assert batch.available_quantity == 20
