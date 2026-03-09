from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

from reconforge.core.discovery import discover
from reconforge.core.reporting import save_json_report, save_markdown_report
from reconforge.core.scanner import scan

console = Console()


def _print_json(data: dict[str, Any]) -> None:
    console.print_json(json.dumps(data))


def _print_findings(data: dict[str, Any]) -> None:
    table = Table(title="ReconForge Findings")
    table.add_column("Severity")
    table.add_column("Title")
    table.add_column("Details")
    findings = data.get("findings", [])
    if not findings:
        console.print("[green]No findings recorded.[/green]")
        return
    for item in findings:
        table.add_row(item.get("severity", ""), item.get("title", ""), item.get("details", ""))
    console.print(table)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reconforge", description="AI-assisted reconnaissance and security posture reporting.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover_parser = subparsers.add_parser("discover", help="Collect passive target metadata.")
    discover_parser.add_argument("target", help="Target URL or hostname.")
    discover_parser.add_argument("--json-out", dest="json_out", help="Optional JSON output path.")

    scan_parser = subparsers.add_parser("scan", help="Run passive security posture checks.")
    scan_parser.add_argument("target", help="Target URL or hostname.")
    scan_parser.add_argument("--json-out", dest="json_out", help="Optional JSON output path.")
    scan_parser.add_argument("--md-out", dest="md_out", help="Optional Markdown report path.")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "discover":
        result = discover(args.target)
        _print_json(result)
        if args.json_out:
            path = save_json_report(result, args.json_out)
            console.print(f"[green]Saved discovery report to {path}[/green]")
        return

    if args.command == "scan":
        result = scan(args.target)
        _print_findings(result)
        if args.json_out:
            path = save_json_report(result, args.json_out)
            console.print(f"[green]Saved JSON report to {path}[/green]")
        if args.md_out:
            path = save_markdown_report(result, args.md_out)
            console.print(f"[green]Saved Markdown report to {path}[/green]")
        return


if __name__ == "__main__":
    main()
