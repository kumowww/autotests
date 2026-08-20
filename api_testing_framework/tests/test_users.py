import pytest
from jsonschema import Draft7Validator
from api_testing_framework.utils.api_client import ApiClient

USER_SCHEMA = {
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "id": {"type": ["integer", "string"]},
                "email": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "avatar": {"type": "string"}
            },
            "required": ["id", "email", "first_name", "last_name", "avatar"]
        }
    },
    "required": ["data"]
}


def test_get_users_list(client):
    r = client.get('users', params={'page': 2})
    assert r.status_code == 200
    assert 'application/json' in r.headers.get('Content-Type', '')
    assert r.elapsed_ms < 2000, f"Response too slow: {r.elapsed_ms}ms"
    json_body = r.json()
    assert 'data' in json_body
    # basic schema validation for first user
    if json_body.get('data'):
        client.validate_schema({'data': json_body['data'][0]}, USER_SCHEMA)


def test_get_single_user(client):
    r = client.get('users/2')
    assert r.status_code == 200
    json_body = r.json()
    client.validate_schema(json_body, USER_SCHEMA)
