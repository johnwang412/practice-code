import pytest

from app.api.base_api import flask_app
from app.models.user_orm import User
from tests import unit_test_db_conn
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def test_db_session():
    dbs = unit_test_db_conn.get_db_session()
    return dbs


@patch('app.api.user_api.database_conn.get_db_session')
def test_create_user_success(mock_get_db_session, client, test_db_session):
    mock_get_db_session.return_value = test_db_session
    response = client.post('/user?first_name=John&last_name=Doe')
    assert response.status_code == 200
    assert response.json['user_id'] == 1
