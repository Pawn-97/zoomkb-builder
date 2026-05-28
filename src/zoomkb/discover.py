"""Discovery engine: robots.txt → sitemap → article URLs → candidate filter."""

import html
import json
import logging
import re
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlparse

import certifi
import urllib3
from bs4 import BeautifulSoup

from zoomkb.constants import DEFAULT_HEADERS, REQUEST_TIMEOUT

logger = logging.getLogger("zoomkb.discover")

_http_pool = urllib3.PoolManager(
    ca_certs=certifi.where(),
    num_pools=16,
    maxsize=16,
    timeout=urllib3.Timeout(connect=10, read=REQUEST_TIMEOUT),
)

SITEMAP_NS = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def _fetch_text(url: str) -> str:
    resp = _http_pool.request("GET", url, headers=DEFAULT_HEADERS, retries=2)
    if resp.status >= 400:
        raise urllib3.exceptions.HTTPError(f"HTTP {resp.status} for {url}")
    return resp.data.decode("utf-8", errors="replace")


def _find_sitemaps(robots_txt: str) -> list[str]:
    """Parse robots.txt for Sitemap directives."""
    sitemaps = []
    for line in robots_txt.splitlines():
        if line.lower().startswith("sitemap:"):
            url = line.split(":", 1)[1].strip()
            sitemaps.append(url)
    return sitemaps


def _parse_urlset_root(root) -> list[dict]:
    """Parse urlset XML element and return URL entries with loc + lastmod."""
    entries = []
    for url_elem in root.findall("ns:url", SITEMAP_NS):
        loc = url_elem.find("ns:loc", SITEMAP_NS)
        if loc is not None and loc.text:
            entry = {"loc": html.unescape(loc.text).strip()}
            lastmod = url_elem.find("ns:lastmod", SITEMAP_NS)
            if lastmod is not None and lastmod.text:
                entry["lastmod"] = lastmod.text.strip()
            entries.append(entry)
    return entries


def _fetch_urlset(url: str) -> list[dict]:
    """Fetch single sitemap and return URL entries with loc + lastmod."""
    try:
        text = _fetch_text(url)
        root = ET.fromstring(text)
        return _parse_urlset_root(root)
    except Exception as e:
        logger.warning("Failed to parse sitemap %s: %s", url, e)
        return []


def canonicalize_url(url: str) -> str:
    """Strip tracking params, keep only article ID params."""
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    kept = {}
    if "id" in query:
        kept["id"] = query["id"][0]
    if "sysparm_article" in query:
        kept["sysparm_article"] = query["sysparm_article"][0]
    qs = "&".join(f"{k}={v}" for k, v in kept.items())
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{qs}"


def is_article_url(url: str) -> bool:
    """Check if URL is a Zoom Support article page."""
    parsed = urlparse(url)
    if not parsed.path.startswith("/hc/"):
        return False
    query = parse_qs(parsed.query)
    return "sysparm_article" in query or "id" in query


def extract_locale(url: str) -> Optional[str]:
    """Extract locale from URL path, e.g., /hc/en/ → 'en'."""
    m = re.match(r"/hc/([a-z]{2})/", urlparse(url).path)
    return m.group(1) if m else None


def is_english_article(url: str) -> bool:
    """Check if URL is an English-language article."""
    return extract_locale(url) == "en"


def extract_title_from_url(url: str) -> Optional[str]:
    """Fetch just enough HTML to grab <title> for candidate pre-filtering."""
    try:
        text = _fetch_text(url)
        soup = BeautifulSoup(text, "html.parser")
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            return title_tag.string.strip()
    except Exception as e:
        logger.debug("Failed to fetch title for %s: %s", url, e)
    return None


