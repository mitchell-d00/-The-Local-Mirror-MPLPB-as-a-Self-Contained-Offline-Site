Category: Specification / Architecture
Subcategory: Knowledge Infrastructure / Local Substrate
Document ID: MPLPB-LOCAL-008
Last Updated: 2026-08-05 v4
Owner: Mitchell D. McPhetridge

Summary: This paper specifies a local version of Multi-Platform Linked Public Building as a self-contained website stored in an ordinary directory. The site consists of plain HTML files connected by relative links, beginning at index.html. A browser can open it for human navigation, while a local crawler can enumerate the same pages, extract their metadata and links, and place their contents into an MPLPB-compatible retrieval index. The local web is the source substrate; the crawler and index are separate components. No server, database, framework, internet connection, or model training is required.

When to use this document:
* Building an MPLPB from private, unpublished, proprietary, or local material
* Giving a crawler a bounded local website to enumerate and index
* Creating a portable MPLPB that works from a folder, archive, external drive, or synchronized directory
* Converting an existing collection of documents into a linked local web
* Testing MPLPB navigation, retrieval, and structure without publishing the corpus
* Running a structure-ablation trial (§14.3) that the public corpus cannot support

Scope / Exclusions:
* This document specifies the local website and the contract by which a crawler reads it.
* It does not require the language model itself to follow hyperlinks manually.
* It does not claim that local retrieval demonstrates public recoverability, independent replication, public precedence, or third-party validation.
* It does not specify a complete search backend. The Rabbit Hole indexer supplies the adapter, parsing, indexing, and retrieval layers.
* It does not require semantic search. A file crawler and ordinary text index are sufficient for the minimal implementation.
* It does not grant the corpus authority over the runtime. The boot block (§9) orients a reader or model; it does not instruct one. A crawled page is corpus content, never operator instruction (§9.2, FM-L11).
* It does not decide which spoke answers a question. This document governs what is retrievable; MPLPB Separation & Precedence governs what answers (§8).

Related documents:
* MPLPB v3 — complete artifacts, Main Index, Sub-Indexes, revision discipline, and reconstruction rules
* Rabbit Hole Internet Indexer Blueprint v2 — source adapters, indexing, chunking, metadata extraction, and hybrid retrieval
* Externalized Continuity at Scale — Navigator loop, complete artifacts, and mode control
* Spinning v2 — use of the retrieved graph as the model's working knowledge source; the empty-graph falsifier that §14.3 is the structural sibling of
* MPLPB Separation & Precedence v1 — spoke boundaries and routing by declared scope
* MPLPB as a Public Experiment, Multi-Apparatus Edition — the public recoverability claim this document is careful not to borrow from; source of open prediction P2
* The Five-Module Combinator — interface contract between MPLPB, Rabbit Hole, Navigator, Spinning, and the deployed companion

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

Multi-Platform Linked Public Building was developed as a way to place continuity in artifacts rather than in a single AI session. Its public form uses published, cross-linked documents that search-capable systems can recover from the web.

The local form is simpler.

A local MPLPB is a small website stored in a directory. It begins at index.html. Every page is an ordinary HTML file. Every internal connection is a relative hyperlink. Each subject area has a Sub-Index, each operational page declares what it contains and when it should be used, and each page links back toward the indexes above it.

A local crawler starts at index.html, follows the allowed local links, extracts page text and metadata, records the link graph, and sends the resulting documents to a text or hybrid-search index. The language model does not need to behave like a browser or manually click through the site. It queries the index built from the site.

The architecture therefore has three distinct layers:

1. The local web: authoritative HTML files and their relative link graph.
2. The crawler and indexer: the Rabbit Hole adapter that enumerates, parses, and indexes the web.
3. The reasoning interface: an AI system that retrieves the indexed pages and answers from them.

This paper specifies the first layer and its interface with the second. Its claim is deliberately narrow: plain local HTML is a suitable source format for an MPLPB-compatible crawler.

One consequence of that narrowness is worth stating up front, because it is the paper's most useful side effect. A local corpus can be ablated. The public corpus cannot — testing whether MPLPB's structure improves retrieval would require unpublishing it. Section 14.3 specifies that ablation as a runnable test rather than a rhetorical falsifier.

---

## 1. The Requirement

The requirement is not to create a new model, a new browser, or a complex knowledge platform.

The requirement is:

**Build a local web that an MPLPB-compatible crawler can crawl.**

The local web must be:

* readable by a normal browser;
* readable as plain text and HTML by a crawler;
* portable between machines;
* usable without an internet connection;
* understandable from a declared entry point;
* bounded so that the crawler does not leave the corpus;
* structured enough to expose scope, versions, relationships, and supersessions;
* independent of a particular search engine, vector database, model vendor, or operating system.

