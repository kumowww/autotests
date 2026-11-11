# Generic API Test Suite

`test_runner.py` is a small pytest runner that loads request cases from `config.json` and sends them with `requests`. Each case can specify a name, HTTP method, path, request body, expected status, optional expected response fields, and an optional authentication role. Basic authentication credentials are also stored in this sample configuration.

## Included configuration

The committed `config.json` is an example for a local application at `http://localhost:28852`. It contains authentication roles named `admin` and `merchant` and example endpoints under `/api/auth/user` and `/api/antifraud/transaction`. The application is not included in this repository, so these requests will not work until a compatible test service is running and the configuration is updated.

The sample uses test credentials for illustration. Replace them with credentials for a disposable local or test environment. Never put real or production secrets in a committed config file.

## Install dependencies

Run commands from the repository root. The root requirements file includes the dependencies used by this runner and the other Python examples:

```bash
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
# macOS or Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configure and run

1. Start the API application that you are authorized to test.
2. Edit `generic/config.json` and set `base_url` to the application's base URL.
3. Replace the sample credentials and test cases with valid test accounts, paths, request bodies, and expected responses.
4. Run the runner from the repository root:

```bash
pytest generic/test_runner.py -v
```

The runner supports `GET`, `POST`, `PUT`, and `DELETE`. It checks the expected HTTP status and, when `expected_body_contains` is present, checks configured values in the JSON response body. It constructs Basic authentication headers from the selected role. Use only disposable test data because test cases may create or modify resources.

## Adding test cases

Add objects to the `tests` array in `config.json`. Example shape:

```json
{
  "name": "Get a resource",
  "method": "GET",
  "path": "/api/resources/1",
  "expected_status": 200,
  "expected_body_contains": {
    "id": 1
  }
}
```

Use the actual contract of your API. The runner is intentionally simple; it does not currently provide environment-variable configuration, request timeouts, response-schema validation, or automatic test-data cleanup.
