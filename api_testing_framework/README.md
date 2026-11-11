# API Testing Framework

This directory contains a Python API test client and pytest examples. `utils/api_client.py` wraps `requests` and provides common HTTP methods, retries, response-time measurement, and JSON Schema validation. Test cases are in `tests/`, shared fixtures are in `tests/conftest.py`, sample request bodies are in `utils/test_data.py`, and `config/config.json` stores the base URL and timeout.

## Current configuration and compatibility

The checked-in configuration currently sets `base_url` to `https://jsonplaceholder.typicode.com`. However, the existing `tests/test_users.py` and `tests/test_auth.py` include assertions and request payloads for a different API format, such as a `data` response wrapper and a `login` endpoint. The tests and configured base URL therefore do not currently describe one matching API. Configure both for the same service before expecting the suite to pass.

The tests in `test_products.py` and `test_orders.py` are placeholders, not actual product or order coverage.

## Install and run from the repository root

```bash
python -m venv .venv
```

Activate the environment, then install the root dependency set:

```bash
# macOS or Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
pytest api_testing_framework/tests -v
```

The framework also has a directory-specific `requirements.txt`; the root `requirements.txt` is the convenient shared dependency set for this repository. To install only this framework's dependencies instead, run `python -m pip install -r api_testing_framework/requirements.txt`.

## Configure a target API

Set `base_url` in `config/config.json`, or override it for one run:

```bash
# macOS or Linux
API_BASE_URL=https://your-test-api.example.com pytest api_testing_framework/tests -v

# Windows PowerShell
$env:API_BASE_URL = "https://your-test-api.example.com"
pytest api_testing_framework/tests -v
```

`API_TIMEOUT` overrides the timeout in seconds. `API_TOKEN` supplies an optional bearer token. Keep credentials outside tracked files and use a test environment, not production.

Changing only the base URL is not sufficient when the API's paths or response shapes differ. Update the cases in `tests/`, payloads in `utils/test_data.py`, and any JSON schemas to match the target service. For example, the current user tests expect a `data` wrapper and user fields such as `first_name`, while JSONPlaceholder's user endpoint returns a flat object with different fields.

## Adapting the framework

1. Choose a test or demo API and confirm its routes, authentication method, payloads, and response schemas.
2. Set its base URL in `config/config.json` or with `API_BASE_URL`.
3. Update the corresponding tests and test data for the API contract.
4. Add explicit assertions for successful and error responses.
5. Run the smallest relevant test file first, then the full API test directory.

The API client supports `get`, `post`, `put`, and `delete` methods. Use `client.validate_schema(instance, schema)` when the response has a stable schema. The repository does not include an API server; the test target must be reachable separately.

## Generic API runner

The separate `generic/` directory contains a config-driven runner. It reads `generic/config.json`, not this directory's `config/config.json`, and the committed example uses a local service at `http://localhost:28852`. That service is not included in this repository. See `generic/README.md` and replace its example test cases and base URL for your own application.
