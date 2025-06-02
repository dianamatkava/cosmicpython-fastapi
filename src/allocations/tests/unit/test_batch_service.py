from typing import List, Set, Optional, Type

import pytest
from sqlalchemy.exc import NoResultFound

from src.allocations.adapters.repository import AbstractRepository
from src.allocations.adapters.uow import AbstractUnitOfWork
from src.allocations.domain import batch_domain_model as domain
from src.allocations.services.schemas import AllocationSchemaDTO
from src.allocations.services.batch_service import BatchService, OutOfStock


class FakeBatchRepository(AbstractRepository):
    db: Set[domain.BatchModel] = set()

    def __init__(self, initial_db: Optional[Set] = None):
        self.db = initial_db if initial_db else set()

    def add(self, batch: domain.BatchModel) -> None:
        self.db.add(batch)

    def get(self, reference: str) -> domain.BatchModel:
        try:
            return next(batch for batch in self.db if batch.reference == reference)
        except StopIteration:
            raise NoResultFound

    def delete(self, reference: str) -> None:
        try:
            batch_to_delete = next(
                batch for batch in self.db if batch.reference == reference
            )
        except StopIteration:
            raise NoResultFound
        self.db.remove(batch_to_delete)

    def list(self) -> List[domain.BatchModel]:
        return list(self.db)


class FakeUoW(AbstractUnitOfWork):
    committed: bool | None = False
    batch_repo: Type[AbstractRepository]  # type: ignore

    def __init__(
        self, batch_repo: Type[AbstractRepository] = FakeBatchRepository
    ) -> None:
        self.batch_repo_cls: Type[AbstractRepository] = batch_repo
        self.batch_repo: AbstractRepository
        self.batch_repo = self.batch_repo_cls  # type: ignore

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.committed = None


@pytest.fixture(name="uow")
def get_fake_uow(batch_repo: Type[AbstractRepository]):
    return FakeUoW(batch_repo=batch_repo)


@pytest.fixture(name="batch_repo")
def get_batch_repo():
    return FakeBatchRepository()


@pytest.fixture(name="batch_service")
def get_batch_service(uow: FakeUoW):
    return BatchService(uow=uow)


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
    assert isinstance(res, domain.BatchModel)
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
    assert res == expected_ref

    batch = batch_service.get_batche_by_ref(res)
    assert len(batch.allocations) == 1
    assert domain.OrderLineModel(**order_line.model_dump()) in batch.allocations
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
    assert domain.OrderLineModel(**order_line.model_dump()) in batch.allocations

    # act
    batch_service.deallocate(order_id=order_line.order_id, batch_reference=ref)

    # assert
    batch = batch_service.get_batche_by_ref(ref)
    assert len(batch.allocations) == 0
