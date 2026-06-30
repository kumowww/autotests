"""
Generic API test runner using pytest.
Loads test cases from config.json and executes them.
"""
import requests
import pytest
import json
import base64
from pathlib import Path

# Load configuration
CONFIG_PATH = Path(__file__).parent / "config.json"
with open(CONFIG_PATH, encoding='utf-8') as f:
    config = json.load(f)

BASE_URL = config["base_url"]
AUTH = config.get("auth", {})

def basic_auth(role):
    """Create Basic Auth header for the given role."""
    user = AUTH[role]
    token = base64.b64encode(
        f"{user['username']}:{user['password']}".encode()
    ).decode()
    return {"Authorization": f"Basic {token}"}

@pytest.mark.parametrize("test_case", config["tests"])
def test_api(test_case):
    """Execute a single API test as defined in the config."""
    url = f"{BASE_URL}{test_case['path']}"
    headers = {"Content-Type": "application/json"}

    # Set authentication if required
    if test_case.get("auth_role"):
        headers.update(basic_auth(test_case["auth_role"]))
    elif test_case.get("auth_required") == False:
        pass  # No header

    method = test_case["method"].upper()
    if method == "POST":
        response = requests.post(url, json=test_case["body"], headers=headers)
    elif method == "PUT":
        response = requests.put(url, json=test_case["body"], headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:  # GET
        response = requests.get(url, headers=headers)

    # Verify status code
    assert response.status_code == test_case["expected_status"], (
        f"Expected {test_case['expected_status']}, "
        f"got {response.status_code} for '{test_case['name']}'"
    )

    # Verify response body content if specified
    if "expected_body_contains" in test_case:
        body = response.json()
        for key, allowed_values in test_case["expected_body_contains"].items():
            if not isinstance(allowed_values, list):
                allowed_values = [allowed_values]
            actual = body.get(key)
            assert actual in allowed_values, (
                f"Key '{key}': expected one of {allowed_values}, got {actual}"
            )