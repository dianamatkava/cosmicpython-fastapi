from sqlmodel import Session

from src.adapters.repository import SqlAlchemyRepository
from src.domain import model


def test_repository_can_save_a_batch(session: Session, sql_repository: SqlAlchemyRepository):
    product = model.ProductModel(sku="RUSTY-SOAPDISH", name="Rusty SO")
    batch = model.BatchModel("batch1", product, 100, eta=None)

    sql_repository.add(batch)
    session.commit()

    rows = session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    )
    assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]