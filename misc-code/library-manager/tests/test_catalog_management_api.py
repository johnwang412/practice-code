import pytest
from app.api.catalog_management_api import app
from tests.sqlite_db_session import get_rw_session_from_clean_db

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# TODO: play with scope here
@pytest.fixture(scope="function")
def db_session():
    session = get_rw_session_from_clean_db()
    yield session
    session.close()


@pytest.fixture()
def three_users(db_session):
    return None



"""
1. Create a fixture that adds 3 users to the database
2. Create a fixture that adds 2 books to the database with 1 copy each
3. Test the checkout item function
"""

def test_checkout_item(client):
    response = client.put(
        '/checkout',
        query_string={'item_id': 'foo', 'user_id': 'bar'})
    assert response.status_code == 200
