"""Crawl Zoom Support articles: requests + JSON-LD primary, trafilatura fallback, crawl4ai optional."""

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import parse_qs, urlparse

import certifi
import html2text
import urllib3
from bs4 import BeautifulSoup

from zoomkb.constants import DEFAULT_HEADERS, MIN_BODY_LENGTH, REQUEST_TIMEOUT

logger = logging.getLogger("zoomkb.crawler")

_http_pool = urllib3.PoolManager(
    ca_certs=certifi.where(),
    num_pools=4,
    maxsize=10,
    timeout=urllib3.Timeout(connect=10, read=REQUEST_TIMEOUT),
)


@dataclass(frozen=True)
class ExtractedArticle:
    article_id: str
    title: str
    body: str
    source_url: str
    extraction_method: str
    word_count: int


def get_article_id(url: str) -> str:
    query = parse_qs(urlparse(url).query)
    return query.get("sysparm_article", ["unknown"])[0]


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    kept = {}
    if "id" in query:
        kept["id"] = query["id"][0]
    if "sysparm_article" in query:
        kept["sysparm_article"] = query["sysparm_article"][0]
    qs = "&".join(f"{k}={v}" for k, v in kept.items())
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{qs}"


def _html_to_markdown(html: str) -> str:
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0
    h.wrap_links = False
    return h.handle(html).strip()


def _extract_jsonld(html: str) -> Optional[dict]:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("script", type="application/ld+json")
    if not tag or not tag.string:
        return None
    try:
        data = json.loads(tag.string)
        if isinstance(data, list):
            data = next((x for x in data if x.get("@type") == "Article"), None)
        if data and data.get("@type") in ("Article", "TechArticle", "BlogPosting", "NewsArticle"):
            return data
    except (json.JSONDecodeError, AttributeError):
        pass
    return None


def _extract_trafilatura(html: str) -> Optional[Tuple[str, str]]:
    try:
        import trafilatura

        result = trafilatura.extract(
            html,
            output_format="json",
            include_comments=False,
            include_tables=True,
            include_images=False,
        )
        if result:
            data = json.loads(result)
            title = data.get("title", "")
            text = data.get("raw_text", "")
            if text and len(text) > MIN_BODY_LENGTH:
                return title, text
    except Exception as e:
        logger.debug("trafilatura extraction failed: %s", e)
    return None


def _extract_crawl4ai(url: str) -> Optional[Tuple[str, str]]:
    if os.getenv("ZOOMKB_CRAWL4AI") != "1":
        return None
    try:
        from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
        from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
        from crawl4ai.content_filter_strategy import PruningContentFilter
        import asyncio

        async def _run():
            browser_config = BrowserConfig(headless=True)
            md_gen = DefaultMarkdownGenerator(
                content_filter=PruningContentFilter(threshold=0.4, threshold_type="fixed")
            )
            run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, markdown_generator=md_gen)
            async with AsyncWebCrawler(config=browser_config) as crawler:
                result = await crawler.arun(url=url, config=run_config)
            md = result.markdown.fit_markdown or result.markdown.raw_markdown
            title = result.metadata.get("title", "") if result.metadata else ""
            return title, md

        return asyncio.run(_run())
    except Exception as e:
        logger.debug("crawl4ai extraction failed: %s", e)
    return None


