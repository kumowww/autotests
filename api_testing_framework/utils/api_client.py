import time
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from jsonschema import validate as json_validate

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class ApiClient:
    def __init__(self, base_url, token=None, timeout=10, max_retries=3, backoff_factor=0.5):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.timeout = timeout

        # Setup retry strategy for idempotent methods and some server errors
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
            backoff_factor=backoff_factor,
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        if token:
            self.session.headers.update({'Authorization': f'Bearer {token}'})
        self.session.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

    def _url(self, path):
        if path.startswith('http'):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def _measure(self, start):
        # prefer response.elapsed when available
        return (time.time() - start) * 1000

    def get(self, path, params=None, **kwargs):
        url = self._url(path)
        logger.debug("GET %s params=%s headers=%s", url, params, self.session.headers)
        start = time.time()
        r = self.session.get(url, params=params, timeout=self.timeout, **kwargs)
        r.elapsed_ms = r.elapsed.total_seconds() * 1000 if hasattr(r, 'elapsed') else self._measure(start)
        logger.debug("RESP %s status=%s time=%sms", url, r.status_code, r.elapsed_ms)
        return r

    def post(self, path, json=None, **kwargs):
        url = self._url(path)
        logger.debug("POST %s body=%s", url, json)
        start = time.time()
        r = self.session.post(url, json=json, timeout=self.timeout, **kwargs)
        r.elapsed_ms = r.elapsed.total_seconds() * 1000 if hasattr(r, 'elapsed') else self._measure(start)
        logger.debug("RESP %s status=%s time=%sms", url, r.status_code, r.elapsed_ms)
        return r

    def put(self, path, json=None, **kwargs):
        url = self._url(path)
        logger.debug("PUT %s body=%s", url, json)
        start = time.time()
        r = self.session.put(url, json=json, timeout=self.timeout, **kwargs)
        r.elapsed_ms = r.elapsed.total_seconds() * 1000 if hasattr(r, 'elapsed') else self._measure(start)
        logger.debug("RESP %s status=%s time=%sms", url, r.status_code, r.elapsed_ms)
        return r

    def delete(self, path, **kwargs):
        url = self._url(path)
        logger.debug("DELETE %s", url)
        start = time.time()
        r = self.session.delete(url, timeout=self.timeout, **kwargs)
        r.elapsed_ms = r.elapsed.total_seconds() * 1000 if hasattr(r, 'elapsed') else self._measure(start)
        logger.debug("RESP %s status=%s time=%sms", url, r.status_code, r.elapsed_ms)
        return r

    @staticmethod
    def validate_schema(instance, schema):
        json_validate(instance=instance, schema=schema)
