from api_testing_framework.utils.test_data import CREATE_USER


def test_create_post_resource(client):
    response = client.post("posts", json={"title": "autotest", "body": "demo", "userId": 1})

    assert response.status_code == 201
    assert response.json()["title"] == "autotest"
    assert response.json()["id"] == 101


def test_create_user_resource(client):
    response = client.post("users", json=CREATE_USER)

    assert response.status_code == 201
    assert response.json()["name"] == CREATE_USER["name"]
