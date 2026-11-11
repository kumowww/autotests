def test_unknown_resource_returns_not_found(client):
    response = client.get("not-a-resource")

    assert response.status_code == 404


def test_unknown_user_returns_not_found(client):
    response = client.get("users/999999")

    assert response.status_code == 404
