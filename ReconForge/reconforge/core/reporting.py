from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def save_json_report(data: dict[str, Any], output_path: str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def render_markdown_report(data: dict[str, Any]) -> str:
    findings = data.get("findings", [])
    lines = [
        "# ReconForge Report",
        "",
        f"- **Target:** {data.get('target', 'N/A')}",
        f"- **Final URL:** {data.get('final_url', 'N/A')}",
        f"- **HTTP Status:** {data.get('status_code', 'N/A')}",
        "",
        "## Findings",
        "",
    ]

    if not findings:
        lines.append("No findings were recorded.")
    else:
        for item in findings:
            lines.extend([
                f"### {item.get('title', 'Untitled')}",
                f"- Severity: **{item.get('severity', 'unknown')}**",
                f"- Details: {item.get('details', '')}",
                "",
            ])
    return "\n".join(lines)


def save_markdown_report(data: dict[str, Any], output_path: str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown_report(data), encoding="utf-8")
    return path
