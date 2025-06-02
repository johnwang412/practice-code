import pytest
from app.api.catalog_management_api import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health_status_code(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_health_response_json(client):
    response = client.get('/health')
    assert response.is_json
    assert response.get_json() == {'status': 'ok'}

def test_health_method_not_allowed(client):
    response = client.post('/health')
    assert response.status_code == 405