Plain HTML with relative links satisfies these requirements.

HTML already provides the necessary primitives:

* pages;
* links;
* metadata;
* headings;
* document titles;
* typed relationships;
* machine-readable structure;
* human-readable rendering.

A local MPLPB does not simulate a website. It is a website whose address space happens to be a local directory rather than a public domain.

---

## 2. The Three-Layer Architecture

The local system should not blur storage, crawling, retrieval, and reasoning into one component.

### 2.1 Layer One: The Local Web

The local web is the authoritative corpus.

It contains:

* index.html;
* one directory per spoke or subject domain;
* one _index.html inside each spoke;
* operational HTML documents;
* a revision log;
* a superseded-document directory;
* one shared stylesheet;
* optionally, a plain-text boot file.

The local web owns:

* document content;
* document identity;
* scope declarations;
* version information;
* relationships;
* navigation;
* supersession;
* corpus boundaries.

It does not own search ranking, embeddings, model behavior, or answer generation.

### 2.2 Layer Two: The Crawler and Index

The crawler is a Rabbit Hole source adapter pointed at the local root.

It performs a bounded traversal:

1. Open index.html.
2. Extract internal links.
3. Resolve each link relative to the current file.
4. Canonicalize the resolved path and reject it if it falls outside the declared root (§4.3).
5. Visit each reachable HTML page once.
6. Extract metadata, text, and outgoing relationships.
7. Record the link graph, including typed edges to retired pages.
8. Send the resulting page records to the selected index, each carrying its lifecycle status.

The index may be:

* a simple filename and full-text index;
* a SQLite search database;
* a keyword index;
* a vector index;
* a hybrid keyword and semantic index;
* another implementation behind the Rabbit Hole adapter contract.

The local-web format does not depend on which index is selected.

### 2.3 Layer Three: The Reasoning Interface

The reasoning system queries the index rather than depending on its own parametric memory.

A request may be routed by:

* exact document ID;
* title;
* category;
* scope;
* trigger condition;
* keyword;
* semantic similarity;
* graph relationship;
* version status.

Retrieved pages are then supplied to the model as answer material.

Spinning may impose a no-shortcut rule requiring substantive answers to be grounded in retrieved corpus material. Externalized Continuity may apply routing and mode-control rules. Those are runtime layers above the local web.

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
      heat_transfer_v1.html

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

It should contain:

* the name and purpose of the corpus;
* the current version;
* the root scope;
* the category map;
* links to every active Sub-Index;
* a link to the revision log;
* crawler boundary information;
* any read-first or reconstruction orientation (subject to §9.2).

The root should be a map, not a long essay.

### 3.2 Spoke Directories

Each top-level domain receives its own directory.

Examples:

```
/spec/
/physics/
/gardening/
/legal/
/game-system/
```

Each directory is an MPLPB spoke. Its _index.html declares the domain it owns and lists its active documents.

### 3.3 Operational Documents

Operational pages contain the actual specifications, policies, guides, research notes, procedures, or reference material.

Every operational page should be reachable from its parent _index.html.

A file that exists on disk but is reachable by no path from index.html — neither through an active Sub-Index nor through the revision log — is an **orphan**. The crawler may still discover it through a filesystem scan, but it is not part of the declared local web until some index links to it.

Reachability, not currency, is the test. A retired page linked from the revision log is reachable and therefore part of the declared web; it is simply not current. This distinction is what keeps §11.5 from turning every correctly retired page into an FM-L2 orphan.

### 3.4 Revision Material

The _log/ directory records changes. It holds two things: revisions.html, and a superseded/ directory containing retired pages.

**revisions.html is a first-class index, not an appendix.** It is linked from index.html, and it links to every retired page with a typed relationship:

```html
<a rel="superseded" href="./superseded/heat_transfer_v1.html">
  Heat Transfer (LOCAL-PHY-001 v1) — superseded 2026-08-05 by v2
</a>
```

This gives the retired page a path from the root, which makes it crawlable, and gives that path a type, which makes it excludable. A retrieval layer that wants only current material filters on the status field (§5), not on the absence of a link.

Active Sub-Indexes point to current pages only. The revision log points to retired ones. Both are reachable; only one is current.

Supersession is recorded on **both** pages, in opposite directions (§5.1). The replacement declares what it supersedes. The retired page declares that it is retired and by what. Neither pointer alone is sufficient — see §5.1 for why.

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

A relative link survives when the corpus is:

* moved;
* renamed;
* zipped;
* copied to another machine;
* placed on removable storage;
* synchronized into another directory;
* served later by a local or public web server.

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

A retired page keeps its original upward links so it remains navigable in context, and adds `rel="superseded-by"` pointing at its replacement.