def extract_article(html: str, url: str) -> ExtractedArticle:
    """Extract article content from HTML. Priority: JSON-LD > trafilatura > crawl4ai."""
    article_id = get_article_id(url)

    # 1. JSON-LD primary
    ld = _extract_jsonld(html)
    if ld and ld.get("articleBody") and len(ld["articleBody"]) > MIN_BODY_LENGTH:
        title = ld.get("headline") or ld.get("name") or article_id
        body = _html_to_markdown(ld["articleBody"])
        logger.debug("JSON-LD extraction succeeded for %s", article_id)
        return ExtractedArticle(
            article_id=article_id,
            title=title,
            body=body,
            source_url=canonicalize_url(url),
            extraction_method="jsonld",
            word_count=len(body.split()),
        )

    # 2. Trafilatura fallback
    tf_result = _extract_trafilatura(html)
    if tf_result:
        title, body = tf_result
        logger.debug("Trafilatura extraction succeeded for %s", article_id)
        return ExtractedArticle(
            article_id=article_id,
            title=title or article_id,
            body=body,
            source_url=canonicalize_url(url),
            extraction_method="trafilatura",
            word_count=len(body.split()),
        )

    # 3. Optional Crawl4AI fallback
    c4_result = _extract_crawl4ai(url)
    if c4_result:
        title, body = c4_result
        logger.debug("Crawl4AI extraction succeeded for %s", article_id)
        return ExtractedArticle(
            article_id=article_id,
            title=title or article_id,
            body=body,
            source_url=canonicalize_url(url),
            extraction_method="crawl4ai",
            word_count=len(body.split()),
        )

    raise ValueError(
        f"Extraction failed for {url}: "
        f"JSON-LD {'missing' if not ld else 'empty articleBody'}, "
        f"trafilatura returned {len(tf_result[1]) if tf_result else 'no content'}, "
        f"crawl4ai {'disabled' if os.getenv('ZOOMKB_CRAWL4AI') != '1' else 'not installed/failed'}. "
        f"Likely a client-side rendered page. Enable crawl4ai with ZOOMKB_CRAWL4AI=1 or skip this URL."
    )


def fetch_url(url: str) -> str:
    """Fetch raw HTML from URL using urllib3 with certifi CA bundle."""
    logger.info("Fetching %s", url)
    resp = _http_pool.request(
        "GET",
        url,
        headers=DEFAULT_HEADERS,
        retries=urllib3.Retry(total=2, backoff_factor=0.5),
    )
    if resp.status >= 400:
        raise urllib3.exceptions.HTTPError(f"HTTP {resp.status} for {url}")
    return resp.data.decode("utf-8", errors="replace")


def crawl_article(url: str, output_dir: Path, product: str = "zoom-phone") -> dict:
    """Fetch, extract, and save a single article. Returns metadata dict."""
    from zoomkb.classifier import classify_relevance
    from zoomkb.validator import validate_article

    html = fetch_url(url)
    article = extract_article(html, url)

    # Validate before saving
    validate_article(article)

    # Classify relevance
    score, confidence = classify_relevance(article.body, article.title, product)

    # Build frontmatter
    import hashlib
    from datetime import datetime, timezone

    content_hash = hashlib.sha256(article.body.encode("utf-8")).hexdigest()
    frontmatter = f"""---
source_type: zoom_support_article
product: {product}
article_id: {article.article_id}
title: {article.title}
source_url: {article.source_url}
captured_at: {datetime.now(timezone.utc).isoformat()}
retrieval_tool: {article.extraction_method}
relevance_score: {score}
confidence: {confidence}
content_hash: sha256:{content_hash}
status: raw
---

"""

    import re

    slug = re.sub(r"[^a-z0-9]+", "-", article.title.lower()).strip("-")[:80]
    filename = f"{article.article_id}-{slug}.md"
    out_path = output_dir / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)

    full_md = frontmatter + f"# {article.title}\n\n" + article.body + "\n"
    out_path.write_text(full_md, encoding="utf-8")

    logger.info("Saved %s (%s words, score=%d, confidence=%s)",
                filename, article.word_count, score, confidence)

    return {
        "article_id": article.article_id,
        "title": article.title,
        "filename": filename,
        "local_path": str(out_path.relative_to(output_dir.parent.parent)),
        "source_url": article.source_url,
        "extraction_method": article.extraction_method,
        "word_count": article.word_count,
        "relevance_score": score,
        "confidence": confidence,
        "content_hash": f"sha256:{content_hash}",
        "status": "accepted" if confidence == "high" else ("review" if confidence == "medium" else "rejected"),
    }
