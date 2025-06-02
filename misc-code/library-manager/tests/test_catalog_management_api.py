import pytest
from app.api.catalog_management_api import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_checkout_item(client):
    response = client.put(
        '/checkout',
        query_string={'item_id': 'foo', 'user_id': 'bar'})
    assert response.status_code == 200
