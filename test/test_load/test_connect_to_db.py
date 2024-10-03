import pytest
from unittest.mock import patch, MagicMock
from src.load.connect_to_db import connect_to_db


@pytest.fixture
def connection_variables():
    return ["test_db", "test_username", "test_password", "test_host", "test_port"]


@patch("psycopg2.connect")
@patch("os.getenv")
def test_connect_to_db_success(mock_getenv, mock_connect, connection_variables):
    mock_getenv.side_effect = connection_variables

    mock_connect.return_value = MagicMock()

    connection = connect_to_db()

    assert connection is not None
    mock_connect.assert_called_once_with(
        dbname="test_db",
        user="test_username",
        password="test_password",
        host="test_host",
        port="test_port",
    )
