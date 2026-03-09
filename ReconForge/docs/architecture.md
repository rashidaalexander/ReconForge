# Architecture

ReconForge is organized around three primary flows:

1. Discovery: collects passive metadata from a target.
2. Scan: evaluates basic security posture signals without exploitation.
3. Reporting: exports findings to JSON and Markdown.

## Pipeline

Target -> HTTP Collector -> Discovery/Scan Engine -> Report Renderer
