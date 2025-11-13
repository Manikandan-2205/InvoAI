
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.services.vendor_service import VendorService
from app.core.result import Result

client = TestClient(app)

@pytest.fixture
def mock_vendor_service():
    with patch('app.api.v1.vendor_routes_v1.get_vendor_service') as mock:
        service_instance = MagicMock(spec=VendorService)
        mock.return_value = service_instance
        yield service_instance

def test_get_all_vendors_success(mock_vendor_service):
    # Arrange
    mock_vendors = [{"id": 1, "name": "Test Vendor"}]
    mock_vendor_service.get_all_vendors.return_value = Result.success(data=mock_vendors)

    # Act
    response = client.get("/api/v1/vendor/")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is True
    assert response_data["data"] == mock_vendors
    mock_vendor_service.get_all_vendors.assert_called_once()

def test_get_all_vendors_failure(mock_vendor_service):
    # Arrange
    mock_vendor_service.get_all_vendors.return_value = Result.error(message="Failed to fetch vendors")

    # Act
    response = client.get("/api/v1/vendor/")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is False
    assert response_data["message"] == "Failed to fetch vendors"
    mock_vendor_service.get_all_vendors.assert_called_once()
