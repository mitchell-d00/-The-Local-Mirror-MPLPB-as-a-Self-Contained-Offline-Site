Category: Specification / Architecture
Subcategory: Knowledge Infrastructure / Local Substrate
Document ID: MPLPB-LOCAL-008
Last Updated: 2026-08-05T18:40Z v4
Owner: Mitchell D. McPhetridge
Supersedes: MPLPB-LOCAL-008 v3 (2026-08-05T14:00Z), v2 (2026-08-05T11:20Z), v1 (2026-08-05T09:15Z)

Summary: This paper specifies a local version of Multi-Platform Linked Public
Building as a self-contained website stored in an ordinary directory. The site
consists of plain HTML files connected by relative links, beginning at
index.html. A browser can open it for human navigation, while a local crawler can
enumerate the same pages, extract their metadata and links, and place their
contents into an MPLPB-compatible retrieval index. The local web is the source
substrate; the crawler and index are separate components. No server, database,
framework, internet connection, or model training is required.

When to use this document:

- Building an MPLPB from private, unpublished, proprietary, or local material
- Giving a crawler a bounded local website to enumerate and index
- Creating a portable MPLPB that works from a folder, archive, external drive, or
  synchronized directory
- Converting an existing collection of documents into a linked local web
- Testing MPLPB navigation, retrieval, and structure without publishing the
  corpus

Scope / Exclusions:

- This document specifies the local website and the contract by which a crawler
  reads it.
- It does not require the language model itself to follow hyperlinks manually.
- It does not claim that local retrieval demonstrates public recoverability,
  independent replication, public precedence, or third-party validation.
- It does not specify a complete search backend. The Rabbit Hole indexer supplies
  the adapter, parsing, indexing, and retrieval layers.
- It does not require semantic search. A file crawler and ordinary text index are
  sufficient for the minimal implementation.

Related documents:

- MPLPB v3 — complete artifacts, Main Index, Sub-Indexes, revision discipline,
  and reconstruction rules
- Rabbit Hole Internet Indexer Blueprint v2 — source adapters, indexing,
  chunking, metadata extraction, and hybrid retrieval
- Externalized Continuity at Scale — Navigator loop, complete artifacts, and mode
  control
- Spinning v2 — use of the retrieved graph as the model's working knowledge
  source
- MPLPB Separation & Precedence v1 — spoke boundaries and routing by declared
  scope
- The Five-Module Combinator — interface contract between MPLPB, Rabbit Hole,
  Navigator, Spinning, and the deployed companion

Back to: Main Index > Specification / Architecture Sub-Index

---

# MPLPB as a Local Web

## A Plain HTML Substrate for Local Crawling and Retrieval

Mitchell D. McPhetridge
Independent Researcher
August 2026
Version 4

---

## Abstract

Multi-Platform Linked Public Building was developed as a way to place continuity
in artifacts rather than in a single AI session. Its public form uses published,
cross-linked documents that search-capable systems can recover from the web.

The local form is simpler.

A local MPLPB is a small website stored in a directory. It begins at index.html.
Every page is an ordinary HTML file. Every internal connection is a relative
hyperlink. Each subject area has a Sub-Index, each operational page declares what
it contains and when it should be used, and each page links back toward the
indexes above it.

A local crawler starts at index.html, follows the allowed local links, extracts
page text and metadata, records the link graph, and sends the resulting documents
to a text or hybrid-search index. The language model does not need to behave like
a browser or manually click through the site. It queries the index built from the
site.

The architecture therefore has three distinct layers:

1. The local web: authoritative HTML files and their relative link graph.
2. The crawler and indexer: the Rabbit Hole adapter that enumerates, parses, and
   indexes the web.
3. The reasoning interface: an AI system that retrieves the indexed pages and
   answers from them.

This paper specifies the first layer and its interface with the second. Its claim
is deliberately narrow: plain local HTML is a suitable source format for an
MPLPB-compatible crawler.

---

## 1. The Requirement

The requirement is not to create a new model, a new browser, or a complex
knowledge platform.

The requirement is:

**Build a local web that an MPLPB-compatible crawler can crawl.**

The local web must be:

