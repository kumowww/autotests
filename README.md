# autotests

[![Python tests](https://github.com/kumowww/autotests/actions/workflows/tests.yml/badge.svg)](https://github.com/kumowww/autotests/actions/workflows/tests.yml)

Examples and starter templates for UI and API automation with Python, Selenium, pytest, Java, Maven, and Postman. The repository currently demonstrates test structure and reusable helpers; it is not a universal test suite that can validate an arbitrary website without adapting URLs, selectors, credentials, endpoints, and expected results.

## Repository contents

```text
selenium-python/          Python Selenium tests, page objects, browser fixture
selenium-java/            Java Selenium/JUnit example and Maven configuration
api_testing_framework/    Python API client, pytest tests, and JSON configuration
generic/                  Config-driven API test runner and sample local-service config
postman-collection/       Postman collection template
Dockerfile                Python and Chromium container image
pytest.ini                Root pytest discovery and import configuration
requirements.txt          Root Python dependencies
```

The Python UI examples use SauceDemo login page objects in `selenium-python/pages/`. The API framework's client is `api_testing_framework/utils/api_client.py`. The `generic/` runner loads cases from `generic/config.json`; its sample base URL points to a local service at `http://localhost:28852`, which is not included in this repository. The Java test in `selenium-java/src/test/java/tests/ExampleTest.java` is a Google search example, not a configurable product-specific page-object suite. The Postman collection contains a URL placeholder and must be configured before sending requests.

## Prerequisites

- Python 3.10 or newer and pip
- Google Chrome or Chromium for Selenium tests
- Java 17 and Maven for the Java example
- Docker for containerized Python test execution
- Network access to the selected demo or application under test

## Download and install Python dependencies

```bash
git clone https://github.com/kumowww/autotests.git
cd autotests
python -m venv .venv
```

Activate the virtual environment:

```bash
# macOS or Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install the root Python dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Important: adapt before running

This repository includes starter examples for different sites and APIs, so their selectors, request schemas, and expected responses are not interchangeable. In particular, review each test file before running the complete pytest collection. The Selenium directory also contains older generic examples alongside the SauceDemo page-object example; the API tests and their configured base URL must describe the same API. The sample `generic/config.json` targets a local service that is not shipped here.

To adapt the UI example for another site:

1. Set the page URL and element locators in the relevant class under `selenium-python/pages/`.
2. Replace the test actions and assertions in `selenium-python/tests/` with flows and expected behavior for that site's test environment.
3. Keep site-specific locators and actions in page classes, and keep scenario assertions in tests.
4. Use only accounts and systems you are authorized to test.

To adapt the API example:

1. Set `base_url` in `api_testing_framework/config/config.json`, or override it with `API_BASE_URL`.
2. Update request paths, payloads, response assertions, and schemas in `api_testing_framework/tests/` for the target API.
3. Supply credentials through environment variables such as `API_TOKEN`; do not commit secrets.
4. Keep in mind that the generic runner is separate and reads `generic/config.json`.

## Run tests

From the repository root, run a selected test file after configuring it for the target:

```bash
pytest selenium-python/tests/test_login.py -v
pytest api_testing_framework/tests/test_users.py -v
```

Run the full Python collection only after checking that every discovered test is configured for the same environment:

```bash
pytest -v
```

The Selenium fixture in `selenium-python/conftest.py` uses headless mode by default. Set `HEADLESS=false` to display the browser. Chrome and a compatible driver must be available locally.

The Java example can be run separately:

```bash
cd selenium-java
mvn test
```

## Docker

The root `Dockerfile` installs Python dependencies and Chromium, then runs `pytest` by default:

```bash
docker build -t autotests .
docker run --rm autotests
```

Configure and validate the tests against your target before using the full-suite Docker command.

## GitHub Actions

A CI badge is shown above, but this repository currently has no workflow file under `.github/workflows/`. The badge will not report a passing workflow until a workflow is added and enabled.

## Postman

Import `postman-collection/example_collection.json` in Postman and replace the example URL with an endpoint in your test environment.
