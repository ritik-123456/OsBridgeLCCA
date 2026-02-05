import pytest
from backend.main import app as flask_app

@pytest.fixture
def client():
    """Flask test client"""
    return flask_app.test_client()

@pytest.fixture
def sample_cost_data():
    """Sample cost data for testing"""
    return {"quantity": 100, "rate": 500}
