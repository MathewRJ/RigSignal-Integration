#!/usr/bin/env python3
"""
Generate a static EPR (Elastic Package Registry) directory structure for
GitHub Pages hosting.

Usage: python scripts/generate-epr-index.py <version> <base_url>
  version:  package version, e.g. 0.1.1
  base_url: GitHub Pages base URL, e.g. https://MathewRJ.github.io/RigSignal-Integration

Output layout (written to dist/):
  dist/search                              <- EPR search endpoint (static JSON)
  dist/package/rigsignal/{v}/             <- package metadata
  dist/epr/rigsignal/rigsignal-{v}.zip   <- package zip (copied from build/)
"""

import json
import shutil
import sys
from pathlib import Path

import yaml  # PyYAML

REPO_ROOT = Path(__file__).parent.parent
DIST = REPO_ROOT / "dist"


def load_manifest() -> dict:
    with open(REPO_ROOT / "manifest.yml") as f:
        return yaml.safe_load(f)


def package_descriptor(m: dict, version: str, base_url: str) -> dict:
    return {
        "name": m["name"],
        "title": m["title"],
        "version": version,
        "description": m["description"].strip(),
        "type": m["type"],
        "categories": m.get("categories", []),
        "conditions": m.get("conditions", {}),
        "owner": m.get("owner", {}),
        "icons": [
            {
                "src": f"{base_url}/package/{m['name']}/{version}/{icon['src']}",
                "title": icon.get("title", m["title"]),
                "type": icon.get("type", "image/svg+xml"),
            }
            for icon in m.get("icons", [])
        ],
        "download": f"/epr/{m['name']}/{m['name']}-{version}.zip",
        "path": f"/package/{m['name']}/{version}",
    }


def build_epr(version: str, base_url: str) -> None:
    m = load_manifest()
    pkg_name = m["name"]

    DIST.mkdir(exist_ok=True)

    # --- search endpoint ---
    search_dir = DIST / "search"
    search_dir.mkdir(exist_ok=True)
    descriptor = package_descriptor(m, version, base_url)
    # Fleet hits /search with query params; static hosting returns all packages
    # and Fleet filters client-side.
    with open(search_dir / "index.json", "w") as f:
        json.dump([descriptor], f, indent=2)
    # Also write it at /search directly (some Fleet versions hit the bare path)
    shutil.copy(search_dir / "index.json", DIST / "search.json")

    # --- package metadata ---
    pkg_dir = DIST / "package" / pkg_name / version
    pkg_dir.mkdir(parents=True, exist_ok=True)
    with open(pkg_dir / "manifest.json", "w") as f:
        json.dump(descriptor, f, indent=2)

    # Copy icon so it's accessible at the versioned path
    icon_src = REPO_ROOT / "img" / "icon.svg"
    if icon_src.exists():
        icon_dst = pkg_dir / "img"
        icon_dst.mkdir(exist_ok=True)
        shutil.copy(icon_src, icon_dst / "icon.svg")

    # --- package zip ---
    zip_src_candidates = [
        REPO_ROOT / "build" / "packages" / f"{pkg_name}-{version}.zip",
        REPO_ROOT / "build" / "packages" / f"{pkg_name}-{version}.zip",
    ]
    zip_src = next((p for p in zip_src_candidates if p.exists()), None)
    if zip_src is None:
        raise FileNotFoundError(
            f"Package zip not found. Run 'elastic-package build' first.\n"
            f"Looked in: {[str(p) for p in zip_src_candidates]}"
        )
    zip_dst = DIST / "epr" / pkg_name
    zip_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy(zip_src, zip_dst / f"{pkg_name}-{version}.zip")

    print(f"EPR structure written to {DIST}/")
    print(f"  search:   {DIST}/search.json")
    print(f"  metadata: {pkg_dir}/manifest.json")
    print(f"  zip:      {zip_dst}/{pkg_name}-{version}.zip")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <version> <base_url>")
        sys.exit(1)
    build_epr(version=sys.argv[1], base_url=sys.argv[2].rstrip("/"))
