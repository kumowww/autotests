import time
import logging
from typing import Any, Dict, List, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from jsonschema import validate as json_validate

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ApiClient:
    """JSON API client with retry, logging and schema validation."""

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        timeout: Union[float, tuple] = 10,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        allowed_methods: Optional[List[str]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.timeout = timeout
        if allowed_methods is None:
            # By default retry only idempotent methods, exclude POST to avoid duplicates
            allowed_methods = ["HEAD", "GET", "OPTIONS", "PUT", "DELETE"]
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=allowed_methods,
            backoff_factor=backoff_factor,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})

    def _url(self, path: str) -> str:
        """Return absolute URL for a path or pass-through absolute URLs."""
        if path.startswith(("http://", "https://")):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def _safe_headers(self) -> Dict[str, str]:
        """Return headers for logging without sensitive Authorization header."""
        return {k: v for k, v in self.session.headers.items() if k.lower() != "authorization"}

    def _log_request(self, method: str, url: str, params: Any = None, json_body: Any = None) -> None:
        logger.debug("%s %s params=%s json=%s headers=%s", method, url, params, json_body, self._safe_headers())

    def _request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None, json: Optional[Any] = None, **kwargs) -> requests.Response:
        url = self._url(path)
        self._log_request(method, url, params=params, json_body=json)
        start = time.perf_counter()
        try:
            response = self.session.request(method=method, url=url, params=params, json=json, timeout=self.timeout, **kwargs)
        except requests.RequestException:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.exception("%s %s failed after %.2fms", method, url, elapsed_ms)
            raise
        elapsed_ms = (response.elapsed.total_seconds() * 1000) if getattr(response, "elapsed", None) is not None else (time.perf_counter() - start) * 1000
        response.elapsed_ms = elapsed_ms
        logger.debug("RESP %s %s -> status=%s elapsed_ms=%.2f", method, url, response.status_code, elapsed_ms)
        return response

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        return self._request("GET", path, params=params, **kwargs)

    def post(self, path: str, json: Optional[Any] = None, **kwargs) -> requests.Response:
        return self._request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: Optional[Any] = None, **kwargs) -> requests.Response:
        return self._request("PUT", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._request("DELETE", path, **kwargs)

    @staticmethod
    def validate_schema(instance: Any, schema: Any) -> None:
        """Validate JSON object against provided schema, raises on mismatch."""
        json_validate(instance=instance, schema=schema)

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "ApiClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