def _matches_product(
    title: Optional[str],
    url: str,
    product_key: str,
    allow_untitled: bool = False,
) -> tuple[bool, list[str]]:
    """Quick heuristic: does title/URL match product signals?

    Untitled sitemap entries are only accepted in explicit broad-discovery mode.
    Product relevance is judged more deeply by the classifier during crawl.
    """
    from zoomkb.constants import PRODUCT_ALIASES

    config = PRODUCT_ALIASES.get(product_key)
    if not config:
        return True, ["unknown product, accepting all"]

    combined = re.sub(r"[-_]+", " ", f"{title or ''} {url}".lower())
    signals: list[str] = []
    seen_lower: set[str] = set()  # Deduplicate overlapping signal names

    product_name = config["name"].lower()
    if product_name in combined:
        tag = f"contains {product_name}"
        if tag not in seen_lower:
            signals.append(tag)
            seen_lower.add(tag)

    for s in config.get("strong_signals", []):
        sl = s.lower()
        if sl in combined and sl not in seen_lower:
            signals.append(f"strong: {s}")
            seen_lower.add(sl)

    for s in config.get("medium_signals", []):
        sl = s.lower()
        if sl in combined and sl not in seen_lower:
            signals.append(f"medium: {s}")
            seen_lower.add(sl)

    if signals:
        return True, signals

    if title is None:
        if allow_untitled:
            return True, ["broad discovery: no title available, accepting for classifier"]
        return False, ["no title available; use --fetch-titles or --broad-discovery"]

    return False, signals


def _fetch_titles_parallel(
    entries: list[dict],
    product_key: str,
    max_workers: int = 5,
    max_candidates: int = 0,
    allow_untitled: bool = False,
) -> tuple[list[dict], list[dict]]:
    """Fetch page titles in parallel and filter by product keyword match.

    Falls back to sequential fetching if ThreadPoolExecutor fails
    (e.g., urllib3 SSL issues in threaded context on macOS LibreSSL).
    """
    candidates: list[dict] = []
    rejected: list[dict] = []
    total = len(entries)

    def _record(title: Optional[str], entry: dict) -> dict:
        matched, signals = _matches_product(
            title,
            entry["canonical_url"],
            product_key,
            allow_untitled=allow_untitled,
        )
        return {
            "url": entry["canonical_url"],
            "original_url": entry["loc"],
            "title": title,
            "lastmod": entry.get("lastmod"),
            "matched": matched,
            "matched_signals": signals,
        }

    def _process_one(entry: dict) -> Optional[dict]:
        try:
            title = extract_title_from_url(entry["loc"])
        except Exception:
            title = None
        return _record(title, entry)

    # Try parallel first, fall back to sequential on failure
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_entry = {}
            for i, entry in enumerate(entries):
                # Check early termination
                if max_candidates > 0 and len(candidates) >= max_candidates:
                    break
                future = executor.submit(extract_title_from_url, entry["loc"])
                future_to_entry[future] = (i, entry)

            done_count = 0
            for future in as_completed(future_to_entry):
                i, entry = future_to_entry[future]
                done_count += 1

                try:
                    title = future.result()
                except Exception:
                    title = None

                record = _record(title, entry)
                if record["matched"]:
                    candidates.append(record)
                else:
                    rejected.append(record)

                if done_count % 100 == 0 or done_count == total:
                    logger.info(
                        "Title fetch: %d/%d (%d candidates, %d rejected)",
                        done_count, total, len(candidates), len(rejected),
                    )

                if max_candidates > 0 and len(candidates) >= max_candidates:
                    for f in future_to_entry:
                        f.cancel()
                    break

    except Exception as e:
        logger.warning(
            "Parallel title fetch failed (%s), falling back to sequential", e
        )
        # Sequential fallback
        for i, entry in enumerate(entries):
            if max_candidates > 0 and len(candidates) >= max_candidates:
                break
            try:
                title = extract_title_from_url(entry["loc"])
            except Exception:
                title = None
            record = _record(title, entry)
            if record["matched"]:
                candidates.append(record)
            else:
                rejected.append(record)

            if (i + 1) % 50 == 0 or i + 1 == total:
                logger.info(
                    "Title fetch (seq): %d/%d (%d candidates, %d rejected)",
                    i + 1, total, len(candidates), len(rejected),
                )

    return candidates, rejected


