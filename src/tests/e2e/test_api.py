from datetime import datetime

from sqlmodel import Session
from starlette import status
from starlette.testclient import TestClient

from src.app import AppSettings
from src.domain import model
from src.routes.schemas.allocations import AllocationsAllocateIn


def test_api_returns_allocation(session: Session, client: TestClient):
    sku = "BLUE_VASE"
    batch_1 = model.BatchModel('batch1', sku=sku, eta=datetime.strptime("2011-01-01", "%Y-%m-%d"), qty=10)
    batch_2 = model.BatchModel('batch1', sku=sku, eta=datetime.strptime("2011-01-10", "%Y-%m-%d"), qty=10)

    session.add(batch_1)
    session.add(batch_2)
    session.commit()

    order_line_1 = AllocationsAllocateIn(order_id="order_1", sku=sku, qty=10)
    order_line_2 = AllocationsAllocateIn(order_id="order_2", sku=sku, qty=10)

    res = client.post(f"{AppSettings.BASE_APP_URL}/allocations", json=order_line_1.model_dump_json())

    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["batch_reference"] == batch_1.reference

