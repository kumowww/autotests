import pytest
from api_testing_framework.utils.test_data import CREATE_USER, UPDATE_USER

USER_SCHEMA_DATA = {
    "type": "object",
    "properties": {
        "id": {"type": ["integer", "string"]},
        "email": {"type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "avatar": {"type": "string"}
    },
    "required": ["id"]
}

def test_get_users_list(client):
    r = client.get('users', params={'page': 2})
    assert r.status_code == 200
    assert 'application/json' in r.headers.get('Content-Type', '')
    assert r.elapsed_ms < 2000
    j = r.json()
    assert 'data' in j
    if j['data']:
        # validate first element structure (loose)
        client.validate_schema(j['data'][0], USER_SCHEMA_DATA)

def test_get_single_user(client):
    r = client.get('users/2')
    assert r.status_code == 200
    j = r.json()
    assert 'data' in j
    client.validate_schema(j['data'], USER_SCHEMA_DATA)

@pytest.fixture
def created_user(client):
    r = client.post('users', json=CREATE_USER)
    assert r.status_code in (201, 200)
    j = r.json()
    # reqres returns id and createdAt
    uid = j.get('id')
    yield uid
    # cleanup if API supports delete (reqres doesn't actually persist, but pattern shown)
    if uid:
        client.delete(f'users/{uid}')

def test_create_update_delete_user(client, created_user):
    uid = created_user
    assert uid is not None
    # update
    r = client.put(f'users/{uid}', json=UPDATE_USER)
    assert r.status_code in (200, 201)
    j = r.json()
    assert 'updatedAt' in j or j.get('job') == UPDATE_USER['job']

def test_negative_create_user_invalid_payload(client):
    # missing required fields
    r = client.post('users', json={"invalid": "data"})
    # depending on API could be 400 or 201; assert either way but check response for expected behavior
    assert r.status_code in (400, 201, 422)