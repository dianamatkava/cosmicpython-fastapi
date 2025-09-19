from sqlalchemy import text
from sqlmodel import Session

from src.inventory.adapters.repository import ProductStockRepository
from src.inventory.domain import product_model as domain


def test_repository_can_save_a_batch(
    session: Session, sql_repository: ProductStockRepository
):
    batch = domain.BatchModel("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    sql_repository.add(batch)
    session.commit()

    rows = session.execute(
        text("SELECT reference, sku, _purchased_quantity, eta FROM batches")
    )
    assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]


def test_can_save_batch_with_allocations(
    session: Session, sql_repository: ProductStockRepository
):
    # arrange
    order_line_1 = domain.OrderLineModel("1", "BLUE-VASE", 50)
    order_line_2 = domain.OrderLineModel("2", "BLUE-VASE", 15)
    batch = domain.BatchModel("batch1", "BLUE-VASE", 200, None)
    batch.allocate(order_line_1)
    batch.allocate(order_line_2)

    assert len(batch._allocations) == 2

    # act
    sql_repository.add(batch)
    session.commit()

    # assert
    row = sql_repository.get("batch1")
    assert row is batch
    assert row._allocations == {order_line_1, order_line_2}


def test_can_get_batch_with_allocations(
    session: Session, sql_repository: ProductStockRepository
):
    # arrange
    session.execute(
        text(
            "INSERT INTO order_lines (sku, qty, order_id) VALUES (:sku, :qty, :order_id)"
        ),
        {"sku": "BLUE_VASE", "qty": 25, "order_id": "1"},
    )
    session.execute(
        text(
            "INSERT INTO batches (reference, sku, _purchased_quantity, eta) VALUES (:reference, :sku, :_purchased_quantity, :eta)"
        ),
        {
            "reference": "batch1",
            "sku": "BLUE_VASE",
            "_purchased_quantity": 25,
            "eta": None,
        },
    )

    [[batch_id]] = session.execute(
        text("SELECT b.id FROM batches b WHERE reference=:reference"),
        {"reference": "batch1"},
    )
    [[order_line_id]] = session.execute(
        text("SELECT o.id FROM order_lines o WHERE order_id=:order_id"),
        {"order_id": "1"},
    )

    session.execute(
        text(
            "INSERT INTO inventory (orderline_id, batch_id) VALUES (:orderline_id, :batch_id)"
        ),
        {"orderline_id": order_line_id, "batch_id": batch_id},
    )

    # act
    batch = sql_repository.get("batch1")
    expected_batch = domain.BatchModel("batch1", "BLUE_VASE", 25, None)

    # assert
    assert batch.sku == expected_batch.sku
    assert batch.reference == expected_batch.reference
    assert batch._purchased_quantity == expected_batch._purchased_quantity
    assert batch._allocations == {domain.OrderLineModel("1", "BLUE_VASE", 25)}


def test_repository_can_get_a_batch(
    session: Session, sql_repository: ProductStockRepository
):
    batch = domain.BatchModel("batch1", "RUSTY-SOAPDISH", 100, eta=None)
    batch2 = domain.BatchModel("batch2", "BLUE_VASE", 50, eta=None)

    sql_repository.add(batch)
    sql_repository.add(batch2)
    session.commit()

    row = sql_repository.get("batch1")
    assert row is batch


def test_repository_can_list_batches(
    session: Session, sql_repository: ProductStockRepository
):
    batch = domain.BatchModel("batch1", "RUSTY-SOAPDISH", 100, eta=None)
    batch2 = domain.BatchModel("batch2", "BLUE_VASE", 50, eta=None)

    sql_repository.add(batch)
    sql_repository.add(batch2)
    session.commit()

    rows = sql_repository.list()
    assert len(rows) == 2
    assert batch in rows
    assert batch2 in rows
