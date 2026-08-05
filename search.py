#!/usr/bin/env python3
"""
MPLPB local-web search. Standard library only (sqlite3 FTS5).

    python3 tools/search.py site "relative link"
    python3 tools/search.py site "relative link" --status any     # include retired
    python3 tools/search.py site --id LOCAL-SPEC-OLD-001          # provenance lookup

Builds an in-memory index from tools/crawl.py output and queries it.

Default retrieval filters to status = current (§7.1). Retired pages remain
reachable by explicit --status any or by document ID, which is what keeps the
corpus able to answer what a document used to say. Every result carries its
document ID, path, scope, version, status, and substrate (§5.2, FM-L7, FM-L10).
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from crawl import crawl  # noqa: E402


def build(records: list[dict]) -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.execute(
        """CREATE VIRTUAL TABLE pages USING fts5(
               document_id, path, title, category, scope, when_to_use,
               updated, status, substrate, discovered_by, text
           )"""
    )
    db.executemany(
        "INSERT INTO pages VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        [
            (
                r["document_id"], r["path"], r["title"], r["category"], r["scope"],
                r["when_to_use"], r["updated"], r["status"], r["substrate"],
                r["discovered_by"], r["text"],
            )
            for r in records
        ],
    )
    return db


def show(rows) -> None:
    if not rows:
        print("no results")
        return
    for doc_id, path, title, scope, updated, status, substrate in rows:
        flag = "" if status == "current" else f"  [{status.upper()}]"
        print(f"\n{title}{flag}")
        print(f"  id       {doc_id}")
        print(f"  path     {path}  ({substrate})")
        print(f"  scope    {scope}")
        print(f"  version  {updated}")


COLS = "document_id, path, title, scope, updated, status, substrate"


def main() -> int:
    ap = argparse.ArgumentParser(description="Search an MPLPB local web.")
    ap.add_argument("root", nargs="?", default="site")
    ap.add_argument("query", nargs="?", help="FTS5 query string")
    ap.add_argument("--id", help="look up one document ID, any status")
    ap.add_argument(
        "--status", choices=["current", "any"], default="current",
        help="default 'current'; 'any' includes retired pages",
    )
    ap.add_argument("-n", "--limit", type=int, default=5)
    args = ap.parse_args()

    if not args.query and not args.id:
        ap.error("give a query or --id")

    records, orphans = crawl(Path(args.root))
    db = build(records)

    if args.id:
        # Provenance lookup ignores the status filter by design.
        rows = db.execute(
            f"SELECT {COLS} FROM pages WHERE document_id = ?", (args.id,)
        ).fetchall()
        show(rows)
    else:
        sql = f"SELECT {COLS} FROM pages WHERE pages MATCH ?"
        params: list = [args.query]
        if args.status == "current":
            sql += " AND status = 'current'"
        sql += " ORDER BY rank LIMIT ?"
        params.append(args.limit)
        show(db.execute(sql, params).fetchall())

    if orphans:
        print(f"\nFM-L2  {len(orphans)} orphan(s) excluded from the index", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
