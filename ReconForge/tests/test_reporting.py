from reconforge.core.reporting import render_markdown_report


def test_render_markdown_report_contains_findings() -> None:
    data = {
        "target": "https://example.com",
        "final_url": "https://example.com",
        "status_code": 200,
        "findings": [
            {
                "severity": "medium",
                "title": "Missing HSTS header",
                "details": "The response did not include Strict-Transport-Security.",
            }
        ],
    }
    markdown = render_markdown_report(data)
    assert "# ReconForge Report" in markdown
    assert "Missing HSTS header" in markdown
