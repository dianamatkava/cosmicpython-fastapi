from datetime import date

from src.inventory.domain.batch import BatchModel
from src.inventory.services.batch_service import BatchService
from src.inventory.services.schemas.batch_dto import BatchSchemaDTO
from src.inventory.tests.unit.services.conftest import FakeBatchRepository


def test_add_batch(batch_service: BatchService):
    # arrange
    batch = BatchSchemaDTO(ref="BATCH-001", sku="BLUE_CHAIR", qty=20, eta=date(2024, 1, 15))

    # act
    batch_service.add_batch(batch)

    # assert
    assert batch_service.uow.committed is True


def test_add_batch_with_optional_eta(batch_service: BatchService):
    # arrange
    batch = BatchSchemaDTO(ref="BATCH-001", sku="BLUE_CHAIR", qty=20)

    # act
    batch_service.add_batch(batch)

    # assert
    assert batch_service.uow.committed is True


def test_get_batch_by_ref_returns_batch(
    batch_service: BatchService, batch_repo: FakeBatchRepository
):
    # arrange
    batch = BatchModel(
        ref="BATCH-001", sku="BLUE_CHAIR", eta=date(2024, 1, 15), qty=20
    )
    batch_repo.build([batch])

    # act
    res = batch_service.get_batche_by_ref("BATCH-001")

    # assert
    assert res.ref == batch.reference
    assert res.sku == batch.sku
    assert res.qty == batch._purchased_quantity
    assert res.eta == batch.eta


def test_get_all_batches(
    batch_service: BatchService, batch_repo: FakeBatchRepository
):
    # arrange
    batches = [
        BatchModel(
            ref="BATCH-001", sku="BLUE_CHAIR", eta=date(2024, 1, 15), qty=20
        ),
        BatchModel(
            ref="BATCH-002", sku="RED_CHAIR", eta=date(2024, 1, 20), qty=15
        ),
    ]
    batch_repo.build(batches)

    # act
    result = batch_service.get_batches()

    # assert
    assert len(result) == 2
    assert sorted([batch.reference for batch in batches]) == sorted(
        [b.ref for b in result]
    )


def test_get_all_batches_returns_empty_list(batch_service: BatchService):
    result = batch_service.get_batches()
    assert result == []


def test_delete_batch(
    batch_service: BatchService, batch_repo: FakeBatchRepository
):
    batch = BatchModel(
        ref="BATCH-001", sku="BLUE_CHAIR", eta=date(2024, 1, 15), qty=20
    )
    batch_repo.build([batch])

    batch_service.delete_batch("BATCH-001")

    assert batch_service.uow.committed is True
    assert len(batch_repo.list()) == 0


# TODO: def test_get_batch_not_found(batch_service: BatchService):
# TODO: def test_delete_batch_not_found(batch_service: BatchService):