### 4.2 Related Links

Related pages may be identified with:

```html
<a rel="related" href="./continuity.html">Externalized Continuity</a>
```

These links become graph edges when the crawler parses the page.

### 4.3 Crawl Boundary

The crawler must treat the local root as a hard boundary.

If the root is `/path/to/mplpb-local/`, then a resolved link may be crawled only if its canonical path remains inside that root.

This prevents a malformed link such as:

```html
<a href="../../../private-file.html">
```

from causing the crawler to index unrelated material.

"Canonical path" is doing real security work here, and the obvious implementations of it are wrong. This matters more in the local case than the public one: a local corpus is pointed at private material by design, and a boundary failure exfiltrates that material into an index the corpus does not own.

The check must satisfy four properties:

**Decode before resolving.** Percent-encoded traversal (`..%2F..%2F`) survives lexical normalization if the path is normalized first and decoded later. Decode, then normalize, then compare. Reject any href that still contains traversal segments after decoding.

**Resolve symbolic links.** A symlink inside the root pointing outside it passes every lexical check ever written. Resolve to the real path — `realpath` / `Path.resolve(strict=True)` / `filepath.EvalSymlinks` — before deciding. A corpus intended to be portable should contain no symlinks at all; the validator (§11.6) should flag them rather than follow them.

**Compare path components, not string prefixes.** Root `/path/to/mplpb-local` and target `/path/to/mplpb-local-backup/secrets.html` pass a string-prefix test and must not pass a boundary test. Compare resolved component lists, or append the separator before comparing.

**Check before reading, not after.** The rejection must happen before the file is opened, so that a rejected path is never read into memory, never partially parsed, and never logged with its contents.

External http:// or https:// links may be recorded as references, but the local crawl should not follow them unless an explicit hybrid-crawl mode is enabled. Non-HTML schemes (file:, data:, javascript:) are rejected outright.

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
  <meta name="mplpb:updated" content="2026-08-05 v1">
  <meta name="mplpb:owner" content="Mitchell D. McPhetridge">
  <meta name="mplpb:substrate" content="local">
  <meta name="mplpb:status" content="current">
  <meta
    name="mplpb:scope"
    content="File layout and relative-link rules for the local web">
  <meta
    name="mplpb:when-to-use"
    content="Adding, moving, validating, or repairing a page">
  <meta name="mplpb:supersedes" content="">
  <meta name="mplpb:superseded-by" content="">

  <link rel="index" href="../index.html">
  <link rel="up" href="./_index.html">
  <link rel="stylesheet" href="../style.css">
</head>
```

The crawler should extract these fields directly rather than attempting to infer them from prose.

`mplpb:substrate` is set to `local` and exists so that generated citations can mark the substrate type, which is the detection mechanism for FM-L10.

### 5.1 Supersession Is Recorded in Both Directions

`mplpb:supersedes` is a forward pointer carried by the replacement page. It answers: what did this page replace?

`mplpb:status` and `mplpb:superseded-by` are carried by the retired page. They answer: is this page current, and if not, what replaced it?

Both are required, because the checks that consume them run in opposite directions.

A forward pointer alone cannot tell a crawler that the page in its hand is retired. To learn that from `mplpb:supersedes` fields, the crawler must first read the entire corpus, invert every supersession edge, and only then revisit each record to label it — a second full pass, and a second pass that fails open, since a page whose replacement was not crawled (because the replacement was itself orphaned, or outside the boundary, or malformed) silently stays labeled current.

With `mplpb:status` on the page itself, lifecycle becomes a local property of a single crawl record. The index can filter retired material at ingest, the retrieval layer can exclude it by default, and FM-L6 becomes a validation check rather than a graph computation. The forward pointer is retained because it is what makes the revision chain traversable in the useful direction for a human reading history.

A retired page therefore carries:

```html
<meta name="mplpb:status" content="superseded">
<meta name="mplpb:superseded-by" content="LOCAL-PHY-001 v2">
<link rel="superseded-by" href="../../physics/heat_transfer.html">
```

Permitted values for `mplpb:status`: `current`, `superseded`, `draft`, `deprecated`. Absence is treated as `current`, so that existing pages remain valid, but the validator (§11.3) requires it explicitly on any page inside `_log/superseded/`.

### 5.2 The Crawl Record

A normalized crawl record may contain:

```json
{
  "document_id": "LOCAL-SPEC-001",
  "path": "spec/mirror_layout.html",
  "title": "Mirror Layout — MPLPB Local",
  "category": "Specification / Architecture",
  "scope": "File layout and relative-link rules for the local web",
  "when_to_use": "Adding, moving, validating, or repairing a page",
  "updated": "2026-08-05 v1",
  "owner": "Mitchell D. McPhetridge",
  "substrate": "local",
  "status": "current",
  "supersedes": [],
  "superseded_by": null,
  "links": [
    { "rel": "up",    "target": "spec/_index.html" },
    { "rel": "index", "target": "index.html" }
  ],
  "text": "Extracted visible page text..."
}
```

The HTML is authoritative. The crawl record is derived.

---

## 6. The Crawler Contract

The Rabbit Hole blueprint defines a source adapter around operations such as `list()`, `read()`, and `get_metadata()`.

For the local web, the adapter may expose:

```
open_root()
read_page(path)
extract_metadata(path)
extract_links(path)
resolve_link(source, href)
is_inside_root(path)
```

`is_inside_root` implements §4.3 in full — decode, resolve symlinks, compare components — and is called before `read_page`, not after.

The crawler does not need a full browser engine if the pages contain static HTML.

It should not require:

* JavaScript execution;
* client-side rendering;
* login state;
* remote fonts;
* framework bundles;
* API calls;
* generated routes;
* a database.

### 6.1 Minimal Crawl Algorithm

```
queue = ["index.html"]
visited = empty set

