import time
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from jsonschema import validate as json_validate

logger = logging.getLogger(__name__)

class ApiClient:
    def __init__(self, base_url, token=None, timeout=10, max_retries=3, backoff_factor=0.5):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.timeout = timeout

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

    def get(self, path, params=None, **kwargs):
        url = self._url(path)
        start = time.time()
        r = self.session.get(url, params=params, timeout=self.timeout, **kwargs)
        r.elapsed_ms = r.elapsed.total_seconds() * 1000 if hasattr(r, 'elapsed') else (time.time()-start)*1000
        logger.debug("GET %s -> %s (%sms)", url, r.status_code, r.elapsed_ms)
        return r

    def post(self, path, json=None, **kwargs):
        url = self._url(path)
        start = time.time()
        r = self.session.post(url, json=json, timeout=self.timeout, **kwargs)
        r.elapsed_ms = r.elapsed.total_seconds() * 1000 if hasattr(r, 'elapsed') else (time.time()-start)*1000
        logger.debug("POST %s -> %s (%sms)", url, r.status_code, r.elapsed_ms)
        return r

    def put(self, path, json=None, **kwargs):
        url = self._url(path)
        start = time.time()
        r = self.session.put(url, json=json, timeout=self.timeout, **kwargs)
        r.elapsed_ms = r.elapsed.total_seconds() * 1000 if hasattr(r, 'elapsed') else (time.time()-start)*1000
        logger.debug("PUT %s -> %s (%sms)", url, r.status_code, r.elapsed_ms)
        return r

    def delete(self, path, **kwargs):
        url = self._url(path)
        start = time.time()
        r = self.session.delete(url, timeout=self.timeout, **kwargs)
        r.elapsed_ms = r.elapsed.total_seconds() * 1000 if hasattr(r, 'elapsed') else (time.time()-start)*1000
        logger.debug("DELETE %s -> %s (%sms)", url, r.status_code, r.elapsed_ms)
        return r

    @staticmethod
    def validate_schema(instance, schema):
        json_validate(instance=instance, schema=schema)
