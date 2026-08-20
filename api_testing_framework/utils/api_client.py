import time
import requests
from jsonschema import validate

class ApiClient:
    def __init__(self, base_url, token=None, timeout=10):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.timeout = timeout
        if token:
            self.session.headers.update({'Authorization': f'Bearer {token}'})

    def _url(self, path):
        if path.startswith('http'):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path, params=None, **kwargs):
        start = time.time()
        r = self.session.get(self._url(path), params=params, timeout=self.timeout, **kwargs)
        r.elapsed_ms = (time.time() - start) * 1000
        return r

    def post(self, path, json=None, **kwargs):
        start = time.time()
        r = self.session.post(self._url(path), json=json, timeout=self.timeout, **kwargs)
        r.elapsed_ms = (time.time() - start) * 1000
        return r

    def put(self, path, json=None, **kwargs):
        start = time.time()
        r = self.session.put(self._url(path), json=json, timeout=self.timeout, **kwargs)
        r.elapsed_ms = (time.time() - start) * 1000
        return r

    def delete(self, path, **kwargs):
        start = time.time()
        r = self.session.delete(self._url(path), timeout=self.timeout, **kwargs)
        r.elapsed_ms = (time.time() - start) * 1000
        return r

    @staticmethod
    def validate_schema(instance, schema):
        validate(instance=instance, schema=schema)
