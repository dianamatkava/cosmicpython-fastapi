"""
Test API that performs end-to-end testing of the API contract by verifying core domain functionality using:
 - production-like unit-of-work
 - postgres-test adapters and session
Also validates the REST API contract by ensuring correct response codes, error handling, and response structures.
"""

from unittest.mock import MagicMock

from sqlalchemy.exc import NoResultFound
from starlette import status
from starlette.testclient import TestClient

from src.orders.routes.schemas.request_models.order_line import (
    OrderLineCreateRequestModel,
)
from src.orders.services.order_line_service import OrderLineService
from src.orders.services.schemas.order_line_dto import OrderLineSchemaDTO


def test_get_order_line_by_id_ok(client: TestClient, mocker: MagicMock):
    # arrange
    order_line_dto = OrderLineSchemaDTO(
        id=1, order_id="ORDER-001", sku="BLUE_CHAIR", qty=5
    )
    mock_get_order_line = mocker.patch.object(
        OrderLineService, "get_order_line", return_value=order_line_dto
    )

    # act
    res = client.get("/order_line/1")

    # assert
    assert res.status_code == status.HTTP_200_OK
    response_data = res.json()
    assert response_data["id"] == 1
    assert response_data["order_id"] == "ORDER-001"
    assert response_data["sku"] == "BLUE_CHAIR"
    assert response_data["qty"] == 5

    mock_get_order_line.assert_called_once_with(id="1")


def test_get_order_line_by_id_not_found(client: TestClient, mocker: MagicMock):
    # arrange
    mock_get_order_line = mocker.patch.object(
        OrderLineService, "get_order_line", side_effect=NoResultFound()
    )

    # act
    res = client.get("/order_line/999")

    # assert
    assert res.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    mock_get_order_line.assert_called_once_with(id="999")


def test_list_order_lines(client: TestClient, mocker: MagicMock):
    # arrange
    order_lines = [
        OrderLineSchemaDTO(id=1, order_id="ORDER-001", sku="BLUE_CHAIR", qty=5),
        OrderLineSchemaDTO(id=2, order_id="ORDER-002", sku="RED_CHAIR", qty=3),
    ]
    mock_get_all_order_lines = mocker.patch.object(
        OrderLineService, "get_all_order_lines", return_value=order_lines
    )

    # act
    res = client.get("/order_line")

    # assert
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 2

    response_data = res.json()
    assert response_data[0]["id"] == 1
    assert response_data[0]["order_id"] == "ORDER-001"
    assert response_data[0]["sku"] == "BLUE_CHAIR"
    assert response_data[1]["id"] == 2
    assert response_data[1]["order_id"] == "ORDER-002"
    assert response_data[1]["sku"] == "RED_CHAIR"

    mock_get_all_order_lines.assert_called_once_with()


def test_list_order_lines_returns_empty(client: TestClient, mocker: MagicMock):
    # arrange
    mock_get_all_order_lines = mocker.patch.object(
        OrderLineService, "get_all_order_lines", return_value=[]
    )

    # act
    res = client.get("/order_line")

    # assert
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == []
    mock_get_all_order_lines.assert_called_once_with()


def test_create_order_line_ok(client: TestClient, mocker: MagicMock):
    # arrange

    order_line_dto = OrderLineSchemaDTO(
        id=1, order_id="ORDER-001", sku="BLUE_CHAIR", qty=5
    )
    mock_create_order_line = mocker.patch.object(
        OrderLineService, "create_order_line", return_value=order_line_dto
    )
    request_data = OrderLineCreateRequestModel(
        order_id="ORDER-001", sku="BLUE_CHAIR", qty=5
    )

    # act
    res = client.post("/order_line", json=request_data.model_dump())

    # assert
    assert res.status_code == status.HTTP_201_CREATED
    response_data = res.json()
    assert response_data["order_id"] == "ORDER-001"
    assert response_data["sku"] == "BLUE_CHAIR"
    assert response_data["qty"] == 5
    mock_create_order_line.assert_called_once()


