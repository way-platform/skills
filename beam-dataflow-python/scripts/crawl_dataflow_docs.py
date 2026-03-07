#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import time
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as md

BASE_URL = "https://docs.cloud.google.com"
SEED_URL = f"{BASE_URL}/dataflow/docs/overview"
USER_AGENT = "way-platform-dataflow-reference-crawler/1.0"
ROOT_PATH_PREFIX = "/dataflow/docs/"

ALLOWED_CODE_LANGS = {
    "python",
    "py",
    "bash",
    "shell",
    "sh",
    "console",
    "terminal",
    "none",
    "text",
    "plaintext",
}
BLOCKED_CODE_LANGS = {
    "java",
    "go",
    "javascript",
    "js",
    "typescript",
    "ts",
    "c",
    "cpp",
    "c++",
    "csharp",
    "cs",
    "kotlin",
    "scala",
    "ruby",
    "php",
    "r",
    "yaml",
    "yml",
    "json",
    "sql",
    "xml",
}

PYTHON_HINT_PATTERNS = [
    re.compile(r"\bpython\b", re.IGNORECASE),
    re.compile(r"\bapache[_ -]?beam\b", re.IGNORECASE),
    re.compile(r"\bdataflowrunner\b", re.IGNORECASE),
]

EXCLUDE_PATH_PATTERNS = [
    re.compile(r"^/dataflow/docs/guides/create-pipeline-java/?$"),
    re.compile(r"^/dataflow/docs/guides/create-pipeline-go/?$"),
    re.compile(r"^/dataflow/docs/quickstarts/create-pipeline-java/?$"),
    re.compile(r"^/dataflow/docs/quickstarts/create-pipeline-go/?$"),
    re.compile(r"^/dataflow/docs/quickstarts/quickstart-go/?$"),
    re.compile(r"^/dataflow/docs/guides/migrate-java-1-to-2/?$"),
    re.compile(r"^/dataflow/docs/guides/sql/.+"),
    re.compile(r"^/dataflow/docs/reference/sql/.+"),
    re.compile(r"^/dataflow/docs/tutorials/ecommerce-java/?$"),
]

DROP_SELECTORS = [
    "script",
    "style",
    "noscript",
    "devsite-language-selector",
    "devsite-search",
    "devsite-toc",
    "nav",
    ".devsite-article-meta",
    ".devsite-book-nav-wrapper",
    ".devsite-page-rating",
    ".devsite-source-link",
    ".devsite-thumb-rating",
    ".devsite-article-footer",
    ".devsite-recommendations",
    ".devsite-banner",
]


@dataclass
class CrawlResult:
    source_url: str
    path: str
    output_file: str
    status: str
    reason: str = ""
    page_title: str = ""
    last_updated: str = ""


def normalize_path(url_or_path: str) -> str:
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        path = urlparse(url_or_path).path or "/"
    else:
        path = url_or_path
    if not path.startswith("/"):
        path = "/" + path
    path = re.sub(r"/+", "/", path)
    return path.rstrip("/") if len(path) > 1 else path


def canonical_dataflow_doc_path(href: str, current_url: str) -> str | None:
    if not href or href.startswith("#"):
        return None
    absolute = urljoin(current_url, href)
    parsed = urlparse(absolute)
    if parsed.scheme not in {"http", "https"}:
        return None
    if parsed.netloc not in {"docs.cloud.google.com", "cloud.google.com"}:
        return None
    path = normalize_path(parsed.path)
    if not path.startswith(ROOT_PATH_PREFIX):
        return None
    if "." in Path(path).name:
        return None
    return path


def should_exclude_path(path: str) -> bool:
    return any(p.match(path) for p in EXCLUDE_PATH_PATTERNS)


def fetch(session: requests.Session, url: str) -> str:
    for attempt in range(3):
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            return r.text
        except requests.RequestException:
            if attempt == 2:
                raise
            time.sleep(0.5 * (attempt + 1))
    raise RuntimeError("unreachable")