def discover_articles(
    source_root: str,
    product: str,
    output_dir: Path,
    fetch_titles: bool = False,
    max_workers: int = 5,
    max_candidates: int = 0,
    locale: Optional[str] = "en",
    broad_discovery: bool = False,
) -> dict:
    """Run full discovery: robots.txt → sitemaps → article URLs → candidate filter.

    When fetch_titles=True, titles are fetched in parallel and filtered by
    product keyword match. Set max_candidates > 0 for early termination.
    Set locale (e.g., 'en') to filter articles by language path (/hc/{locale}/).
    Pass locale=None to include all languages.
    """
    robots_url = source_root.rstrip("/") + "/robots.txt"
    logger.info("Fetching %s", robots_url)

    try:
        robots_txt = _fetch_text(robots_url)
    except Exception as e:
        logger.error("Failed to fetch robots.txt: %s", e)
        return {"error": str(e)}

    sitemap_urls = _find_sitemaps(robots_txt)
    logger.info("Found %d sitemap(s)", len(sitemap_urls))

    all_urls: list[dict] = []
    for sm_url in sitemap_urls:
        try:
            text = _fetch_text(sm_url)
            root = ET.fromstring(text)
            tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
            if tag == "sitemapindex":
                child_urls = [
                    html.unescape(loc.text).strip()
                    for loc in root.findall(".//ns:loc", SITEMAP_NS)
                    if loc.text
                ]
                child_labels = [
                    parse_qs(urlparse(u).query).get("sitemapConfigId", ["?"])[0][:30]
                    for u in child_urls
                ]
                logger.info(
                    "Sitemap index → %d child sitemaps: %s",
                    len(child_urls), child_labels,
                )
                for child in child_urls:
                    all_urls.extend(_fetch_urlset(child))
            else:
                all_urls.extend(_parse_urlset_root(root))
        except Exception as e:
            logger.warning("Failed to parse sitemap %s: %s", sm_url, e)

    logger.info("Total URLs from sitemaps: %d", len(all_urls))

    # Filter to article URLs
    article_entries = [e for e in all_urls if is_article_url(e["loc"])]
    logger.info("Article URLs: %d", len(article_entries))

    # Deduplicate by canonical URL
    seen: set[str] = set()
    deduped: list[dict] = []
    for entry in article_entries:
        canonical = canonicalize_url(entry["loc"])
        if canonical not in seen:
            seen.add(canonical)
            entry["canonical_url"] = canonical
            deduped.append(entry)

    logger.info("After dedup: %d", len(deduped))

    # Locale filter — only keep articles matching the requested language
    before_locale = len(deduped)
    if locale:
        deduped = [e for e in deduped if extract_locale(e["canonical_url"]) == locale]
        logger.info("After locale filter (%s): %d (removed %d)", locale, len(deduped), before_locale - len(deduped))
    else:
        logger.info("No locale filter, keeping all %d", len(deduped))

    # Product filter — parallel title fetch when enabled
    if fetch_titles:
        logger.info(
            "Fetching titles in parallel (workers=%d, max_candidates=%d)...",
            max_workers, max_candidates,
        )
        candidates, rejected = _fetch_titles_parallel(
            deduped,
            product,
            max_workers=max_workers,
            max_candidates=max_candidates,
            allow_untitled=broad_discovery,
        )
    else:
        if not broad_discovery:
            logger.warning(
                "Title fetching disabled and broad discovery not enabled; "
                "untitled sitemap entries must match product signals in their URL."
            )
        candidates = []
        rejected = []
        for entry in deduped:
            matched, signals = _matches_product(
                None,
                entry["loc"],
                product,
                allow_untitled=broad_discovery,
            )
            record = {
                "url": entry["canonical_url"],
                "original_url": entry["loc"],
                "title": None,
                "lastmod": entry.get("lastmod"),
                "matched": matched,
                "matched_signals": signals,
            }
            if matched:
                candidates.append(record)
                if max_candidates > 0 and len(candidates) >= max_candidates:
                    break
            else:
                rejected.append(record)

    logger.info("Candidates: %d, Rejected: %d", len(candidates), len(rejected))

    # Save outputs
    review_dir = output_dir / "review"
    review_dir.mkdir(parents=True, exist_ok=True)

    candidate_path = review_dir / "candidate-articles.json"
    candidate_path.write_text(
        json.dumps(
            {"product": product, "count": len(candidates), "candidates": candidates},
            indent=2,
        ),
        encoding="utf-8",
    )

    rejected_path = review_dir / "rejected-articles.json"
    rejected_path.write_text(
        json.dumps(
            {"product": product, "count": len(rejected), "rejected": rejected},
            indent=2,
        ),
        encoding="utf-8",
    )

    return {
        "sitemaps_found": len(sitemap_urls),
        "total_urls": len(all_urls),
        "article_urls": len(article_entries),
        "after_dedup": len(deduped),
        "candidates": len(candidates),
        "rejected": len(rejected),
        "candidate_file": str(candidate_path),
        "rejected_file": str(rejected_path),
    }
