# autotests

Automated UI and API test examples:

- **selenium-python/**: UI tests with Selenium WebDriver, pytest and page classes (`pages/`)
- **selenium-java/**: UI tests with Selenium WebDriver, JUnit 5 and Maven
- **api-python/**: API tests with requests and pytest
- **postman-collection/**: Postman collection (JSON) for manual and automated API checks
- **.github/workflows/tests.yml**: GitHub Actions workflow that runs all three test suites on every push and pull request

## Targets

- UI: https://www.saucedemo.com (public demo shop; demo accounts `standard_user` / `secret_sauce`, `locked_out_user` / `secret_sauce`)
- API: https://jsonplaceholder.typicode.com (public fake REST API, no key needed)

## Requirements

- Python 3.9 or newer (CI uses 3.12)
- Google Chrome (Selenium Manager downloads the matching driver automatically)
- Java 17 or newer and Maven 3.8 or newer (for `selenium-java`)

## Running the tests

```bash
cd selenium-python
pip install -r requirements.txt
pytest
```

```bash
cd api-python
pip install -r requirements.txt
pytest
```

```bash
cd selenium-java
mvn test
```

The Postman collection is in `postman-collection/`. Import the JSON file in Postman via **Import**.

## Technologies

- Selenium WebDriver 4 (Python, Java)
- pytest, requests
- JUnit 5, Maven
- Postman
- GitHub Actions

## Notes

- The tests use public demo sites. If their markup changes, the locators in `pages/` and in the Java test need to be updated.