- readable by a normal browser;
- readable as plain text and HTML by a crawler;
- portable between machines;
- usable without an internet connection;
- understandable from a declared entry point;
- bounded so that the crawler does not leave the corpus;
- structured enough to expose scope, versions, relationships, and supersessions;
- independent of a particular search engine, vector database, model vendor, or
  operating system.

Plain HTML with relative links satisfies these requirements.

HTML already provides the necessary primitives: pages, links, metadata, headings,
document titles, typed relationships, machine-readable structure, and
human-readable rendering.

A local MPLPB does not simulate a website. It is a website whose address space
happens to be a local directory rather than a public domain.

---

## 2. The Three-Layer Architecture

The local system should not blur storage, crawling, retrieval, and reasoning into
one component.

### 2.1 Layer One: The Local Web

The local web is the authoritative corpus.

It contains index.html; one directory per spoke or subject domain; one
_index.html inside each spoke; operational HTML documents; a revision log; a
superseded-document directory; one shared stylesheet; and optionally a plain-text
boot file.

The local web owns document content, document identity, scope declarations,
version information, relationships, navigation, supersession, and corpus
boundaries.

It does not own search ranking, embeddings, model behavior, or answer generation.

### 2.2 Layer Two: The Crawler and Index

The crawler is a Rabbit Hole source adapter pointed at the local root.

It performs a bounded traversal:

1. Open index.html.
2. Extract internal links.
3. Resolve each link relative to the current file.
4. Reject links outside the declared root.
5. Visit each reachable HTML page once.
6. Extract metadata, text, and outgoing relationships.
7. Record the link graph.
8. Send the resulting page records to the selected index.

The index may be a simple filename and full-text index, a SQLite search database,
a keyword index, a vector index, a hybrid keyword and semantic index, or another
implementation behind the Rabbit Hole adapter contract.

The local-web format does not depend on which index is selected.

### 2.3 Layer Three: The Reasoning Interface

The reasoning system queries the index rather than depending on its own
parametric memory.

A request may be routed by exact document ID, title, category, scope, trigger
condition, keyword, semantic similarity, graph relationship, or version status.

Retrieved pages are then supplied to the model as answer material.

Spinning may impose a no-shortcut rule requiring substantive answers to be
grounded in retrieved corpus material. Externalized Continuity may apply routing
and mode-control rules. Those are runtime layers above the local web.

The local website remains useful without either one.

---

## 3. Directory Layout

A minimal local MPLPB may use the following structure:

```
mplpb-local/
  index.html
  style.css
  BOOT.md
  _log/
    revisions.html
    superseded/
      old_layout.html
  spec/
    _index.html
    mirror_layout.html
  physics/
    _index.html
    heat_transfer.html
  gardening/
    _index.html
    sowing_windows.html
```

The names are examples. The structural roles are the requirement.

### 3.1 Root Index

index.html is the crawl entry point and Main Index.

It should contain the name and purpose of the corpus; the current version; the
root scope; the category map; links to every active Sub-Index; links to the
revision log; crawler boundary information; and any read-first or reconstruction
instructions.

The root should be a map, not a long essay.

### 3.2 Spoke Directories

Each top-level domain receives its own directory — `/spec/`, `/physics/`,
`/gardening/`, `/legal/`, `/game-system/`.

Each directory is an MPLPB spoke. Its _index.html declares the domain it owns and
lists its active documents.

### 3.3 Operational Documents

Operational pages contain the actual specifications, policies, guides, research
notes, procedures, or reference material.

Every operational page should be reachable from its parent _index.html.

A file that exists on disk but cannot be reached from index.html is an orphan.
The crawler may still discover it through a filesystem scan, but it is not part
of the declared local web until an index links to it.

### 3.4 Revision Material

The `_log/` directory records changes. Retired pages move to
`_log/superseded/`. The replacement page names the retired document in its
supersession metadata. The active indexes should point to current pages, not
superseded ones.

How retired pages nevertheless reach the index is specified in §7.1. They are not
simply dropped.

---

## 4. Link Discipline

Relative links are the central portability rule.

Use:

```html
<a href="../spec/mirror_layout.html">Mirror layout</a>
```

Do not use:

```html
<a href="file:///Users/name/Desktop/mplpb/spec/mirror_layout.html">
```

Do not use machine-specific absolute filesystem paths.

A relative link survives when the corpus is moved, renamed, zipped, copied to
another machine, placed on removable storage, synchronized into another
directory, or served later by a local or public web server.