def extract_content(soup: BeautifulSoup) -> Tag:
    for selector in ["article .devsite-article-body", "article", "main"]:
        node = soup.select_one(selector)
        if isinstance(node, Tag):
            return node
    raise ValueError("main content container not found")


def find_last_updated(soup: BeautifulSoup) -> str:
    for node in soup.find_all(string=re.compile(r"Last updated", re.IGNORECASE)):
        if node.parent:
            text = " ".join(node.parent.get_text(" ", strip=True).split())
            if text:
                return text
    return ""


def language_token_from_tag(tag: Tag) -> str | None:
    syntax = tag.get("syntax")
    if isinstance(syntax, str) and syntax.strip():
        return syntax.strip().lower()
    for cls in tag.get("class", []):
        if cls.startswith("language-"):
            return cls.removeprefix("language-").strip().lower()
    data_lang = tag.get("data-lang")
    if isinstance(data_lang, str) and data_lang.strip():
        return data_lang.strip().lower()
    return None


def classify_code_language(pre: Tag) -> str | None:
    if lang := language_token_from_tag(pre):
        return lang
    code = pre.find("code")
    if isinstance(code, Tag) and (lang := language_token_from_tag(code)):
        return lang
    for ancestor in pre.parents:
        if isinstance(ancestor, Tag) and (lang := language_token_from_tag(ancestor)):
            return lang
    return None


def should_keep_code_block(pre: Tag) -> bool:
    lang = classify_code_language(pre)
    if lang is None:
        text = pre.get_text("\n", strip=True)
        if re.search(r"\b(go run|mvn\b|gradle\b|exec:java|java\s+-|javac\b)\b", text):
            return False
        return any(x in text for x in ["gcloud ", "python ", "pip ", "export ", "--project", "--region"])
    if lang in ALLOWED_CODE_LANGS:
        return True
    if lang in BLOCKED_CODE_LANGS:
        return False
    return True


def clean_dom(content: Tag) -> Tag:
    for selector in DROP_SELECTORS:
        for node in content.select(selector):
            node.decompose()

    for pre in list(content.find_all("pre")):
        if should_keep_code_block(pre):
            continue
        if isinstance(pre.parent, Tag) and pre.parent.name == "devsite-code":
            pre.parent.decompose()
        else:
            pre.decompose()

    for node in list(content.select("[aria-hidden='true']")):
        if node.find("pre"):
            node.decompose()

    return content


def markdown_from_html(content: Tag) -> str:
    text = md(str(content), heading_style="ATX", bullets="-", wrap=False, strip=["span"])
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text + "\n"


def page_is_python_relevant(path: str, content: Tag, markdown_body: str) -> bool:
    lowered_path = path.lower()
    if "python" in lowered_path:
        return True
    if should_exclude_path(path):
        return False
    if re.search(r"(^|/)(java|go)(/|$)", lowered_path):
        return False

    for pattern in PYTHON_HINT_PATTERNS:
        if pattern.search(markdown_body):
            return True

    stats = Counter()
    for pre in content.find_all("pre"):
        lang = classify_code_language(pre)
        if not lang:
            continue
        if lang in {"python", "py"}:
            stats["python"] += 1
        if lang in BLOCKED_CODE_LANGS:
            stats["blocked"] += 1

    if stats["python"] > 0:
        return True
    if stats["blocked"] == 0:
        return True
    return False


def output_path_for(path: str, output_root: Path) -> Path:
    return output_root / f"{path.strip('/')}.md"


def discover_paths(session: requests.Session, seed_url: str, delay: float, discover_limit: int | None) -> list[str]:
    queue = deque([normalize_path(seed_url)])
    seen: set[str] = set()

    while queue:
        path = queue.popleft()
        if path in seen:
            continue
        seen.add(path)
        if len(seen) % 25 == 0:
            print(f"[discover] visited {len(seen)} pages")
        if discover_limit is not None and len(seen) >= discover_limit:
            break

        url = f"{BASE_URL}{path}"
        try:
            html = fetch(session, url)
        except Exception:
            continue

        soup = BeautifulSoup(html, "lxml")
        for anchor in soup.select("a[href]"):
            href = anchor.get("href")
            if not isinstance(href, str):
                continue
            child = canonical_dataflow_doc_path(href, url)
            if child and child not in seen:
                queue.append(child)
        time.sleep(delay)

    return sorted(seen)


