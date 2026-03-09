from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from reconforge.utils.http import normalize_target, origin, request_url


@dataclass
class DiscoveryResult:
    target: str
    final_url: str
    status_code: int
    title: str
    server: str | None
    content_type: str | None
    content_length: int
    same_origin_links: list[str]
    technologies: list[str]
    robots_txt: bool
    sitemap_xml: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _guess_technologies(headers: dict[str, str], html: str) -> list[str]:
    fingerprints: list[str] = []
    server = headers.get("Server", "")
    powered_by = headers.get("X-Powered-By", "")

    checks = {
        "nginx": "Nginx",
        "apache": "Apache",
        "cloudflare": "Cloudflare",
        "php": "PHP",
        "express": "Express",
    }
    haystack = f"{server} {powered_by} {html[:4000]}".lower()
    for token, label in checks.items():
        if token in haystack and label not in fingerprints:
            fingerprints.append(label)

    html_checks = {
        "wp-content": "WordPress",
        "next/static": "Next.js",
        "__next": "Next.js",
        "react": "React",
        "vue": "Vue",
        "angular": "Angular",
        "bootstrap": "Bootstrap",
    }
    for token, label in html_checks.items():
        if token in html.lower() and label not in fingerprints:
            fingerprints.append(label)

    return fingerprints


def _extract_same_origin_links(base_url: str, html: str, limit: int = 15) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    base_origin = origin(base_url)
    links: list[str] = []
    for tag in soup.find_all("a", href=True):
        href = urljoin(base_url, tag["href"])
        if urlparse(href).scheme not in {"http", "https"}:
            continue
        if origin(href) == base_origin and href not in links:
            links.append(href)
        if len(links) >= limit:
            break
    return links


def discover(target: str) -> dict[str, Any]:
    normalized = normalize_target(target)
    try:
        response = request_url(normalized)
    except Exception as exc:
        return {
            "target": normalized,
            "error": str(exc),
            "same_origin_links": [],
            "technologies": [],
            "robots_txt": False,
            "sitemap_xml": False,
        }

    html = response.text if "html" in response.headers.get("Content-Type", "") else ""
    soup = BeautifulSoup(html, "html.parser") if html else None
    title = soup.title.get_text(strip=True) if soup and soup.title else ""

    robots_ok = False
    sitemap_ok = False
    try:
        robots_ok = request_url(urljoin(response.url, "/robots.txt"), timeout=5).status_code == 200
    except Exception:
        robots_ok = False
    try:
        sitemap_ok = request_url(urljoin(response.url, "/sitemap.xml"), timeout=5).status_code == 200
    except Exception:
        sitemap_ok = False

    result = DiscoveryResult(
        target=normalized,
        final_url=response.url,
        status_code=response.status_code,
        title=title,
        server=response.headers.get("Server"),
        content_type=response.headers.get("Content-Type"),
        content_length=len(response.text),
        same_origin_links=_extract_same_origin_links(response.url, html),
        technologies=_guess_technologies(response.headers, html),
        robots_txt=robots_ok,
        sitemap_xml=sitemap_ok,
    )
    return result.to_dict()
