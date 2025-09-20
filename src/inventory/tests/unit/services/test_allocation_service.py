from typing import List

import pytest
from sqlalchemy.exc import NoResultFound

from src.inventory.domain.batch import BatchModel
from src.inventory.services.batch_service import BatchService, OutOfStock
from src.inventory.services.schemas.allocations_dto import AllocationSchemaDTO
from src.inventory.tests.unit.services.conftest import FakeUoW
from src.orders.domain.order_line_model import OrderLineModel


@pytest.fixture(name="order_line")
def get_order_line() -> AllocationSchemaDTO:
    return AllocationSchemaDTO(order_id="1", sku="sku1", qty=5)


def test_add_batch(uow: FakeUoW, batch_service: BatchService):
    # act
    batch_service.add_batch("ref1", "sku1", qty=10)
    # assert
    assert uow.committed is True


def test_get_batche_by_ref(batch_service: BatchService):
    # arrange
    ref = "ref1"
    batch_service.add_batch("ref1", "sku1", qty=10)
    # act
    res = batch_service.get_batche_by_ref("ref1")
    # assert
    assert isinstance(res, BatchModel)
    assert res.reference == ref


def test_get_batche_by_ref_not_found(batch_service: BatchService):
    # act &  assert
    with pytest.raises(NoResultFound):
        batch_service.get_batche_by_ref("ref1")


def test_get_batches(batch_service: BatchService):
    # arrange
    batch_service.add_batch("ref1", "sku1", qty=10)
    batch_service.add_batch("ref2", "sku2", qty=10)
    # act
    res = batch_service.get_batches()
    # assert
    assert isinstance(res, List)
    assert len(res) == 2


def test_get_batches_returns_empty_list(batch_service: BatchService):
    # act
    res = batch_service.get_batches()
    # assert
    assert res == []


def test_delete_batch(uow: FakeUoW, batch_service: BatchService):
    # arrange
    assert uow.committed is False
    ref = "ref1"
    batch_service.add_batch(ref, "sku1", qty=10)
    # act
    batch_service.delete_batch(ref)
    # assert
    assert uow.committed is True
    with pytest.raises(NoResultFound):
        batch_service.get_batche_by_ref(ref)


def test_delete_batch_when_not_found(batch_service: BatchService):
    # act &  assert
    with pytest.raises(NoResultFound):
        batch_service.delete_batch("ref1")


def test_allocate_can_allocate(
    order_line: AllocationSchemaDTO, uow: FakeUoW, batch_service: BatchService
):
    # arrange
    expected_ref = "ref3"
    assert uow.committed is False
    for i in range(1, 4):
        batch_service.add_batch(f"ref{i}", order_line.sku, qty=i * 2)

    # act
    res = batch_service.allocate(order_line)

    # assert
    assert uow.committed is True
    assert res == (expected_ref, "1")

    batch = batch_service.get_batche_by_ref(res[0])
    assert len(batch.allocations) == 1
    assert OrderLineModel(**order_line.model_dump()) in batch.allocations
    assert batch.available_quantity == 1
    assert batch._purchased_quantity == 6
    assert batch.allocated_quantity == 5


def test_allocate_when_out_of_stock(
    order_line: AllocationSchemaDTO, uow: FakeUoW, batch_service: BatchService
):
    # arrange
    batch_service.add_batch("ref1", order_line.sku, qty=2)
    # act & assert
    with pytest.raises(OutOfStock):
        batch_service.allocate(order_line)


def test_deallocate(
    order_line: AllocationSchemaDTO, uow: FakeUoW, batch_service: BatchService
):
    # arrange
    ref = "ref1"
    batch_service.add_batch(ref, order_line.sku, qty=10)
    batch_service.allocate(order_line)
    batch = batch_service.get_batche_by_ref(ref)
    assert len(batch.allocations) == 1
    assert OrderLineModel(**order_line.model_dump()) in batch.allocations

    # act
    batch_service.deallocate(order_id=order_line.order_id, batch_reference=ref)

    # assert
    batch = batch_service.get_batche_by_ref(ref)
    assert len(batch.allocations) == 0
