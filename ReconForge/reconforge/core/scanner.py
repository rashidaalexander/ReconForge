from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from reconforge.utils.http import normalize_target, request_url

SECURITY_HEADERS = {
    "Strict-Transport-Security": "Missing HSTS header",
    "Content-Security-Policy": "Missing Content-Security-Policy header",
    "X-Content-Type-Options": "Missing X-Content-Type-Options header",
    "Referrer-Policy": "Missing Referrer-Policy header",
}


@dataclass
class Finding:
    severity: str
    title: str
    details: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def scan(target: str) -> dict[str, Any]:
    normalized = normalize_target(target)
    try:
        response = request_url(normalized)
    except Exception as exc:
        return {
            "target": normalized,
            "error": str(exc),
            "findings": [],
            "options_status": None,
        }

    findings: list[Finding] = []

    for header, message in SECURITY_HEADERS.items():
        if header not in response.headers:
            findings.append(Finding(
                severity="medium",
                title=message,
                details=f"The response for {response.url} did not include {header}.",
            ))

    server = response.headers.get("Server")
    if server:
        findings.append(Finding(
            severity="info",
            title="Server header disclosed",
            details=f"The server identified itself as: {server}",
        ))

    x_powered_by = response.headers.get("X-Powered-By")
    if x_powered_by:
        findings.append(Finding(
            severity="info",
            title="X-Powered-By header disclosed",
            details=f"The application disclosed framework information: {x_powered_by}",
        ))

    options_status = None
    try:
        options_status = request_url(response.url, method="OPTIONS", timeout=5).status_code
    except Exception:
        options_status = None

    return {
        "target": normalized,
        "final_url": response.url,
        "status_code": response.status_code,
        "findings": [item.to_dict() for item in findings],
        "options_status": options_status,
    }
