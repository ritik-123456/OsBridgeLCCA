import pytest
from backend.main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# ✅ Test API Endpoint for Cost Calculation
@pytest.mark.integration
def test_cost_calculation_api(client):
    response = client.post("/calculate_cost", json={"quantity": 100, "rate": 500})
    assert response.status_code == 200
    assert response.json["total_cost"] == 50000
# Placeholder for test API