def run(output_root: Path, manifest_file: Path, limit: int | None, delay: float, discover_limit: int | None) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    manifest_file.parent.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    discovered_paths = discover_paths(session, SEED_URL, delay=delay, discover_limit=discover_limit)
    paths = [p for p in discovered_paths if not should_exclude_path(p)]
    if limit is not None:
        paths = paths[:limit]

    fetched_at = dt.datetime.now(dt.timezone.utc).isoformat()
    results: list[CrawlResult] = []

    print(f"Discovered {len(discovered_paths)} Dataflow docs paths")
    print(f"After exclusions: {len(paths)} paths")

    for idx, path in enumerate(paths, start=1):
        source_url = f"{BASE_URL}{path}"
        out_file = output_path_for(path, output_root)
        out_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            html = fetch(session, source_url)
            soup = BeautifulSoup(html, "lxml")
            title = soup.title.get_text(strip=True) if soup.title else ""
            updated = find_last_updated(soup)
            content = extract_content(soup)
            raw_body = markdown_from_html(content)

            if not page_is_python_relevant(path, content, raw_body):
                results.append(CrawlResult(source_url, path, str(out_file), "skipped", "not python-relevant", title, updated))
                print(f"[{idx:03d}/{len(paths):03d}] skip {path}")
                time.sleep(delay)
                continue

            cleaned = clean_dom(content)
            markdown_body = markdown_from_html(cleaned)
            frontmatter = [
                "---",
                f"source_url: {source_url}",
                f"fetched_at_utc: {fetched_at}",
                f"page_title: {json.dumps(title)}",
                f"last_updated: {json.dumps(updated)}",
                "---",
                "",
            ]
            out_file.write_text("\n".join(frontmatter) + markdown_body, encoding="utf-8")
            results.append(CrawlResult(source_url, path, str(out_file), "ok", page_title=title, last_updated=updated))
            print(f"[{idx:03d}/{len(paths):03d}] ok   {path}")
        except Exception as exc:  # noqa: BLE001
            results.append(CrawlResult(source_url, path, str(out_file), "error", str(exc)))
            print(f"[{idx:03d}/{len(paths):03d}] fail {path} :: {exc}")
        time.sleep(delay)

    manifest = {
        "seed_url": SEED_URL,
        "base_url": BASE_URL,
        "generated_at_utc": fetched_at,
        "path_prefix": ROOT_PATH_PREFIX,
        "excluded_path_patterns": [p.pattern for p in EXCLUDE_PATH_PATTERNS],
        "allowed_code_languages": sorted(ALLOWED_CODE_LANGS),
        "blocked_code_languages": sorted(BLOCKED_CODE_LANGS),
        "discovered_paths": discovered_paths,
        "results": [r.__dict__ for r in results],
    }
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    ok_count = sum(r.status == "ok" for r in results)
    skip_count = sum(r.status == "skipped" for r in results)
    fail_count = sum(r.status == "error" for r in results)
    print(f"\nDone: {ok_count} ok, {skip_count} skipped, {fail_count} failed")
    print(f"Manifest: {manifest_file}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawl Dataflow docs and export python-focused markdown references.")
    parser.add_argument("--output-dir", default="beam-dataflow-python/references/dataflow")
    parser.add_argument("--manifest", default="beam-dataflow-python/references/dataflow/_crawl-manifest.json")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0.05)
    parser.add_argument("--discover-limit", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(
        output_root=Path(args.output_dir),
        manifest_file=Path(args.manifest),
        limit=args.limit,
        delay=args.delay,
        discover_limit=args.discover_limit,
    )


if __name__ == "__main__":
    main()
