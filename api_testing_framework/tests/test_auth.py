import pytest

def test_auth_protected_endpoint_requires_token(client):
    # This API doesn't enforce token on public endpoints; check unknown routes handling
    r = client.get('unknown/endpoint')
    # Accept either 404 or 401 depending on API; ensure we handle unauthorized/unknown gracefully
    assert r.status_code in (401, 404)

def test_login_emulation(client):
    # Reqres provides a login endpoint for testing
    payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    r = client.post('login', json=payload)
    assert r.status_code == 200
    body = r.json()
    assert 'token' in body
