import pytest
from app import app, calculate_bmi


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_calculate_bmi_function():
    """Test the BMI calculation function directly."""
    # Test normal case
    assert calculate_bmi(70, 1.75) == pytest.approx(22.86, 0.01)
    # Test another normal case
    assert calculate_bmi(80, 1.80) == pytest.approx(24.69, 0.01)
    # Test edge case with very low values
    assert calculate_bmi(45, 1.60) == pytest.approx(17.58, 0.01)
    # Test edge case with high values
    assert calculate_bmi(100, 1.90) == pytest.approx(27.70, 0.01)


def test_bmi_endpoint_success(client):
    """Test successful BMI calculation through the API."""
    # Test with normal values
    response = client.post('/calculate-bmi',
                           json={'weight': 70, 'height': 1.75})
    assert response.status_code == 200
    data = response.get_json()
    assert 'bmi' in data
    assert data['bmi'] == pytest.approx(22.86, 0.01)
    assert data['weight'] == 70
    assert data['height'] == 1.75


def test_bmi_endpoint_missing_data(client):
    """Test API response when data is missing."""
    # Test missing weight
    response = client.post('/calculate-bmi',
                           json={'height': 1.75})
    assert response.status_code == 400
    assert 'error' in response.get_json()

    # Test missing height
    response = client.post('/calculate-bmi',
                           json={'weight': 70})
    assert response.status_code == 400
    assert 'error' in response.get_json()

    # Test empty request
    response = client.post('/calculate-bmi',
                           json={})
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_bmi_endpoint_invalid_data(client):
    """Test API response with invalid data."""
    # Test negative weight
    response = client.post('/calculate-bmi',
                           json={'weight': -70, 'height': 1.75})
    assert response.status_code == 400
    assert 'error' in response.get_json()

    # Test negative height
    response = client.post('/calculate-bmi',
                           json={'weight': 70, 'height': -1.75})
    assert response.status_code == 400
    assert 'error' in response.get_json()

    # Test zero values
    response = client.post('/calculate-bmi',
                           json={'weight': 0, 'height': 1.75})
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_bmi_endpoint_non_numeric(client):
    """Test API response with non-numeric data."""
    # Test string weight
    response = client.post('/calculate-bmi',
                           json={'weight': 'invalid', 'height': 1.75})
    assert response.status_code == 400
    assert 'error' in response.get_json()

    # Test string height
    response = client.post('/calculate-bmi',
                           json={'weight': 70, 'height': 'invalid'})
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_bmi_endpoint_wrong_method(client):
    """Test API response with wrong HTTP method."""
    # Test GET request
    response = client.get('/calculate-bmi')
    assert response.status_code == 405

    # Test PUT request
    response = client.put('/calculate-bmi')
    assert response.status_code == 405

    # Test DELETE request
    response = client.delete('/calculate-bmi')
    assert response.status_code == 405
