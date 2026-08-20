import json
import os
import pytest
from api_testing_framework.utils.api_client import ApiClient

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

@pytest.fixture(scope='session')
def config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

@pytest.fixture(scope='session')
def client(config):
    base = config.get('base_url')
    token = config.get('auth', {}).get('token')
    return ApiClient(base_url=base, token=token)
