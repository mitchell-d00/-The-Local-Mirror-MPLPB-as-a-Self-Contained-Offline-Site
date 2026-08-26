# MPLPB Local Web

A bounded, portable knowledge corpus that is an actual website — plain HTML files
in a directory, connected by relative links, starting at `index.html`. Open it in
a browser and it works. Point a crawler at it and it indexes. No server, no
database, no framework, no internet connection, no model training.

Reference implementation of **MPLPB-LOCAL-008 v4** (`docs/`).

## Three layers, kept separate

| Layer | What it is | Here |
|---|---|---|
| 1. Local web | Authoritative HTML + relative link graph | `site/` |
| 2. Crawler + index | Enumerates, parses, indexes | `tools/crawl.py`, `tools/search.py` |
| 3. Reasoning | Queries the index, answers from retrieved pages | your model |

The model never has to click through links. A crawler walks the graph; the model
queries what came out.

## Quick start

```bash
python3 tools/validate.py site            # 8 structural checks
python3 tools/crawl.py site -o out.jsonl  # crawl records, one JSON per page
python3 tools/search.py site "relative link"
python3 tools/search.py site --id LOCAL-SPEC-OLD-001   # retired page, by ID
```

Standard library only. No `pip install`.

## Three ingestion paths

The subtle part, and the reason the crawler is not just a link walker:

| Path | Source | Ingested? | Status |
|---|---|---|---|
| Graph | Reachable from `index.html` | yes | `current` |
| Retired | Under `_log/superseded/`, found by filesystem audit | yes | `retired` |
| Orphan | Unreachable and not superseded | **no** — reported as FM-L2 | — |

Retired pages are deliberately unlinked, so a graph-only crawl can never reach
them. If the filesystem audit is treated as maintenance-only, the corpus silently
loses its own history: it still validates, still crawls, still answers current
questions — and can no longer say what a document used to say. Orphans are the
opposite case: unlinked by accident, so they are reported rather than indexed.

Default retrieval filters to `status = current`. `--status any` and `--id`
lookups reach retired pages.

## Structure

```
site/
  index.html              Main Index — crawl root, boot block, category map
  BOOT.md                 plain-text twin of the boot block
  style.css
  _log/
    revisions.html        append-only change record
    superseded/           retired pages, never deleted
  spec/
    _index.html           Sub-Index with scope declaration
    link_discipline.html
  physics/
    _index.html
    heat_transfer.html
tools/
  validate.py             §11 checks 11.1–11.8
  crawl.py                bounded graph crawl + filesystem audit
  search.py               SQLite FTS5 index with status filtering
docs/
  MPLPB_Local_Web_v4.md   the specification
```

## Page metadata

Every page carries machine-readable fields the crawler reads directly:

```html
<meta name="mplpb:document-id" content="LOCAL-SPEC-001">
<meta name="mplpb:category"    content="Specification / Architecture">
<meta name="mplpb:updated"     content="2026-08-05T18:40Z v2">
<meta name="mplpb:scope"       content="What this page owns">
<meta name="mplpb:when-to-use" content="Trigger conditions; semicolon separated">
<meta name="mplpb:status"      content="current">
<meta name="mplpb:supersedes"  content="LOCAL-SPEC-OLD-001">
<link rel="index" href="../index.html">
<link rel="up"    href="./_index.html">
```

`updated` carries a time component, not just a date — three revisions in one
working day cannot otherwise be ordered. `supersedes` is a semicolon-separated
list of document IDs.

## Validator checks

1. **11.1** every local link target exists
2. **11.2** every current page reachable from `index.html`
3. **11.3** required metadata and `rel="index"` / `rel="up"` present
4. **11.4** no two current pages share a document ID
5. **11.5** supersession, status, and location agree
6. **11.6** no link resolves outside the corpus root
7. **11.7** every current page listed in its Sub-Index (or the Main Index)
8. **11.8** `updated` values parse and remain orderable

Exit code 1 on any failure, so it drops straight into CI. A workflow is included
at `.github/workflows/validate.yml`.

## Building your own

1. Copy `site/` and delete the example spokes.
2. Fill in the boot block in `index.html` and `BOOT.md`.
3. One directory per bounded domain, each with a scope declaration in
   `_index.html`.
4. Copy `spec/link_discipline.html` as your page template.
5. Run `validate.py` after every change.

To retire a page: move it to `_log/superseded/`, flip its status to `retired`,
name it in the replacement's `supersedes`, remove it from the Sub-Index, and add
a line to `revisions.html`. Never delete.

## What this does not claim

The corpus being crawlable does not establish that its claims are true, that a
model will consult it, that structure beats a flat pile of files, or that local
timestamps prove precedence. §14 of the spec states the falsifiers, including the
ablation test that would settle whether the structure contributes above storage.
That test has not been run.

## License

Add one before publishing. MIT or CC BY 4.0 both fit a specification plus
reference tooling.
