from __future__ import annotations

from urllib.parse import urlparse

import requests

DEFAULT_HEADERS = {
    "User-Agent": "ReconForge/0.1 (+https://github.com/rashidaalexander/reconforge)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def normalize_target(target: str) -> str:
    target = target.strip()
    if not target.startswith(("http://", "https://")):
        target = f"https://{target}"
    return target.rstrip("/")


def request_url(url: str, method: str = "GET", timeout: int = 10) -> requests.Response:
    response = requests.request(
        method=method,
        url=url,
        headers=DEFAULT_HEADERS,
        timeout=timeout,
        allow_redirects=True,
    )
    return response


def origin(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"