### 4.1 Required Upward Links

Every page should declare its Main Index and parent:

```html
<link rel="index" href="../index.html">
<link rel="up" href="./_index.html">
```

The body should also expose human-visible navigation:

```html
<nav class="related">
  <a rel="up" href="./_index.html">Back to: Specification Sub-Index</a>
  <a rel="index" href="../index.html">Main Index</a>
</nav>
```

### 4.2 Related Links

Related pages may be identified with:

```html
<a rel="related" href="./continuity.html">Externalized Continuity</a>
```

These links become graph edges when the crawler parses the page.

### 4.3 Crawl Boundary

The crawler must treat the local root as a hard boundary. If the root is
`/path/to/mplpb-local/`, then a resolved link may be crawled only if its
canonical path remains inside that root.

This prevents a malformed link such as `<a href="../../../private-file.html">`
from causing the crawler to index unrelated material.

External http:// or https:// links may be recorded as references, but the local
crawl should not follow them unless an explicit hybrid-crawl mode is enabled.

---

## 5. Page Metadata

Each page should carry machine-readable metadata in its `<head>`.

A minimal operational page:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Mirror Layout — MPLPB Local</title>
  <meta name="mplpb:document-id" content="LOCAL-SPEC-001">
  <meta name="mplpb:category" content="Specification / Architecture">
  <meta name="mplpb:updated" content="2026-08-05T18:40Z v1">
  <meta name="mplpb:owner" content="Mitchell D. McPhetridge">
  <meta name="mplpb:scope"
        content="File layout and relative-link rules for the local web">
  <meta name="mplpb:when-to-use"
        content="Adding, moving, validating, or repairing a page">
  <meta name="mplpb:status" content="current">
  <meta name="mplpb:supersedes" content="">
</head>
```

The crawler should extract these fields directly rather than attempting to infer
them from prose.

### 5.1 Field Formats

Field formats are pinned so that validators and crawlers agree.

| Field | Format |
|---|---|
| `document-id` | Single token, unique among current pages, uppercase with hyphens |
| `category` | Free text |
| `updated` | ISO 8601 timestamp with timezone, then a space, then `v<n>` |
| `owner` | Free text |
| `scope` | One sentence naming what this page owns |
| `when-to-use` | Semicolon-separated trigger conditions |
| `status` | `current` or `retired` — required on every page |
| `supersedes` | Semicolon-separated list of document IDs; empty string when none |

**On `updated`:** a date alone is insufficient. Three versions of a document
revised in one working day cannot be ordered from a date, and ordering is exactly
what revision discipline depends on. The timestamp carries a time component.

**On `supersedes`:** the HTML value is a string; the crawl record parses it into
an array by splitting on `;` and trimming. A single value and a list use the same
syntax, so the validator never has to guess.

**On `status`:** this field is what makes §7.1 possible. Without it a retired page
and a current page are indistinguishable once their text is in an index.

### 5.2 Crawl Record

A normalized crawl record may contain:

```json
{
  "document_id": "LOCAL-SPEC-001",
  "path": "spec/mirror_layout.html",
  "title": "Mirror Layout — MPLPB Local",
  "category": "Specification / Architecture",
  "scope": "File layout and relative-link rules for the local web",
  "when_to_use": "Adding, moving, validating, or repairing a page",
  "updated": "2026-08-05T18:40Z v1",
  "owner": "Mitchell D. McPhetridge",
  "status": "current",
  "supersedes": [],
  "substrate": "local",
  "discovered_by": "graph",
  "links": [
    { "rel": "up", "target": "spec/_index.html" },
    { "rel": "index", "target": "index.html" }
  ],
  "text": "Extracted visible page text..."
}
```

The HTML is authoritative. The crawl record is derived.

`substrate` is set to `local` on every record produced by this adapter. It exists
so that a citation generated downstream can state that the source is a local
document rather than a published one (FM-L10).

`discovered_by` records which ingestion path found the page — `graph` or `audit`
— and is specified in §7.1.

---

## 6. The Crawler Contract

The Rabbit Hole blueprint defines a source adapter around operations such as
`list()`, `read()`, and `get_metadata()`.

For the local web, the adapter may expose:

```
open_root()
read_page(path)
extract_metadata(path)
extract_links(path)
resolve_link(source, href)
is_inside_root(path)
```

The crawler does not need a full browser engine if the pages contain static HTML.
It should not require JavaScript execution, client-side rendering, login state,
remote fonts, framework bundles, API calls, generated routes, or a database.

### 6.1 Minimal Crawl Algorithm

```
queue = ["index.html"]
visited = empty set
while queue is not empty:
    current = remove first item from queue
    if current is already visited:
        continue
    if current is outside the root:
        reject it
        continue
    page = read current
    metadata = extract MPLPB fields
    text = extract visible document text
    links = extract href and rel values
    emit page record with discovered_by = "graph"
    mark current visited
    for each local HTML link:
        target = resolve relative to current
        if target is inside root and not visited:
            add target to queue
