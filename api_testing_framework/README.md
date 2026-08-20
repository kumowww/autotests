# API Testing Framework

This folder contains an example API testing framework using Python, pytest and requests.
Tests are configured to run against the public demo API at https://reqres.in/api which supports user CRUD endpoints.

Structure:

- tests/ - pytest tests covering users, auth and placeholder tests for products and orders
- utils/ - ApiClient helper and test payloads
- config/ - config.json (base_url and optional token)
- reports/ - empty folder reserved for test reports

How to run

1. Create and activate a virtual environment (recommended).

2. Install dependencies:
   pip install -r api_testing_framework/requirements.txt

3. Run tests:
   pytest api_testing_framework/tests

Notes

- Tests include JSON Schema validation and simple performance assertions (response time).
- Update config/config.json to point to your API and set authentication if needed.
- You can extend tests to include negative cases, authentication flows, header checks, and schema checks.
