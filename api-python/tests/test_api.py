import requests

def test_get_users(base_url):
    # Change the endpoint to match your API
    endpoint = "/users"
    response = requests.get(f"{base_url}{endpoint}")

    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Response should be a list of users"
    assert len(data) > 0, "User list is empty"

def test_create_user(base_url):
    # Change endpoint and payload as needed
    endpoint = "/users"
    payload = {
        "name": "Test User",
        "email": "test@example.com"
    }
    response = requests.post(f"{base_url}{endpoint}", json=payload)

    assert response.status_code in [201, 200], f"Expected 201/200, but got {response.status_code}"
    data = response.json()
    assert data["name"] == payload["name"], "User name doesn't match"
    assert "id" in data, "Response should contain an 'id' field"