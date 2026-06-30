# Generic API Test Suite

A configurable test framework for REST APIs, using Python and pytest.

## Structure
- `config.json` – test cases and environment settings
- `test_runner.py` – pytest test executor
- `README.md` – this file

## Prerequisites
- Python 3.8+
- Install dependencies: `pip install pytest requests`

## Usage
1. Edit `config.json` to match your API endpoints and credentials.
2. Ensure your application is running.
3. Run the tests:  
   `pytest test_runner.py -v`

## Adding New Projects
Copy this folder and adjust `config.json`. The test runner remains unchanged.