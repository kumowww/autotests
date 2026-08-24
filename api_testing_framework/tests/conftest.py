import json
import logging
import os
from pathlib import Path
from typing import Dict, Any

import pytest
from dotenv import load_dotenv

from api_testing_framework.utils.api_client import ApiClient

load_dotenv()
if not logging.getLogger().handlers:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config" / "config.json"
CONFIG_PATH = Path(os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH))


@pytest.fixture(scope="session")
def config() -> Dict[str, Any]:
    """Load config from JSON and allow overrides via environment variables."""
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    if "API_BASE_URL" in os.environ:
        cfg["base_url"] = os.environ["API_BASE_URL"]
    if "API_TIMEOUT" in os.environ:
        cfg["timeout"] = float(os.environ["API_TIMEOUT"])
    return cfg


@pytest.fixture(scope="session")
def client(config: Dict[str, Any]) -> ApiClient:
    """Create ApiClient instance using config and environment variables."""
    token = os.getenv("API_TOKEN", config.get("auth", {}).get("token"))
    api_client = ApiClient(base_url=config["base_url"], token=token, timeout=config.get("timeout", 10))
    yield api_client
    api_client.close()