```

This is enough to enumerate the declared graph.

### 6.2 Crawl Modes

Two modes are useful, and they produce different things.

**Graph crawl.** Starts from index.html and follows links. This identifies the
declared MPLPB — what the corpus says it currently is.

**Filesystem audit.** Lists every supported file beneath the root and compares it
with the graph crawl. This identifies orphan pages, unreachable pages, missing
index entries, stale files, and accidental duplicates.

The graph crawl is retrieval infrastructure. The filesystem audit is *both*
maintenance infrastructure and — for retired pages only — a second ingestion
path. See §7.1. Earlier versions of this document said the audit was maintenance
only; that was wrong, and the consequence is described below.

---

## 7. Indexing

The crawler emits one record per page.

For small corpora, indexing the whole page is acceptable. For larger pages, the
indexer may split the text into chunks while retaining the page-level metadata on
every chunk.

A chunk record should preserve source path, document ID, title, category, scope,
version, status, chunk number, parent-page link, and relationship edges.

This allows retrieval to return a relevant passage without losing its document
identity.

Keyword indexing is sufficient for the minimum local system. Hybrid retrieval may
combine exact keyword matching, filename matching, metadata filtering, semantic
similarity, and graph expansion. Semantic retrieval is an improvement, not a
requirement for the local web to exist.

### 7.1 Three Ingestion Paths, Not Two

There is a defect in the naive reading of §3.4 and §6.2 together, and it is worth
stating plainly because it silently destroys a capability the corpus claims.

Retired pages live in `_log/superseded/`. By design, no active index links to
them — that is what retirement means. Therefore the graph crawl, which follows
links from index.html, **cannot reach them**. If the filesystem audit is treated
as maintenance-only, retired pages are never indexed at all. FM-L6 then requires
that retrieval "exclude retired pages by default," but there is nothing to
exclude: absent and excluded-by-default become indistinguishable, and the corpus
loses the ability to answer *what did this document used to say, and when did it
change*.

The specification is therefore three ingestion paths:

1. **Graph path.** Pages reachable from index.html. Ingested with
   `discovered_by: "graph"` and `status: "current"`. These are the default
   retrieval set.
2. **Retired path.** Pages under `_log/superseded/` found by the filesystem
   audit. Ingested with `discovered_by: "audit"` and `status: "retired"`.
   Excluded from default retrieval; available to explicit provenance queries and
   to any query that names a document ID directly.
3. **Orphan path.** Files outside `_log/superseded/` that the audit finds and the
   graph crawl did not reach. These are **not ingested**. They are reported as
   FM-L2 defects. An orphan is a maintenance failure, not a document class.

The distinction between path 2 and path 3 is the whole point. A page in
`superseded/` is deliberately unlinked; a page anywhere else that is unlinked is
an accident. Treating them identically either floods the index with abandoned
drafts or discards the revision history.

Default retrieval filter: `status = "current"`. Provenance retrieval:
`status = any`, with the status surfaced in every returned record.

---

## 8. Routing by Scope

MPLPB Separation & Precedence treats each bounded domain as a spoke and the
routing layer as the spinner.

In the local web the root index.html is the top-level routing map; each directory
is a spoke; each _index.html declares the spoke's scope; the crawler records
those scope declarations; and the retrieval layer uses them as ranking or
filtering signals.

For a clearly scoped request, retrieval should prefer the owning spoke. A
question about link validation belongs to `spec/`; a question about heat transfer
belongs to `physics/`; a question about sowing dates belongs to `gardening/`.

### 8.1 Cross-Domain Requests: Retrieval and Answering Are Different Layers

A cross-domain request may retrieve from more than one spoke. This does not
license a cross-domain answer, and the difference is where an implementer is most
likely to introduce the failure SEP-007 §5 names as a silent cross-domain guess.

The two layers have different rules:

- **Retrieval layer.** May return results from multiple spokes. Must preserve the
  source scope of each result rather than flattening the corpus into one
  undifferentiated collection. Returning material from two spokes is not an
  error.
- **Answering layer.** When no single spoke's declared scope cleanly owns the
  query, the hub does not pick one and does not blend them. It reports which
  spokes were touched and asks the user to narrow — "do you want the physics of
  heat transfer in soil, or the gardening guidance on when to sow?" — then routes
  the clarified query.

Retrieval breadth followed by an answering-layer clarification is the correct
behavior. Retrieval breadth followed by a merged answer is the false-merger
failure mode arriving through the back door.

Scope helps route. It does not determine truth.

---

## 9. Booting a Stateless Session

The local web may include a short boot block in index.html and an optional
BOOT.md copy.

The boot block should state what the corpus is; where the authoritative root is;
that answers about the corpus should use crawled or retrieved pages; how
categories are divided; which version is current; where revisions and
supersessions are recorded; and which runtime rules apply.

The boot file is not the crawler. Its purpose is to orient a human or AI
interface after the local web has been mounted or indexed.

A minimal instruction is:

> Treat index.html as the root of this corpus. Retrieve relevant local pages
> before answering corpus-dependent questions. Prefer current documents reachable
> from the Main Index. Preserve document IDs, scope, version, and supersession
> status in retrieval. Cite retrieved pages as local documents, not published
> ones.

---

## 10. What the Local Web Does Not Claim

The local web provides a source substrate.

It does not, by itself, establish:

- that a model will voluntarily follow the Main Index;
- that semantic retrieval will return the correct page;
- that the corpus's claims are true;
- that the corpus is independently recoverable by strangers;
- that filesystem dates establish public precedence;
- that a link graph improves answer quality;
- that a structured corpus outperforms unstructured files;
- that a retrieved page was actually used in the answer.

Those are separate questions requiring separate tests.

The narrow claim here is only:

**A bounded directory of static HTML pages with relative links and MPLPB metadata
can be crawled, indexed, moved, inspected, and used as the local source layer of
the broader architecture.**

---

## 11. Validation and Maintenance

A local-web validator should perform at least the following checks. All are
mechanical and should be performed by a script rather than left to memory. The
reference implementation is `tools/validate.py` in the accompanying repository.

**11.1 Link validity.** Every local target exists.

**11.2 Root reachability.** Every active page is reachable from index.html.
Pages under `_log/superseded/` are exempt and are checked by 11.5 instead.

**11.3 Required metadata.** Every operational page declares document ID,
category, updated version, scope, when-to-use, status, index link, and up link.

**11.4 Unique document identity.** No two pages with `status: current` share a
document ID. Retired pages may share an ID with the current page that replaced
them — that is the point of an ID — but no two *current* pages may.

**11.5 Supersession consistency.** Every document ID named in a `supersedes`
field resolves to a page that exists under `_log/superseded/` and carries
`status: retired`; no page under `_log/superseded/` is listed in an active index;
and no page carrying `status: retired` sits outside `_log/superseded/`.

**11.6 Boundary safety.** No followed path resolves outside the corpus root.

**11.7 Index consistency.** Each current operational page appears in its parent
_index.html.

**11.8 Timestamp ordering.** Every `updated` value parses as an ISO 8601
timestamp with a timezone and a version token, so that same-day revisions remain
orderable.

---

## 12. Failure Modes

**Numbering note.** The FM-L identifiers below supersede all earlier FM-L
assignments in this document's version history. Versions 1 and 2 of this paper
used FM-L1 for retrieval bypass, FM-L2 for orphan invisibility, and FM-L5 for
hybrid leakage. Those assignments are void. The failures themselves survive, at
FM-L8, FM-L2, and FM-L10 respectively. Any citation of an FM-L number should name
the document version alongside it until the older drafts age out of circulation.

**FM-L1 — Broken relative link.** A page points to a file that no longer exists.
*Detection:* link validation (11.1).

**FM-L2 — Orphan page.** A file exists outside `_log/superseded/` but no path
from index.html reaches it. *Detection:* compare filesystem audit with graph
crawl (11.2). Not ingested; reported as a defect (§7.1, path 3).

**FM-L3 — Scope omission.** A spoke or document does not declare what it owns.
*Detection:* required-metadata validation (11.3).

**FM-L4 — Crawl escape.** A relative path resolves outside the intended root.
*Detection:* canonical-path boundary check before reading (11.6).

**FM-L5 — Dynamic-page dependency.** A page requires JavaScript or a remote
service before its content exists. *Detection:* compare source HTML extraction
with rendered output. The local-web specification rejects such pages from the
authoritative corpus.

**FM-L6 — Superseded-content collision.** Current and retired versions are
indexed without status distinction. *Detection:* index records must carry
`status`, and default retrieval must filter to `current`. Requires §7.1's retired
ingestion path to be implemented; without it this failure is masked by the more
serious absence of retired content entirely.

**FM-L7 — Retrieval without provenance.** The search layer returns a fragment
without document ID, path, title, version, or status. *Detection:* require every
indexed chunk to retain page-level metadata.

**FM-L8 — Model bypass.** The model answers a corpus-specific question without
retrieving the local corpus. *Detection:* require citations or retrieval logs for
corpus-dependent answers. This failure belongs to the runtime protocol, not to
HTML itself.

**FM-L9 — Metadata trust failure.** Incorrect metadata causes a correct page to
be routed incorrectly. *Detection:* periodic manual sampling and metadata
validation. Structured metadata is useful because it is machine-readable, but
machine-readable errors propagate farther than prose errors.

**FM-L10 — Local/public confusion.** A local document is cited as though it were
publicly accessible or independently timestamped. *Detection:* the `substrate`
field is set on every crawl record and must appear in generated citations.

**FM-L11 — Retired-history loss.** Retired pages are never ingested, so the
corpus cannot answer what a document previously said. *Detection:* count records
with `status: retired` in the index and compare against the file count under
`_log/superseded/`. A mismatch means the retired ingestion path is not running.
This is the failure §7.1 exists to prevent and it is invisible to every other
check, because a corpus missing its own history still validates, still crawls,
and still answers current questions correctly.

---

## 13. Minimal Implementation

The minimal implementation requires only a directory, index.html, static HTML
pages, relative links, one parser, one bounded crawl loop, and one searchable
text index.

A complete first build may follow this sequence:

1. Create the root directory.
2. Write index.html.
3. Create one spoke directory.
4. Write its _index.html.
5. Add one operational page.
6. Link the root to the Sub-Index.
7. Link the Sub-Index to the page.
8. Add `rel="index"` and `rel="up"` to the page.
9. Run the validator.
10. Run the crawler.
11. Confirm that all three pages appear in the index.
12. Search for a phrase from the operational page.
13. Verify that the result carries its path, document ID, scope, version, and
    status.
14. Retire the operational page, replace it, and confirm that the retired version
    is still retrievable by document ID while absent from default results.

Step 14 is the one most likely to be skipped and is the only one that exercises
§7.1. Nothing more is required to prove the basic local-web mechanism.

A vector database, embeddings, GraphRAG, mode controller, and companion interface
can be added later without changing the source files.

---

## 14. Falsifier

The local-web claim is operational and should fail plainly.

**Test 1 — Crawlability.** If a crawler starting from index.html cannot enumerate
the active corpus, resolve its relative links, extract its MPLPB metadata,
preserve its page relationships, and place its content into a searchable index
without requiring page-specific code, then the local-web format as specified has
failed.

**Test 2 — Portability.** If moving the complete root directory to another
location breaks valid internal navigation or crawling, despite all internal links
being relative, then the implementation has violated the portability contract.

**Test 3 — Field utilization.** If the indexed metadata and link relationships
are never read by retrieval, routing, validation, or maintenance, then those
fields are decorative *in that implementation* and should not be credited with
improving it.

Tests 1 and 2 validate the local web as infrastructure. Test 3 is narrower than
it may appear and its limits should be stated: it detects whether the fields are
*consulted*, not whether consulting them *helps*. An implementation could read
every field on every query and still perform no better than one that ignored them
entirely. Test 3 passing is therefore necessary and not sufficient for the claim
that structure improves outcomes — a claim §10 already lists as unestablished.

**Test 4 — Structural contribution (open).** The sufficient test is an ablation:
duplicate the corpus, strip the metadata blocks, indexes, and typed links,
flatten the directory tree, randomize filenames, then run the same probe set
against both copies in randomized order and score whether the framework's rules
and relationships come back intact. If the stripped copy scores the same, the
structure is not contributing above storage. This test has not been run. It is
recorded here as open rather than assumed, and no claim in this paper should be
read as though it had passed.

---

## 15. Relationship to the Broader Architecture

The local web occupies one specific position in the five-module system.

**MPLPB** supplies the artifact discipline, indexes, revisions, scope
declarations, and recoverable structure.

**Rabbit Hole** crawls the local web and converts its pages into index records.

**Externalized Continuity** uses the resulting structure for navigation and
behavioral governance.

**Spinning** requires the model to reason over retrieved corpus material rather
than treating its own memory as the source.

**Mythic Logic Companion** may use the complete stack as a deployed interface.

The local web does not replace these modules. It gives them a shared source
object: one folder, one root page, one bounded link graph.

---

## 16. Conclusion

A local MPLPB does not need to be a specialized application.

It can be a website.

The site lives in a directory rather than on a public server. Its root is
index.html. Its documents are plain HTML. Its internal links are relative. Its
metadata declares identity, scope, version, use conditions, status, and
relationships. A bounded crawler follows the graph, extracts the pages, and
builds an index. A separate audit pass recovers the retired history the graph
deliberately no longer reaches. A reasoning system queries that index.

This separation keeps the architecture small and testable:

- HTML stores the corpus.
- Links define the graph.
- The crawler enumerates it.
- The audit recovers what the graph has retired.
- The index retrieves it.
- The model reasons over what was retrieved.

The source remains readable when every higher layer is removed. Open the folder
in a browser and it is still a working knowledge site. Replace the index backend
and the pages do not change. Replace the language model and the pages do not
change. Move the directory and the relative graph remains intact.

That is the local version of MPLPB: not a private imitation of the public web,
but a real, bounded web whose entire address space fits inside one portable
folder.

---

## Philosophical Note

The useful property of the web is not that its pages are far away.

It is that documents have addresses, declare relationships, and can be traversed
from a known beginning.

A local folder can possess those same properties. The network is optional. The
structure is not.

— MDM

---

*Revision note, v4:* This version corrects five defects in v3 rather than
reframing it; v3's three-layer separation and narrow implementation claim are
retained unchanged and remain the paper's contribution.

1. **Retired pages now have an ingestion path (§7.1, FM-L11).** v3 routed retired
   pages out of the graph crawl and declared the filesystem audit
   maintenance-only, which meant retired pages were never indexed and FM-L6's
   "exclude by default" had nothing to exclude. Three explicit paths — graph,
   retired, orphan — replace the two-mode framing.
2. **FM-L numbering collision resolved (§12).** v1 and v2 assigned FM-L1, FM-L2,
   and FM-L5 to different failures than v3 does. Since superseded versions are
   retained rather than deleted, the same identifier pointed at different
   failures depending on which draft a reader held. v4 declares the earlier
   assignments void and states where those failures now live.
3. **Cross-domain routing split by layer (§8.1).** v3's "may retrieve from more
   than one spoke" read as a contradiction of SEP-007's rule that the hub does
   not guess. Retrieval breadth and answering discipline are now separated
   explicitly.
4. **Timestamps carry a time component (header, §5.1, 11.8).** v1 through v3 all
   dated 2026-08-05 and could not be ordered from their own metadata. The header
   now also carries an explicit `Supersedes` field, applying to this paper the
   same rule §11.5 imposes on every other document.
5. **Falsifier Test 3 bounded, Test 4 added (§14).** Field utilization detects
   whether metadata is consulted, not whether it helps. The ablation that would
   test the stronger claim is now named separately and logged as open.

Also pinned: `mplpb:supersedes` is a semicolon-separated list of document IDs
(§5.1), and `mplpb:status` is introduced as a required field, since §7.1 and
FM-L6 are both unimplementable without it.
