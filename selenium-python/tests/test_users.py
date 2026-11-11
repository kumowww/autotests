from api_testing_framework.utils.test_data import CREATE_USER, UPDATE_USER

USER_SCHEMA = {
    "type": "object",
    "properties": {"id": {"type": "integer"}},
    "required": ["id"],
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
    assert response.json()["id"] == 1
    assert response.json()["username"] == "Bret"


def test_create_user(client):
    response = client.post("users", json=CREATE_USER)

    assert response.status_code == 201
    assert response.json()["name"] == CREATE_USER["name"]
    assert response.json()["job"] == CREATE_USER["job"]
    assert "id" in response.json()


def test_update_user(client):
    response = client.put("users/1", json=UPDATE_USER)

    assert response.status_code == 200
    assert response.json()["job"] == UPDATE_USER["job"]
