import pytest
from api_testing_framework.utils.test_data import CREATE_USER, UPDATE_USER


USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string"},
    },
    "required": ["id", "name", "username", "email"],
}


def test_get_users_list(client):
    response = client.get("users")

    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")

    users = response.json()

    assert isinstance(users, list)
    assert users
    client.validate_schema(users[0], USER_SCHEMA)


def test_get_single_user(client):
    response = client.get("users/1")

    assert response.status_code == 200

    user = response.json()

    assert user["id"] == 1
    assert user["username"] == "Bret"
    client.validate_schema(user, USER_SCHEMA)


def test_create_user(client):
    response = client.post("users", json=CREATE_USER)

    assert response.status_code == 201

    created_user = response.json()

    assert created_user["name"] == CREATE_USER["name"]
    assert created_user["username"] == CREATE_USER["username"]
    assert created_user["email"] == CREATE_USER["email"]
    assert "id" in created_user


def test_update_user(client):
    response = client.put("users/1", json=UPDATE_USER)

    assert response.status_code == 200

    updated_user = response.json()

    assert updated_user["name"] == UPDATE_USER["name"]
    assert updated_user["username"] == UPDATE_USER["username"]
    assert updated_user["email"] == UPDATE_USER["email"]
