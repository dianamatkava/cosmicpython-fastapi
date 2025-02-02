from sqlmodel import Session
from sqlalchemy import text
from src.adapters.repository import SqlAlchemyRepository
from src.domain import model
from src.domain.model import OrderLineModel


def test_repository_can_save_a_batch(session: Session, sql_repository: SqlAlchemyRepository):
    batch = model.BatchModel("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    sql_repository.add(batch)
    session.commit()

    rows = session.execute(
        text('SELECT reference, sku, _purchased_quantity, eta FROM batches')
    )
    assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]


def test_can_save_batch_with_allocations(session: Session, sql_repository: SqlAlchemyRepository):
    # arrange
    order_line_1 = model.OrderLineModel('1', 'BLUE-VASE', 50)
    order_line_2 = model.OrderLineModel('2', 'BLUE-VASE', 15)
    batch = model.BatchModel('batch1', 'BLUE-VASE', 200, None)
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


def test_repository_can_get_a_batch(session: Session, sql_repository: SqlAlchemyRepository):
    batch = model.BatchModel("batch1", "RUSTY-SOAPDISH", 100, eta=None)
    batch2 = model.BatchModel("batch2", "BLUE_VASE", 50, eta=None)

    sql_repository.add(batch)
    sql_repository.add(batch2)
    session.commit()

    row = sql_repository.get("batch1")
    assert row is batch


def test_repository_can_list_batches(session: Session, sql_repository: SqlAlchemyRepository):
    batch = model.BatchModel("batch1", "RUSTY-SOAPDISH", 100, eta=None)
    batch2 = model.BatchModel("batch2", "BLUE_VASE", 50, eta=None)

    sql_repository.add(batch)
    sql_repository.add(batch2)
    session.commit()

    rows = sql_repository.list()
    assert len(rows) == 2
    assert batch in rows
    assert batch2 in rows

