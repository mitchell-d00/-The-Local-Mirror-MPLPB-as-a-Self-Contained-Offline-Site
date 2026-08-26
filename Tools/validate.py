#!/usr/bin/env python3
"""
MPLPB local-web validator. Standard library only.

    python3 tools/validate.py site

Implements the eight checks in MPLPB-LOCAL-008 v4 §11:

  11.1  link validity              every local target exists
  11.2  root reachability          every current page reachable from index.html
  11.3  required metadata          every page declares the required fields
  11.4  unique document identity   no two current pages share a document ID
  11.5  supersession consistency   supersedes/status/location agree
  11.6  boundary safety            no link resolves outside the root
  11.7  index consistency          every current page listed in its parent index
  11.8  timestamp ordering         updated values parse and are orderable

Exit 0 when clean, 1 when any check fails.
"""

from __future__ import annotations

import re
import sys
from collections import deque
from html.parser import HTMLParser
from pathlib import Path

REQUIRED_META = [
    "mplpb:document-id",
    "mplpb:category",
    "mplpb:updated",
    "mplpb:scope",
    "mplpb:when-to-use",
    "mplpb:status",
]

SUPERSEDED_DIR = "superseded"

# ISO 8601 with timezone, a space, then a version token: 2026-08-05T18:40Z v2
UPDATED_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?(Z|[+-]\d{2}:?\d{2})\s+v\d+$"
)


class Page(HTMLParser):
    """Extract mplpb meta fields, rel values, and internal hrefs."""

    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, str] = {}
        self.rels: set[str] = set()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        a = dict(attrs)
        if tag == "meta" and a.get("name", "").startswith("mplpb:"):
            self.meta[a["name"]] = a.get("content", "")
        if tag in ("link", "a"):
            for r in (a.get("rel") or "").split():
                self.rels.add(r.lower())
            href = a.get("href")
            if href:
                self.hrefs.append(href)


def load(path: Path) -> Page:
    p = Page()
    p.feed(path.read_text(encoding="utf-8", errors="replace"))
    return p


def is_internal(href: str) -> bool:
    low = href.lower()
    return not low.startswith(("http://", "https://", "mailto:", "#", "data:"))


def split_ids(value: str) -> list[str]:
    """mplpb:supersedes is a semicolon-separated list of document IDs (§5.1)."""
    return [part.strip() for part in value.split(";") if part.strip()]


def retired_location(path: Path, root: Path) -> bool:
    return SUPERSEDED_DIR in path.relative_to(root).parts


