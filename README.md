# autotests

A collection of automated test examples demonstrating skills in UI and API testing using Java, Python, Selenium, Postman, and pytest.

## Repository structure

**selenium-java/** Selenium WebDriver tests written in Java with JUnit 5 and Maven.
**selenium-python/** Selenium WebDriver tests written in Python with pytest.
**api-python/** API tests written in Python with requests and pytest.
**postman-collection/** Exported Postman collection for manual/automated API exploration.

## Prerequisites

JDK 11 or newer (for Java tests)
Maven 3.8+
Python 3.9+ with pip
Google Chrome browser
Git (to clone the repository)

## Getting started

1. Clone the repository:

git clone https://github.com/kumowww/autotests.git

cd autotests

## Run Java Selenium tests:

cd selenium-java
mvn clean test

## Run Python Selenium tests:

cd selenium-python
pip install -r requirements.txt
pytest

## Run Python API tests:

cd api-python
pip install -r requirements.txt
pytest

## Import Postman collection:

Open Postman, click Import and select the JSON file from postman-collection/.

## Test configuration

Each test file contains placeholders (marked with comments) where you can insert your own website URL, API endpoints, search queries, and expected values. Look for lines like:

- BASE_URL = "INSERT_YOUR_SITE_URL"

- endpoint = "/users"

- EXPECTED_TITLE = "Expected page title"

Replace them with actual data before running.

## Technologies demonstrated

- Automated UI testing with Selenium WebDriver

- Page Object Model (implicitly, through structured helper classes)

- API testing with requests library

- Test frameworks: JUnit 5, pytest

- Build and dependency management: Maven, pip

- Version control: Git

##  Contact

GitHub: kumowww