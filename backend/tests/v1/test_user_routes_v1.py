
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.services.user_service import UserService
from app.core.result import Result

client = TestClient(app)

@pytest.fixture
def mock_user_service():
    with patch('app.api.v1.user_routes_v1.get_user_service') as mock:
        service_instance = MagicMock(spec=UserService)
        mock.return_value = service_instance
        yield service_instance

def test_get_all_users_success(mock_user_service):
    # Arrange
    mock_users = [{"id": 1, "username": "testuser"}]
    mock_user_service.get_all_users.return_value = Result.success(data=mock_users)

    # Act
    response = client.get("/api/v1/user/get-all-user-details")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is True
    assert response_data["data"] == mock_users
    mock_user_service.get_all_users.assert_called_once()

def test_get_all_users_failure(mock_user_service):
    # Arrange
    mock_user_service.get_all_users.return_value = Result.error(message="Failed to fetch users")

    # Act
    response = client.get("/api/v1/user/get-all-user-details")

    # Assert
    assert response.status_code == 200  # The API returns a 200 but with success=False
    response_data = response.json()
    assert response_data["success"] is False
    assert response_data["message"] == "Failed to fetch users"
    mock_user_service.get_all_users.assert_called_once()