def validate(root: Path) -> int:
    entry = root / "index.html"
    if not entry.exists():
        print(f"FAIL  no index.html at {root}")
        return 1

    pages = sorted(root.rglob("*.html"))
    parsed = {p: load(p) for p in pages}
    fails: list[str] = []

    def rel(p: Path) -> str:
        return str(p.relative_to(root))

    # ---- 11.1 link validity, 11.6 boundary safety --------------------------
    for page, info in parsed.items():
        for href in info.hrefs:
            if not is_internal(href):
                continue
            if href.startswith("/") or href.lower().startswith("file:"):
                fails.append(f"11.1  {rel(page)}: non-relative link -> {href}")
                continue
            target = (page.parent / href.split("#")[0]).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                fails.append(f"11.6  {rel(page)}: link escapes root -> {href}")
                continue
            if not target.exists():
                fails.append(f"11.1  {rel(page)}: broken link -> {href}")

    # ---- 11.3 required metadata + upward links -----------------------------
    for page, info in parsed.items():
        for field in REQUIRED_META:
            if not info.meta.get(field):
                fails.append(f"11.3  {rel(page)}: missing {field}")
        status = info.meta.get("mplpb:status", "")
        if status and status not in ("current", "retired"):
            fails.append(f"11.3  {rel(page)}: status must be current|retired, got '{status}'")
        if page != entry:
            for required in ("index", "up"):
                if required not in info.rels:
                    fails.append(f'11.3  {rel(page)}: missing rel="{required}"')

    # ---- 11.8 timestamp ordering -------------------------------------------
    for page, info in parsed.items():
        updated = info.meta.get("mplpb:updated", "")
        if updated and not UPDATED_RE.match(updated):
            fails.append(
                f"11.8  {rel(page)}: updated '{updated}' is not "
                "'<ISO8601 with timezone> v<n>'"
            )

    # ---- 11.4 unique document identity among current pages -----------------
    by_id: dict[str, list[Path]] = {}
    for page, info in parsed.items():
        if info.meta.get("mplpb:status") != "current":
            continue
        doc_id = info.meta.get("mplpb:document-id")
        if doc_id:
            by_id.setdefault(doc_id, []).append(page)
    for doc_id, holders in by_id.items():
        if len(holders) > 1:
            joined = ", ".join(rel(h) for h in holders)
            fails.append(f"11.4  duplicate current document ID {doc_id}: {joined}")

    # ---- 11.2 root reachability (current pages only) -----------------------
    seen = {entry.resolve()}
    queue = deque([entry])
    while queue:
        page = queue.popleft()
        for href in parsed[page].hrefs:
            if not is_internal(href):
                continue
            target = (page.parent / href.split("#")[0]).resolve()
            if target.suffix != ".html" or not target.exists():
                continue
            if target not in seen and target in parsed:
                seen.add(target)
                queue.append(target)

    for page, info in parsed.items():
        if retired_location(page, root):
            continue  # checked by 11.5 instead
        if page.resolve() not in seen:
            fails.append(f"11.2  {rel(page)}: orphan, unreachable from index.html")

    # ---- 11.5 supersession consistency -------------------------------------
    retired_ids = {
        info.meta.get("mplpb:document-id"): page
        for page, info in parsed.items()
        if info.meta.get("mplpb:status") == "retired"
    }
    for page, info in parsed.items():
        # status and location must agree, both directions
        status = info.meta.get("mplpb:status")
        in_superseded = retired_location(page, root)
        if status == "retired" and not in_superseded:
            fails.append(f"11.5  {rel(page)}: status retired but not under _log/{SUPERSEDED_DIR}/")
        if in_superseded and status != "retired":
            fails.append(f"11.5  {rel(page)}: under _log/{SUPERSEDED_DIR}/ but status is '{status}'")
        # every superseded ID resolves to a retired page
        for dead_id in split_ids(info.meta.get("mplpb:supersedes", "")):
            if dead_id not in retired_ids:
                fails.append(
                    f"11.5  {rel(page)}: supersedes {dead_id}, which is not a retired page"
                )
        # retired pages must not be linked from a live index
        if page.name.startswith("_index") or page == entry:
            for href in info.hrefs:
                if not is_internal(href):
                    continue
                target = (page.parent / href.split("#")[0]).resolve()
                tgt_info = parsed.get(target)
                if tgt_info and tgt_info.meta.get("mplpb:status") == "retired":
                    fails.append(f"11.5  {rel(page)}: active index links retired page {href}")

    # ---- 11.7 index consistency --------------------------------------------
    for page, info in parsed.items():
        if page == entry or page.name.startswith("_index"):
            continue
        if retired_location(page, root) or info.meta.get("mplpb:status") == "retired":
            continue
        # A page inside a spoke must be listed in that spoke's Sub-Index.
        # A page outside any spoke (e.g. _log/revisions.html) must instead be
        # linked directly from the Main Index -- otherwise it has no declared
        # parent at all.
        parent = page.parent / "_index.html"
        holder = parent if parent.exists() else entry
        listed = any(
            (holder.parent / h.split("#")[0]).resolve() == page.resolve()
            for h in parsed[holder].hrefs
            if is_internal(h)
        )
        if not listed:
            fails.append(f"11.7  {rel(page)}: not listed in {rel(holder)}")

    # ---- report -------------------------------------------------------------
    current = sum(1 for i in parsed.values() if i.meta.get("mplpb:status") == "current")
    retired = sum(1 for i in parsed.values() if i.meta.get("mplpb:status") == "retired")
    print(f"validated {len(pages)} page(s) under {root}  ({current} current, {retired} retired)")

    if fails:
        for f in sorted(fails):
            print("  FAIL  " + f)
        print(f"\n{len(fails)} problem(s)")
        return 1

    print("  OK    11.1–11.8 all clean")
    return 0


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve()
    if not root.is_dir():
        print(f"FAIL  {root} is not a directory")
        return 1
    return validate(root)


if __name__ == "__main__":
    sys.exit(main())
