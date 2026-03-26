#!/usr/bin/env python3
"""CLI utility to download an offline copy of a website.

Reuses the core downloader logic from the Asimov Academy Website Downloader
project, replacing the original web UI with a command-line interface.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from downloader import WebsiteDownloader, get_site_name, zip_directory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="site_downloader_tool",
        description="Download an offline copy of a website, including rendered JS assets.",
    )
    parser.add_argument("url", help="Target site URL")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="downloads",
        help="Directory where the extracted site and zip file will be written",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Optional base name for the output folder/zip. Defaults to the site name.",
    )
    parser.add_argument(
        "--keep-unzipped",
        action="store_true",
        help="Keep the downloaded folder after creating the ZIP file",
    )
    parser.add_argument(
        "--no-zip",
        action="store_true",
        help="Do not create a ZIP file; keep only the downloaded folder",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce console output to errors only",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    output_root = Path(args.output_dir).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    site_name = args.name or get_site_name(args.url)
    download_dir = output_root / site_name
    zip_path = output_root / f"{site_name}.zip"

    def logger(message: str) -> None:
        if not args.quiet:
            print(message)

    logger(f"🌐 Downloading: {args.url}")
    logger(f"📁 Output folder: {download_dir}")

    try:
        downloader = WebsiteDownloader(args.url, str(download_dir), log_callback=logger)
        success = downloader.process()
    except KeyboardInterrupt:
        print("\n⛔ Download interrupted by user.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"❌ Fatal error: {exc}", file=sys.stderr)
        return 1

    if not success:
        print("❌ Failed to download website.", file=sys.stderr)
        return 1

    logger(f"✅ Site downloaded to: {download_dir}")

    if not args.no_zip:
        logger(f"📦 Creating ZIP: {zip_path}")
        zip_directory(str(download_dir), str(zip_path))
        logger(f"✅ ZIP created: {zip_path}")
        if not args.keep_unzipped:
            import shutil

            shutil.rmtree(download_dir)
            logger(f"🧹 Removed extracted folder: {download_dir}")

    print(str(zip_path if not args.no_zip else download_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
