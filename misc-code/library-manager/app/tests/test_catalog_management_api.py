import pytest
from app.api.catalog_management_api import app
from app.tests.unittest_db_conn import get_rw_session_from_clean_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_checkout_item(client):
    response = client.put(
        '/checkout',
        query_string={'item_id': 1, 'user_id': 1})
    assert response.status_code == 200
