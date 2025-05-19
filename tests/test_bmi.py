import pytest
from app import create_app
from app.services.bmi_service import BMIService


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_calculate_bmi_function():
    """Test the BMI calculation function directly"""
    # Test normal case
    assert BMIService.calculate_bmi(70, 1.75) == pytest.approx(22.86, 0.01)
    # Test another normal case
    assert BMIService.calculate_bmi(80, 1.80) == pytest.approx(24.69, 0.01)
    # Test edge case with very low values
    assert BMIService.calculate_bmi(45, 1.60) == pytest.approx(17.58, 0.01)
    # Test edge case with high values
    assert BMIService.calculate_bmi(100, 1.90) == pytest.approx(27.70, 0.01)


def test_bmi_categories():
    """Test BMI category classification"""
    assert BMIService.get_bmi_category(17) == "Underweight"
    assert BMIService.get_bmi_category(22) == "Normal weight"
    assert BMIService.get_bmi_category(27) == "Overweight"
    assert BMIService.get_bmi_category(32) == "Obese"


def test_bmi_endpoint_success(client):
    """Test successful BMI calculation through the API"""
    response = client.post('/calculate-bmi',
                           json={'weight': 70, 'height': 1.75})
    assert response.status_code == 200
    data = response.get_json()
    assert 'bmi' in data
    assert 'category' in data
    assert data['bmi'] == pytest.approx(22.86, 0.01)
    assert data['category'] == "Normal weight"


def test_bmi_endpoint_missing_data(client):
    """Test API response when data is missing"""
    response = client.post('/calculate-bmi',
                           json={'weight': 70})
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_bmi_endpoint_invalid_data(client):
    """Test API response with invalid data"""
    response = client.post('/calculate-bmi',
                           json={'weight': -70, 'height': 1.75})
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_bmi_endpoint_non_numeric(client):
    """Test API response with non-numeric data"""
    response = client.post('/calculate-bmi',
                           json={'weight': 'invalid', 'height': 1.75})
    assert response.status_code == 400
    assert 'error' in response.get_json()
