import os
import json
import logging
import pytest
from api_testing_framework.utils.api_client import ApiClient
from dotenv import load_dotenv

load_dotenv()  # load .env if exists

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=LOG_LEVEL)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

@pytest.fixture(scope='session')
def config():
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    # allow env override
    cfg['base_url'] = os.getenv('API_BASE_URL', cfg.get('base_url'))
    return cfg

@pytest.fixture(scope='session')
def client(config):
    token = os.getenv('API_TOKEN', config.get('auth', {}).get('token'))
    return ApiClient(base_url=config['base_url'], token=token)