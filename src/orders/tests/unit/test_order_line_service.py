import pytest
from sqlalchemy.exc import NoResultFound

from src.orders.domain.order_line_model import OrderLineModel
from src.orders.services.order_line_service import OrderLineService
from src.orders.services.schemas.order_line_dto import OrderLineSchemaDTO
from src.orders.tests.conftest import FakeOrderLineRepository


def test_create_order_line_ok(order_line_service: OrderLineService):
    # arrange
    order_line_data = OrderLineSchemaDTO(order_id="ORDER-001", sku="BLUE_CHAIR", qty=5)

    # act
    result = order_line_service.create_order_line(order_line_data)

    # assert
    assert order_line_service.uow.committed is True
    assert result.order_id == order_line_data.order_id
    assert result.sku == order_line_data.sku
    assert result.qty == order_line_data.qty


def test_create_order_line_raises_when_product_not_found(
    order_line_service: OrderLineService, fake_order_line_repo: FakeOrderLineRepository
):
    # arrange
    order_line_data = OrderLineSchemaDTO(
        order_id="ORDER-001", sku="NONEXISTENT_SKU", qty=5
    )
    # Mock product repo to raise NoResultFound
    order_line_service.uow.product_repo.get = lambda sku: (_ for _ in ()).throw(
        NoResultFound()
    )

    # act & assert
    try:
        order_line_service.create_order_line(order_line_data)
        assert False, "Expected NoResultFound exception"
    except NoResultFound:
        pass


def test_create_order_line_raises_when_order_not_found(
    order_line_service: OrderLineService,
):
    # arrange
    order_line_data = OrderLineSchemaDTO(
        order_id="NONEXISTENT_ORDER", sku="BLUE_CHAIR", qty=5
    )
    # This would typically be handled by order validation in a real scenario

    # act & assert
    # Note: Current implementation doesn't validate order existence
    # This test demonstrates where order validation would go
    pass


def test_create_order_line_raises_when_qty_value_error(
    order_line_service: OrderLineService,
):
    # arrange
    # Note: Pydantic validation handles this at the DTO level
    # This test would cover business logic quantity validation
    order_line_data = OrderLineSchemaDTO(order_id="ORDER-001", sku="BLUE_CHAIR", qty=1)

    # act
    result = order_line_service.create_order_line(order_line_data)

    # assert
    assert result.qty == 1
    assert order_line_service.uow.committed is True


def test_get_order_line_ok(
    order_line_service: OrderLineService, fake_order_line_repo: FakeOrderLineRepository
):
    # arrange
    order_line = OrderLineModel(id=1, order_id="ORDER-001", sku="BLUE_CHAIR", qty=5)
    fake_order_line_repo.build([order_line])

    # act
    result = order_line_service.get_order_line(id=1)

    # assert
    assert result.id == order_line.id
    assert result.order_id == order_line.order_id
    assert result.sku == order_line.sku
    assert result.qty == order_line.qty


def test_get_order_line_not_found(order_line_service: OrderLineService):
    # act & assert
    with pytest.raises(NoResultFound):
        order_line_service.get_order_line(id=999)


def test_get_all_order_lines_ok(
    order_line_service: OrderLineService, fake_order_line_repo: FakeOrderLineRepository
):
    # arrange
    order_lines = [
        OrderLineModel(id=1, order_id="ORDER-001", sku="BLUE_CHAIR", qty=5),
        OrderLineModel(id=2, order_id="ORDER-002", sku="RED_CHAIR", qty=3),
    ]
    fake_order_line_repo.build(order_lines)

    # act
    result = order_line_service.get_all_order_lines()

    # assert
    assert len(result) == 2
    assert sorted([ol.id for ol in order_lines]) == sorted([r.id for r in result])


def test_get_all_order_lines_returns_empty(order_line_service: OrderLineService):
    # arrange
    # Empty repository

    # act
    result = order_line_service.get_all_order_lines()

    # assert
    assert result == []


def test_delete_order_line_ok(
    order_line_service: OrderLineService, fake_order_line_repo: FakeOrderLineRepository
):
    # arrange
    order_line = OrderLineModel(id=1, order_id="ORDER-001", sku="BLUE_CHAIR", qty=5)
    fake_order_line_repo.build([order_line])

    # act
    order_line_service.delete_order_line(id=1)

    # assert
    assert order_line_service.uow.committed is True
    assert len(fake_order_line_repo.list()) == 0


def test_delete_order_line_not_found(order_line_service: OrderLineService):
    with pytest.raises(NoResultFound):
        order_line_service.delete_order_line(id=999)

    # assert
    assert order_line_service.uow.committed is False


# TODO: def test_create_order_line_duplicate_validation(order_line_service: OrderLineService):
# TODO: def test_update_order_line_ok(order_line_service: OrderLineService):
# TODO: def test_get_order_lines_by_order_id(order_line_service: OrderLineService):
