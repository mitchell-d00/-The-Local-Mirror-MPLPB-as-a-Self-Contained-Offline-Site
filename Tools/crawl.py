#!/usr/bin/env python3
"""
MPLPB local-web crawler. Standard library only.

    python3 tools/crawl.py site                 # records to stdout as JSONL
    python3 tools/crawl.py site -o records.jsonl

Implements the three ingestion paths of MPLPB-LOCAL-008 v4 §7.1:

  graph    reachable from index.html            -> ingested, status current
  retired  under _log/superseded/, audit-found  -> ingested, status retired
  orphan   unreachable and not superseded       -> NOT ingested, reported as FM-L2

Emits one JSON record per ingested page, per §5.2.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from html.parser import HTMLParser
from pathlib import Path

SUPERSEDED_DIR = "superseded"


class Page(HTMLParser):
    """Extract mplpb metadata, typed links, and visible text."""

    SKIP = {"script", "style", "head", "title"}

    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.title = ""
        self._chunks: list[str] = []
        self._skip_depth = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs) -> None:
        a = dict(attrs)
        if tag == "meta" and a.get("name", "").startswith("mplpb:"):
            self.meta[a["name"]] = a.get("content", "")
        if tag in ("link", "a") and a.get("href"):
            rels = (a.get("rel") or "").split() or [""]
            for r in rels:
                self.links.append({"rel": r.lower(), "href": a["href"]})
        if tag == "title":
            self._in_title = True
        if tag in self.SKIP:
            self._skip_depth += 1

    def handle_endtag(self, tag) -> None:
        if tag == "title":
            self._in_title = False
        if tag in self.SKIP and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data) -> None:
        if self._in_title:
            self.title += data.strip()
        elif not self._skip_depth:
            text = data.strip()
            if text:
                self._chunks.append(text)

    @property
    def text(self) -> str:
        return " ".join(self._chunks)


def parse(path: Path) -> Page:
    p = Page()
    p.feed(path.read_text(encoding="utf-8", errors="replace"))
    return p


def is_internal(href: str) -> bool:
    low = href.lower()
    return not low.startswith(("http://", "https://", "mailto:", "#", "data:"))


def inside(target: Path, root: Path) -> bool:
    """§4.3 crawl boundary: canonical path must remain inside the root."""
    try:
        target.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def split_ids(value: str) -> list[str]:
    return [p.strip() for p in value.split(";") if p.strip()]


def record(path: Path, root: Path, info: Page, discovered_by: str) -> dict:
    links = []
    for link in info.links:
        href = link["href"]
        if not is_internal(href):
            continue
        target = (path.parent / href.split("#")[0]).resolve()
        if not inside(target, root):
            continue
        links.append({
            "rel": link["rel"] or "link",
            "target": str(target.relative_to(root.resolve())),
        })
    return {
        "document_id": info.meta.get("mplpb:document-id", ""),
        "path": str(path.relative_to(root)),
        "title": info.title,
        "category": info.meta.get("mplpb:category", ""),
        "scope": info.meta.get("mplpb:scope", ""),
        "when_to_use": info.meta.get("mplpb:when-to-use", ""),
        "updated": info.meta.get("mplpb:updated", ""),
        "owner": info.meta.get("mplpb:owner", ""),
        "status": info.meta.get("mplpb:status", "current"),
        "supersedes": split_ids(info.meta.get("mplpb:supersedes", "")),
        "substrate": "local",
        "discovered_by": discovered_by,
        "links": links,
        "text": info.text,
    }


def crawl(root: Path) -> tuple[list[dict], list[str]]:
    root = root.resolve()
    entry = root / "index.html"
    if not entry.exists():
        raise SystemExit(f"no index.html at {root}")

    records: list[dict] = []
    orphans: list[str] = []

    # --- path 1: graph crawl from index.html (§6.1) -------------------------
    visited: set[Path] = set()
    queue = deque([entry.resolve()])
    while queue:
        current = queue.popleft()
        if current in visited or not inside(current, root):
            continue
        visited.add(current)
        info = parse(current)
        records.append(record(current, root, info, "graph"))
        for link in info.links:
            href = link["href"]
            if not is_internal(href):
                continue
            target = (current.parent / href.split("#")[0]).resolve()
            if target.suffix == ".html" and target.exists() and inside(target, root):
                if target not in visited:
                    queue.append(target)

    # --- paths 2 and 3: filesystem audit (§6.2, §7.1) -----------------------
    for path in sorted(root.rglob("*.html")):
        if path.resolve() in visited:
            continue
        if SUPERSEDED_DIR in path.relative_to(root).parts:
            info = parse(path)
            rec = record(path, root, info, "audit")
            rec["status"] = "retired"  # location is authoritative here
            records.append(rec)
        else:
            orphans.append(str(path.relative_to(root)))

    return records, orphans


def main() -> int:
    ap = argparse.ArgumentParser(description="Crawl an MPLPB local web.")
    ap.add_argument("root", nargs="?", default="site")
    ap.add_argument("-o", "--out", help="write JSONL here instead of stdout")
    args = ap.parse_args()

    records, orphans = crawl(Path(args.root))

    lines = "\n".join(json.dumps(r, ensure_ascii=False) for r in records)
    if args.out:
        Path(args.out).write_text(lines + "\n", encoding="utf-8")
    else:
        print(lines)

    graph = sum(1 for r in records if r["discovered_by"] == "graph")
    audit = sum(1 for r in records if r["discovered_by"] == "audit")
    print(
        f"\ningested {len(records)} page(s): {graph} via graph, {audit} retired via audit",
        file=sys.stderr,
    )
    if orphans:
        print(f"FM-L2  {len(orphans)} orphan(s) NOT ingested:", file=sys.stderr)
        for o in orphans:
            print(f"       {o}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
