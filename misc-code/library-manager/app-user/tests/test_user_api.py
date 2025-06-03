import pytest

from app.api.base_api import flask_app
from tests import unit_test_db_conn
from unittest.mock import patch

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


@patch('app.api.user_api.database_conn.get_db_session')
def test_create_user_success(mock_get_db_session, client):
    mock_get_db_session.side_effect = lambda: unit_test_db_conn.get_db_session(reset_data=False)
    fname = 'Johnny'
    lname = 'Doe'

    response = client.post(f'/user?first_name={fname}&last_name={lname}')
    assert response.status_code == 200
    user_id = response.json['user_id']

    response = client.get(f'/user?user_id={user_id}')
    assert response.status_code == 200
    assert response.json['user_id'] == user_id
    assert response.json['first_name'] == fname
    assert response.json['last_name'] == lname


@patch('app.api.user_api.database_conn.get_db_session')
def test_create_user_data_reset(mock_get_db_session, client):
    mock_get_db_session.side_effect = unit_test_db_conn.get_db_session
    fname = 'Johnny'
    lname = 'Doe'

    response = client.post(f'/user?first_name={fname}&last_name={lname}')
    assert response.status_code == 200
    user_id = response.json['user_id']

    response = client.get(f'/user?user_id={user_id}')
    assert response.status_code == 404