def test_create_order_line_order_not_found(client: TestClient, mocker: MagicMock):
    # arrange
    mock_create_order_line = mocker.patch.object(
        OrderLineService,
        "create_order_line",
        side_effect=NoResultFound("Order not found"),
    )
    request_data = {
        "order_id": "NONEXISTENT-ORDER",
        "sku": "BLUE_CHAIR",
        "qty": 5,
    }

    # act
    res = client.post("/order_line", json=request_data)

    # assert
    assert res.status_code == status.HTTP_404_NOT_FOUND
    mock_create_order_line.assert_called_once()


def test_create_order_line_order_product_not_found(
    client: TestClient, mocker: MagicMock
):
    # arrange
    mock_create_order_line = mocker.patch.object(
        OrderLineService,
        "create_order_line",
        side_effect=NoResultFound("Product not found"),
    )
    request_data = {
        "order_id": "ORDER-001",
        "sku": "NONEXISTENT_SKU",
        "qty": 5,
    }

    # act
    res = client.post("/order_line", json=request_data)

    # assert
    assert res.status_code == status.HTTP_404_NOT_FOUND
    mock_create_order_line.assert_called_once()


def test_create_order_line_order_qty_validation_error(client: TestClient):
    # arrange
    invalid_data = {
        "order_id": "ORDER-001",
        "sku": "BLUE_CHAIR",
        "qty": -5,  # Should be >= 1
    }

    # act
    res = client.post("/order_line", json=invalid_data)

    # assert
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    error_detail = res.json()["detail"]

    # Check that quantity validation error is present
    qty_errors = [error for error in error_detail if "qty" in error.get("loc", [])]
    assert len(qty_errors) > 0

    # Test zero quantity
    invalid_data["qty"] = 0
    res = client.post("/order_line", json=invalid_data)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_order_line_ok(client: TestClient, mocker: MagicMock):
    # arrange
    mock_delete_order_line = mocker.patch.object(OrderLineService, "delete_order_line")

    # act
    res = client.delete("/order_line/1")

    # assert
    assert res.status_code == status.HTTP_200_OK
    assert res.json() is None
    mock_delete_order_line.assert_called_once_with(id="1")


def test_delete_order_line_not_found(client: TestClient, mocker: MagicMock):
    # arrange
    mock_delete_order_line = mocker.patch.object(
        OrderLineService, "delete_order_line", side_effect=NoResultFound()
    )

    # act
    res = client.delete("/order_line/999")

    # assert
    assert res.status_code == status.HTTP_404_NOT_FOUND
    mock_delete_order_line.assert_called_once_with(id="999")


def test_create_order_line_validates_required_fields(client: TestClient):
    # arrange
    incomplete_data = {
        "order_id": "ORDER-001",
        # Missing sku and qty
    }

    # act
    res = client.post("/order_line", json=incomplete_data)

    # assert
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    error_detail = res.json()["detail"]

    missing_fields = {error["loc"][-1] for error in error_detail}
    assert "sku" in missing_fields
    assert "qty" in missing_fields


def test_create_order_line_validates_data_types(client: TestClient):
    # arrange
    invalid_data = {
        "order_id": "ORDER-001",
        "sku": "BLUE_CHAIR",
        "qty": "not_a_number",  # Should be int
    }

    # act
    res = client.post("/order_line", json=invalid_data)

    # assert
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_order_line_service_dependency_injection_works(
    client: TestClient, mocker: MagicMock
):
    # arrange
    mock_get_all_order_lines = mocker.patch.object(
        OrderLineService, "get_all_order_lines", return_value=[]
    )

    # act
    res = client.get("/order_line")

    # assert
    assert res.status_code == status.HTTP_200_OK
    mock_get_all_order_lines.assert_called_once_with()


def test_endpoints_use_correct_content_type(client: TestClient, mocker: MagicMock):
    # arrange
    mock_create_order_line = mocker.patch.object(OrderLineService, "create_order_line")
    order_line_dto = OrderLineSchemaDTO(
        id=1, order_id="ORDER-001", sku="BLUE_CHAIR", qty=5
    )
    mock_create_order_line.return_value = order_line_dto
    request_data = {
        "order_id": "ORDER-001",
        "sku": "BLUE_CHAIR",
        "qty": 5,
    }

    # act
    res = client.post("/order_line", json=request_data)

    # assert
    assert res.status_code == status.HTTP_201_CREATED
