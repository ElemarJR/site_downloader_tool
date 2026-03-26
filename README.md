# site_downloader_tool

CLI utility to download an offline copy of a website, including JavaScript-rendered pages and captured assets.

This project was derived from the core downloader logic of:
- https://github.com/asimov-academy/Website-Downloader

The original project exposes a web UI. This version repackages the same idea as a command-line tool so it can be used directly as a utility.

## Features

- Download a site for offline viewing
- Render JavaScript pages using Playwright/Chromium
- Capture assets discovered during network activity
- Rewrite references for local usage
- Generate a ZIP file automatically

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Usage

```bash
python site_downloader_tool.py https://example.com
```

### Options

```bash
python site_downloader_tool.py https://example.com \
  --output-dir downloads \
  --name example-site \
  --keep-unzipped
```

### Help

```bash
python site_downloader_tool.py --help
```

## Output

By default the tool:
1. downloads the rendered site into a temporary folder under `downloads/`
2. creates a ZIP file with the site contents
3. removes the extracted folder unless `--keep-unzipped` is used

The final ZIP path is printed to stdout on success.
