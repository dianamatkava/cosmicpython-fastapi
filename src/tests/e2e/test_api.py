from datetime import datetime
import requests
import factory
from sqlmodel import Session
from starlette import status

from src.app import AppSettings
from src.domain import model
from src.routes.models.allocations import AllocationsAllocateIn


class OrderLineFactory(factory.Factory):
    class Meta:
        model = model.OrderLineModel

    sku = factory.Faker('uuid4')
    qty = factory.Faker('random_int', min=1, max=100)
    order_id = factory.Faker('uuid4')


class BatchFactory(factory.Factory):
    class Meta:
        model = model.BatchModel

    reference = factory.Faker('uuid4')
    eta = factory.Faker('date_between', start_date='-30d', end_date='+30d')


def test_api_returns_allocation(session: Session):
    sku = "BLUE_VASE"
    batch_1 = model.BatchModel('batch1', sku=sku, eta=datetime.strptime("2011-01-01", "%Y-%m-%d"), qty=10)
    batch_2 = model.BatchModel('batch1', sku=sku, eta=datetime.strptime("2011-01-10", "%Y-%m-%d"), qty=10)

    order_line_1 = model.OrderLineModel("order_1", sku=sku, qty=10)
    order_line_2 = model.OrderLineModel("order_2", sku=sku, qty=10)

    session.add(batch_1)
    session.add(batch_2)
    session.commit()

    res = requests.post(f"{AppSettings.BASE_APP_URL}/allocate", json=AllocationsAllocateIn(order_line=order_line_1).model_dump_json())

    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["batch_reference"] == batch_1.reference

