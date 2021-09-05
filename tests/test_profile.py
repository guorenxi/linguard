import sys

import pytest
from flask_login import current_user

from tests.utils import default_cleanup, is_http_success, login, exists_credentials_file

url = "/profile"


def cleanup():
    default_cleanup()


@pytest.fixture
def client():
    sys.argv = [sys.argv[0], "linguard.test.yaml"]
    from app import app
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


def test_get(client):
    login(client)

    response = client.get(url)
    assert is_http_success(response.status_code), cleanup()
    assert current_user.name.encode() in response.data

    cleanup()


def test_post_ok(client):
    login(client)

    new_username = "root"
    response = client.post(url, data={"username": new_username})
    assert is_http_success(response.status_code), cleanup()
    assert b"alert-danger" not in response.data, cleanup()
    assert current_user.name == new_username
    assert exists_credentials_file()

    cleanup()


def test_post_ko(client):
    login(client)

    response = client.post(url, data={"username": ""})
    assert is_http_success(response.status_code), cleanup()
    assert b"alert-danger" in response.data, cleanup()
    assert not exists_credentials_file()

    cleanup()