while queue is not empty:
    current = remove first item from queue

    if current is already visited:
        continue

    resolved = canonicalize(current)     # decode, normalize, resolve symlinks
    if not is_inside_root(resolved):
        reject and log; continue         # rejected before any read

    page     = read resolved
    metadata = extract MPLPB fields      # including status, superseded_by
    text     = extract visible document text
    links    = extract href and rel values

    emit page record with lifecycle status
    mark current visited

    for each local HTML link:
        target = resolve relative to current
        if is_inside_root(canonicalize(target)) and target not visited:
            add target to queue
```

Retired pages enter this traversal by the same door as everything else: revisions.html is reachable from index.html, and it links to them. No special case is required in the crawl loop. The distinction between current and retired is carried in the record, not in the reachability.

### 6.2 Crawl Modes and the Maintenance Tier

Two modes are useful, and they belong to different tiers.

**Graph crawl.** Starts from index.html and follows links. This identifies the declared MPLPB. It is retrieval infrastructure and must satisfy the no-browser constraint above.

**Filesystem audit.** Lists every supported file beneath the root and compares it with the graph crawl. This identifies orphan pages, unreachable pages, missing index entries, stale files, and accidental duplicates. It is maintenance infrastructure.

The tiers have different budgets, and this is the point of separating them. The graph crawl runs on every index build and must stay cheap and dependency-free. The maintenance tier runs occasionally, on the author's machine, and may use tools the crawler is forbidden — including a headless browser, if a check genuinely requires rendering (see FM-L5).

A check that needs capabilities the crawler contract excludes is not thereby impossible. It is a maintenance check.

---

## 7. Indexing

The crawler emits one record per page.

For small corpora, indexing the whole page is acceptable. For larger pages, the indexer may split the text into chunks while retaining the page-level metadata on every chunk.

A chunk record should preserve:

* source path;
* document ID;
* title;
* category;
* scope;
* version;
* lifecycle status;
* substrate type;
* chunk number;
* parent-page link;
* relationship edges.

This allows retrieval to return a relevant passage without losing its document identity. A chunk that arrives at the model without its status field cannot be excluded when retired, and cannot be marked local when cited — which is FM-L6 and FM-L10 arriving together through the same gap.

Keyword indexing is sufficient for the minimum local system.

Hybrid retrieval may combine exact keyword matching, filename matching, metadata filtering, semantic similarity, and graph expansion.

Semantic retrieval is an improvement, not a requirement for the local web to exist.

---

## 8. Routing by Scope

MPLPB Separation & Precedence treats each bounded domain as a spoke and the routing layer as the spinner.

In the local web:

* the root index.html is the top-level routing map;
* each directory is a spoke;
* each _index.html declares the spoke's scope;
* the crawler records those scope declarations;
* the retrieval layer uses them as ranking or filtering signals.

For a clearly scoped request, retrieval should prefer the owning spoke. A question about link validation belongs to spec/; a question about heat transfer belongs to physics/; a question about sowing dates belongs to gardening/.

### 8.1 Retrieval May Span Spokes; Answers May Not Blend

Separation & Precedence §4 states that on a genuinely cross-domain query the hub does not blend and does not guess — it asks the user to narrow. This document says a cross-domain request may retrieve from more than one spoke. Those are not in conflict, and the reason is worth stating explicitly so that a reader comparing the two documents does not read drift where there is a layer boundary.

**Retrieval and precedence operate at different layers.**

Retrieval is evidence-gathering. It is allowed, and often required, to return material from several spokes — that is how the routing layer discovers that a query straddles two declared scopes in the first place. A retrieval layer that returned only one spoke's material would make the cross-domain case *undetectable*, and the hub would then satisfy the letter of the precedence rule while silently committing FM-SEP "silent cross-domain guess" at the layer below.

Precedence is answer-selection. It applies after retrieval, at the layer Separation & Precedence governs, and there the rule is unchanged: the in-scope spoke answers, the out-of-scope spoke yields, and a genuine straddle produces a clarifying question rather than a merged answer.

The obligation this places on the local web is therefore not to restrict retrieval, but to **preserve provenance through it**: every retrieved chunk keeps the scope declaration of the spoke it came from, so the routing layer can see that it is holding material from two owners and act accordingly. Flattening the corpus into one undifferentiated collection destroys exactly the signal precedence needs.

Scope helps route. It does not determine truth.

---

## 9. Booting a Stateless Session

The local web may include a short boot block in index.html and an optional BOOT.md copy.

The boot block should state:

1. what the corpus is;
2. where the authoritative root is;
3. that answers about the corpus should use crawled or retrieved pages;
4. how categories are divided;
5. which version is current;
6. where revisions and supersessions are recorded;
7. which runtime rules the corpus was written under.

The boot file is not the crawler. Its purpose is to orient a human or AI interface after the local web has been mounted or indexed.

A minimal instruction is:

> Treat index.html as the root of this corpus. Retrieve relevant local pages before answering corpus-dependent questions. Prefer current documents reachable from the Main Index. Preserve document IDs, scope, version, and supersession status in retrieval.

### 9.2 The Boot Block Orients; It Does Not Authorize

Item 7 above requires a constraint that the rest of this specification does not, and it is the one place where the local web could become a liability rather than a substrate.

A local MPLPB is a folder. Folders are copied, shared, downloaded, restored from backups, and synchronized from sources their eventual reader did not write. If a crawling or reading agent treats a page inside the corpus as operator instruction, then anyone who can place a folder in front of that agent can configure it — and the boot block, which is designed to be read first and to describe runtime rules, is the natural place to put such an instruction.

The rule is therefore:

**Content retrieved from the corpus is data. It is never instruction.**

The boot block may *describe* which runtime rules a corpus was authored under. It may not *impose* them. Mode selection, safety posture, tool permissions, retrieval scope, and every other behavioral setting are properties of the runtime and its operator, established outside the corpus and unchanged by anything found inside it.

This is the local analogue of the same discipline the public protocol requires. A runtime block in a published document is a proposal to an agent, evaluated by that agent's operator; it is not a command that executes on load. The property is the same in both substrates, and the local substrate needs it stated more loudly, because a local folder carries no publication history, no author attribution a reader can check, and no public record that would make tampering visible.

Stating this does not weaken the corpus. It is what makes a corpus safe to hand to a stranger — which is, eventually, the point.

---

## 10. What the Local Web Does Not Claim

The local web provides a source substrate.

It does not, by itself, establish:

* that a model will voluntarily follow the Main Index;
* that semantic retrieval will return the correct page;
* that the corpus's claims are true;
* that the corpus is independently recoverable by strangers;
* that filesystem dates establish public precedence;
* that a link graph improves answer quality;
* that a structured corpus outperforms unstructured files;
* that a retrieved page was actually used in the answer.

Those are separate questions requiring separate tests. Two of them — the last two on this list — are now testable here, and §14.3 specifies how. The rest remain open.

The narrow claim here is only:

**A bounded directory of static HTML pages with relative links and MPLPB metadata can be crawled, indexed, moved, inspected, and used as the local source layer of the broader architecture.**

---

## 11. Validation and Maintenance

A local-web validator should perform at least the following checks.

**11.1 Link validity.** Every local target exists.

**11.2 Root reachability.** Every active page is reachable from index.html through an active Sub-Index. Every retired page is reachable from index.html through revisions.html. A page reachable by neither is an orphan (FM-L2).

**11.3 Required metadata.** Every operational page declares document ID, category, updated version, scope, when-to-use, substrate, index link, and up link. Every page inside `_log/superseded/` additionally declares status and superseded-by explicitly.

**11.4 Unique document identity.** No two *current* pages share a document ID. A retired page may share the ID of its replacement — that is what makes it the same document at an earlier version — provided its status is `superseded`. Uniqueness is enforced over the current set, and over the (document ID, version) pair across the whole corpus.

**11.5 Supersession consistency.** Four conditions, all mechanical:

* every page declared in a `supersedes` field exists in `_log/superseded/`;
* every page in `_log/superseded/` declares `status: superseded` and a `superseded-by` target that exists;
* the two directions agree — if A supersedes B, B is superseded-by A;
* no page with `status: superseded` is listed in an active Sub-Index, and every such page is listed in revisions.html.

**11.6 Boundary safety.** No followed path resolves outside the corpus root under the §4.3 rules. The validator additionally reports any symlink beneath the root, whether or not its target is inside, since a portable corpus should contain none.

**11.7 Index consistency.** Each current operational page appears in its parent _index.html.

**11.8 Provenance completeness.** Every emitted chunk carries document ID, path, title, version, status, and substrate. A chunk missing any of these is a defect at ingest, not at retrieval (FM-L7).

These checks are mechanical. They should be performed by a script rather than left to memory.

---

## 12. Failure Modes

**FM-L1 — Broken relative link.** A page points to a file that no longer exists.
*Detection:* link validation (§11.1).

**FM-L2 — Orphan page.** A file exists but no path from index.html reaches it, through neither an active index nor the revision log.
*Detection:* compare filesystem audit with graph crawl (§6.2). Note that under §3.3 and §3.4, correctly retired pages are reachable and therefore do not trigger this. A retired page that *does* trigger it has fallen out of revisions.html, which is a real defect.

**FM-L3 — Scope omission.** A spoke or document does not declare what it owns.
*Detection:* required-metadata validation (§11.3).

**FM-L4 — Crawl escape.** A relative path resolves outside the intended root.
*Detection:* the four-property boundary check of §4.3, applied before read. Testing this requires deliberate adversarial fixtures in the validation suite — an encoded-traversal href, a sibling-directory prefix collision, and a symlink escape — because all three pass naive implementations and none occur by accident in a well-formed corpus.

**FM-L5 — Dynamic-page dependency.** A page requires JavaScript or a remote service before its content exists.
*Detection:* two tiers. At crawl time, a source-only heuristic: flag any page whose extracted visible text falls below a threshold relative to its markup size, or that contains `<script>` blocks alongside near-empty content containers, or that declares a framework root element. This is cheap and requires no rendering. At maintenance time, and only there, a rendered comparison may confirm the flag using a headless browser — permissible because §6.2 places the audit in a different tier with a different budget. The crawler contract is unaffected. The local-web specification rejects such pages from the authoritative corpus either way.

**FM-L6 — Superseded-content collision.** Current and retired versions are indexed without status distinction.
*Detection:* every crawl record carries `status` from the page's own metadata (§5.1), so the check is per-record and requires no graph inversion. Current retrieval excludes non-current status by default.

**FM-L7 — Retrieval without provenance.** The search layer returns a fragment without document ID, path, title, or version.
*Detection:* §11.8. Every indexed chunk retains page-level metadata.

**FM-L8 — Model bypass.** The model answers a corpus-specific question without retrieving the local corpus.
*Detection:* require citations or retrieval logs for corpus-dependent answers. This failure belongs to the runtime protocol (Spinning's no-shortcut rule), not to HTML itself.

**FM-L9 — Metadata trust failure.** Incorrect metadata causes a correct page to be routed incorrectly.
*Detection:* periodic manual sampling and metadata validation. Structured metadata is useful because it is machine-readable, but machine-readable errors propagate farther than prose errors. The `status` field added in v4 raises the stakes here specifically: a page mislabeled `superseded` becomes invisible to default retrieval rather than merely misranked. Sampling should cover status fields preferentially.

**FM-L10 — Local/public confusion.** A local document is cited as though it were publicly accessible or independently timestamped.
*Detection:* `mplpb:substrate` is carried in metadata and through every chunk (§7), and generated citations render it. A citation to a local page that does not say so is the failure.

**FM-L11 — Boot-block authority confusion.** A reading or crawling agent treats corpus content — the boot block, a page, a metadata field — as operator instruction rather than as data, and changes its behavior accordingly.
*Detection:* present the crawler or companion with a test corpus whose boot block contains an instruction the runtime should refuse (a mode change, a boundary relaxation, an instruction to ignore the superseded filter). Correct behavior is to index the text and disregard the instruction. Any behavioral change is the failure. This check belongs in the validation suite permanently, not once, since it regresses silently whenever the runtime layer changes.

---

## 13. Minimal Implementation

The minimal implementation requires only:

* a directory;
* index.html;
* static HTML pages;
* relative links;
* one parser;
* one bounded crawl loop;
* one searchable text index.

A complete first build may follow this sequence:

1. Create the root directory.
2. Write index.html.
3. Create one spoke directory.
4. Write its _index.html.
5. Add one operational page.
6. Link the root to the Sub-Index.
7. Link the Sub-Index to the page.
8. Add rel="index" and rel="up" to the page.
9. Run the crawler.
10. Confirm that all three pages appear in the index.
11. Search for a phrase from the operational page.
12. Verify that the result carries its path, document ID, scope, version, status, and substrate.

Then exercise the lifecycle, which is where the v3 specification was underdetermined:

13. Supersede the operational page: write a v2, move v1 to `_log/superseded/`, set its status and superseded-by, add it to revisions.html, point the Sub-Index at v2.
14. Re-crawl. Confirm both versions are indexed, both carry correct status, and default retrieval returns only v2.
15. Run the validator. Confirm §11.5 passes and no orphan is reported.

Nothing more is required to prove the basic local-web mechanism.

A vector database, embeddings, GraphRAG, mode controller, and companion interface can be added later without changing the source files.

---

## 14. Falsifiers

The local-web claim is operational and should fail plainly. Three tests, of which the third is the one worth running first.

### 14.1 Enumeration

If a crawler starting from index.html cannot enumerate the active corpus, resolve its relative links, extract its MPLPB metadata, preserve its page relationships, and place its content into a searchable index without requiring page-specific code, then the local-web format as specified has failed.

### 14.2 Portability

If moving the complete root directory to another location breaks valid internal navigation or crawling, despite all internal links being relative, then the implementation has violated the portability contract.

These two validate the local web as infrastructure. Both are close to trivially passable by a correct implementation, which is what makes them adequate as specifications and inadequate as evidence.

### 14.3 Structure Ablation

The third test asks whether the structure does anything, and unlike the first two it can fail informatively.

The v3 formulation — *if the indexed metadata and link relationships are never used by retrieval, routing, validation, or maintenance, then those fields are decorative* — cannot fail as written. Section 11's validators consume the metadata, so "never used" is false by construction the moment a validator runs. Usage is not the question. Contribution is.

**The test.** Index the same corpus twice, from the same source files:

* **Arm A (structured):** the full pipeline of this document — metadata extracted into fields, link graph recorded, scope preserved on chunks, status filtering active, graph expansion available to retrieval.
* **Arm B (flat):** the same pages' visible text, chunked identically, indexed with no metadata fields, no link graph, no scope, no status filter. Same embedding model or same keyword index, same chunk size, same ranking function. The only difference is structure.

**The query set.** Fix N queries before either arm is built, each with a known correct target page recorded in advance. The set must include the cases where structure should matter if it matters anywhere:

* version-sensitive queries whose correct answer exists in both a current and a retired page (tests status filtering);
* scope-ambiguous queries whose terms appear in two spokes (tests scope preservation);
* relationship queries whose answer requires a page that is a graph neighbor of the best lexical match (tests graph expansion);
* plain lexical queries where structure should make no difference (the control — if Arm A wins here too, something is wrong with the comparison, not with Arm B).

**The measurements.** Whether the correct document ID appears in the top k; precision at k; and, separately, whether the returned chunk carried enough provenance for the answer to be attributable at all. That last one is not a tie-breaker — a system that retrieves the right passage without provenance has failed differently, not less.

**What each outcome means.** If Arm A does not beat Arm B on the version-sensitive and scope-ambiguous queries, the metadata is decorative *for this corpus and this query set*, and the paper's structural claims should be narrowed to the maintenance benefits alone — which §11 does establish independently. If Arm A wins only on the query classes designed to favor it, that is still a real result, stated at its true size: structure helps on version and scope resolution, and is neutral elsewhere. If Arm A wins on the control queries too, suspect a confound in the harness before believing it.

**Why here.** This is open prediction P2 from the multi-apparatus protocol, which has stayed untested because the public corpus cannot be ablated — removing structure from published documents would mean unpublishing them. Locally the ablation costs a second index build.

It is also the structural sibling of Spinning's falsifier. Spinning ablates the graph's *content* and asks whether the model still answers correctly, testing whether retrieval is doing the work. This ablates the graph's *structure* and asks whether retrieval still finds the right page, testing whether the metadata is doing the work. The two together cover the corpus's central empirical claim from both sides.

**Honest limits.** A query set written by the corpus author is the weakest form of this test, for the same reason author-run replication trials are the weakest evidence class in the multi-apparatus protocol: the queries will unconsciously match the structure they were written alongside. A third-party query set is materially stronger. A single corpus is also a single data point — a result here is about this corpus's structure, not about structure in general. Log it as such.

---

## 15. Relationship to the Broader Architecture

The local web occupies one specific position in the five-module system.

**MPLPB** supplies the artifact discipline, indexes, revisions, scope declarations, and recoverable structure.

**Rabbit Hole** crawls the local web and converts its pages into index records.

**Externalized Continuity** uses the resulting structure for navigation and behavioral governance.

**Spinning** requires the model to reason over retrieved corpus material rather than treating its own memory as the source.

**Mythic Logic Companion** may use the complete stack as a deployed interface.

The local web does not replace these modules. It gives them a shared source object: one folder, one root page, one bounded link graph.

It also gives the corpus something it did not previously have: a substrate that can be experimented on. The public corpus is an instrument for testing recoverability and cannot be varied without damaging what it measures. The local corpus can be duplicated, ablated, corrupted deliberately, and rebuilt in an afternoon. Several of the corpus's open predictions are stuck for exactly this reason, and this is where they become cheap.

---

## 16. Conclusion

A local MPLPB does not need to be a specialized application.

It can be a website.

The site lives in a directory rather than on a public server. Its root is index.html. Its documents are plain HTML. Its internal links are relative. Its metadata declares identity, scope, version, lifecycle status, use conditions, and relationships. A bounded crawler follows the graph, extracts the pages, and builds an index. A reasoning system queries that index.

This separation keeps the architecture small and testable:

* HTML stores the corpus.
* Links define the graph.
* The crawler enumerates it.
* The index retrieves it.
* The model reasons over what was retrieved.

The source remains readable when every higher layer is removed. Open the folder in a browser and it is still a working knowledge site. Replace the index backend and the pages do not change. Replace the language model and the pages do not change. Move the directory and the relative graph remains intact.

That is the local version of MPLPB: not a private imitation of the public web, but a real, bounded web whose entire address space fits inside one portable folder.

---

## Philosophical Note

The useful property of the web is not that its pages are far away.

It is that documents have addresses, declare relationships, and can be traversed from a known beginning.

A local folder can possess those same properties. The network is optional. The structure is not.

What the network did provide, and what a folder does not, is the discipline of being read by someone who did not write it. A local corpus can be sloppy in ways a public one cannot afford, because nothing tests it. The ablation in §14.3 exists to supply that pressure artificially — to let the structure fail in private before it is asked to hold in public.

— MDM

---

## Revision Note (v4)

This revision fixes four internal contradictions in v3 and adds one failure mode. Logged rather than silently corrected, per the corpus's revision discipline.

**1. Retired pages were orphans by construction.** v3 §3.3 defined an orphan as unreachable from index.html; §11.5 required retired pages to be absent from active indexes; §6.2 assigned filesystem audit to maintenance and graph crawl to retrieval. Together these left retired pages with no path into the retrieval index at all, while FM-L6 assumed they were in it and needed status distinction. **Fixed** by making `_log/revisions.html` a linked, first-class index that reaches retired pages through typed `rel="superseded"` edges (§3.4), and by redefining orphan as unreachable-by-any-path rather than absent-from-active-indexes (§3.3, §11.2, FM-L2).

**2. Supersession metadata pointed the wrong direction.** v3 carried only `mplpb:supersedes`, a forward pointer on the replacement. The checks that consume it — FM-L6, §11.5 — need to know that the page in hand is retired, which is the reverse edge, recoverable only by inverting the whole corpus graph in a second pass that fails open on partial crawls. **Fixed** by adding `mplpb:status` and `mplpb:superseded-by` to the retired page, making lifecycle a local property of each crawl record (§5.1). §11.4 revised so that a retired page may share its replacement's document ID.

**3. FM-L5 required capabilities the crawler contract forbids.** Detection was specified as comparing source extraction with rendered output; §6 forbids a browser engine. **Fixed** by splitting detection across the two tiers §6.2 already distinguishes: a source-only heuristic at crawl time, an optional rendered confirmation at maintenance time, where the budget permits it.

**4. The cross-domain rule appeared to contradict Separation & Precedence.** v3 §8 permitted retrieval across spokes; SEP-007 §4 forbids blending and requires a clarifying question. **Fixed** by naming the layer boundary explicitly (§8.1): retrieval gathers evidence and may span spokes — must, in fact, or the straddle is undetectable — while precedence selects answers and does not blend. The local web's obligation is provenance preservation, not retrieval restriction.

**5. The boundary check was underspecified for a security-relevant control.** §4.3 said "canonical path" without stating what that excludes. **Fixed** with four required properties — decode before resolving, resolve symlinks, compare components rather than string prefixes, check before reading — plus adversarial fixtures in FM-L4 and a symlink report in §11.6.

**6. The third falsifier could not fail.** v3's "if the metadata is never used" is false by construction once any validator runs. **Replaced** with a runnable structure-ablation protocol (§14.3): same corpus indexed twice, structured against flat, against a pre-registered query set, with stated interpretations for each outcome and stated limits on what a single author-run trial can support. This instantiates open prediction P2, which the public corpus cannot test.

**7. New: FM-L11, boot-block authority confusion.** v3's boot block declared "which runtime rules apply," which would make any shareable folder a configuration surface for the agent reading it. §9.2 establishes that corpus content is data and never instruction, and FM-L11 supplies a permanent regression check.

Back to: Main Index > Specification / Architecture Sub-Index
