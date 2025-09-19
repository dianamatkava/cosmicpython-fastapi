from contextlib import nullcontext

import pytest
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from src.register.domain.product_model import ProductModel
from src.orders.adapters.repository import OrderLineRepository
from src.orders.domain.order_line_model import OrderLineModel


@pytest.fixture(name="order_line")
def create_order_line(session: Session, product: ProductModel) -> OrderLineModel:
    order_line = OrderLineModel(order_id="order1", sku="RED_CHAIR", qty=10)
    session.add(order_line)
    session.commit()
    return order_line


def test_order_line_repository_get(
    session: Session,
    order_line: OrderLineModel,
    order_line_repository: OrderLineRepository,
):
    # act
    order_line = order_line_repository.get(id=order_line.id)

    # assert
    assert order_line.id == order_line.id
    assert order_line.order_id == order_line.order_id
    assert order_line.sku == order_line.sku
    assert order_line.qty == order_line.qty


def test_order_line_repository_get_not_found(
    order_line_repository: OrderLineRepository,  # placeholder
):
    # act & assert
    with pytest.raises(NoResultFound):
        order_line_repository.get(id=99)


def test_order_line_repository_list(
    session: Session, order_line_repository: OrderLineRepository
):
    # arrange
    session.add(OrderLineModel(order_id="order1", sku="RED_CHAIR", qty=10))
    session.add(OrderLineModel(order_id="order1", sku="BUE_CHAIR", qty=5))

    # act
    order_lines = order_line_repository.list()

    # assert
    assert len(order_lines) == 2
    assert ["order1"] * 2 == sorted([order_line.order_id for order_line in order_lines])
    assert ["BUE_CHAIR", "RED_CHAIR"] == sorted(
        [order_line.sku for order_line in order_lines]
    )


def test_order_line_repository_list_when_empty(
    order_line_repository: OrderLineRepository,
):
    order_lines = order_line_repository.list()
    assert order_lines == []


def test_order_line_repository_create(
    session: Session, order_line_repository: OrderLineRepository
):
    order_line_repository.add(
        OrderLineModel(order_id="order1", sku="RED_CHAIR", qty=10)
    )
    assert session.query(OrderLineModel).filter_by(order_id="order1").one()


def test_order_line_repository_delete(
    session: Session, order_line_repository: OrderLineRepository
):
    # arrange
    to_delete = OrderLineModel(order_id="order1", sku="RED_CHAIR", qty=10)
    session.add(OrderLineModel(order_id="order1", sku="WHITE_CHAIR", qty=5))
    session.add(to_delete)
    session.flush()

    # act
    order_line_repository.delete(id=to_delete.id)

    # assert
    products = session.query(OrderLineModel).all()
    assert len(products) == 1
    assert products[0].sku == "WHITE_CHAIR"


def test_order_line_repository_delete_when_not_found(
    session: Session, order_line_repository: OrderLineRepository
):
    with nullcontext():
        order_line_repository.delete(id=99)
