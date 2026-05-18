"""Batch extract entities from .prompt.md files via OpenAI API.

Pipeline (middle step): reads extraction-queue/<article_id>.prompt.md
→ calls OpenAI LLM → writes extraction-queue/<article_id>.result.json
"""

import json
import logging
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

logger = logging.getLogger("zoomkb.extractor")

_JSON_BLOCK_RE = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```")


def _parse_prompt(prompt_path: Path) -> tuple[str, str, str]:
    """Split .prompt.md into article_id, instructions section, and article content.

    Returns (article_id, instructions, article_content).
    """
    text = prompt_path.read_text(encoding="utf-8")
    article_id = prompt_path.stem.replace(".prompt", "")
    return article_id, text


def extract_article(
    prompt_path: Path,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    temperature: float = 0.2,
) -> dict:
    """Process single .prompt.md file via OpenAI API. Returns parsed result dict.

    Returns dict with keys: article_id, concepts, user_roles, task_flows,
    constraints, ux_patterns. On error returns {"_error": "..."}.
    """
    article_id, prompt_text = _parse_prompt(prompt_path)

    api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return {"_error": "No API key. Set OPENAI_API_KEY env var."}

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise knowledge extraction engine. Always output valid JSON exactly matching the requested schema. No markdown outside the JSON block.",
                },
                {"role": "user", "content": prompt_text},
            ],
        )

        raw = response.choices[0].message.content.strip()

        # Try to extract JSON from markdown code block first
        m = _JSON_BLOCK_RE.search(raw)
        if m:
            raw = m.group(1)

        result = json.loads(raw)

    except ImportError:
        raise RuntimeError(
            "openai package required. Install with: pip install 'zoomkb[llm]'"
        )
    except json.JSONDecodeError as e:
        logger.warning("JSON parse failed for %s: %s. Raw: %.200s", article_id, e, raw)
        return {"_error": f"JSON parse failed: {e}", "_raw": raw[:500]}
    except Exception as e:
        logger.error("Extraction failed for %s: %s", article_id, e)
        return {"_error": str(e)}

    # Validate result has expected keys
    expected = {"concepts", "user_roles", "task_flows", "constraints", "ux_patterns"}
    if not isinstance(result, dict):
        return {"_error": "Response is not a JSON object"}

    # Ensure all expected keys exist
    for key in expected:
        result.setdefault(key, [])

    result["article_id"] = result.get("article_id", article_id)
    return result


def batch_extract(
    output_dir: Path,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    max_workers: int = 3,
    force: bool = False,
    article_ids: Optional[list[str]] = None,
    dry_run: bool = False,
) -> dict:
    """Process all .prompt.md files in extraction-queue/.

    Args:
        output_dir: KB output directory (contains extraction-queue/, raw/, etc.)
        model: OpenAI model name.
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        max_workers: Parallel extraction workers (default 3).
        force: Re-extract even if .result.json exists.
        article_ids: Process specific articles only.
        dry_run: Print what would be done without calling API.

    Returns stats dict.
    """
    queue_dir = output_dir / "extraction-queue"
    if not queue_dir.exists():
        logger.error("extraction-queue/ not found. Run 'zoomkb ingest --prepare' first.")
        return {"error": "extraction-queue/ not found", "extracted": 0, "failed": 0, "skipped": 0}

    prompt_files = sorted(queue_dir.glob("*.prompt.md"))

    # Filter by article_ids
    if article_ids:
        aid_set = set(article_ids)
        prompt_files = [p for p in prompt_files if p.stem.replace(".prompt", "") in aid_set]

    stats: dict = {
        "extracted": 0, "failed": 0, "skipped": 0,
        "queued": len(prompt_files), "would_extract": 0,
    }

    if not prompt_files:
        logger.warning("No .prompt.md files in extraction-queue/. Run 'zoomkb ingest --prepare' first.")
        return stats

    to_process: list[Path] = []
    for pf in prompt_files:
        result_path = pf.parent / (pf.stem.replace(".prompt", "") + ".result.json")
        if result_path.exists() and not force:
            stats["skipped"] += 1
            continue
        to_process.append(pf)

    if dry_run:
        stats["dry_run"] = True
        stats["would_extract"] = len(to_process)
        return stats

    if not to_process:
        return stats

    api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        logger.error("OPENAI_API_KEY not set. Cannot proceed.")
        stats["error"] = "OPENAI_API_KEY not set"
        return stats

    logger.info("Extracting %d articles (model=%s, workers=%d)", len(to_process), model, max_workers)

    def _process_one(prompt_path: Path) -> tuple[str, bool, str]:
        aid = prompt_path.stem.replace(".prompt", "")
        result_path = prompt_path.parent / (aid + ".result.json")
        try:
            result = extract_article(prompt_path, model=model, api_key=api_key)
            if "_error" in result:
                return aid, False, result["_error"]
            result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
            return aid, True, ""
        except Exception as e:
            return aid, False, str(e)

    errors: list[str] = []
    extracted_count = 0
    failed_count = 0

    if max_workers <= 1:
        for pf in to_process:
            aid, ok, err = _process_one(pf)
            if ok:
                extracted_count += 1
                logger.info("  %s: OK", aid)
            else:
                failed_count += 1
                errors.append(f"{aid}: {err}")
                logger.error("  %s: %s", aid, err)
            time.sleep(0.5)  # Rate limit padding
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(_process_one, pf): pf for pf in to_process}
            for future in as_completed(futures):
                aid, ok, err = future.result()
                if ok:
                    extracted_count += 1
                    logger.info("  %s: OK", aid)
                else:
                    failed_count += 1
                    errors.append(f"{aid}: {err}")
                    logger.error("  %s: %s", aid, err)

    stats["extracted"] = extracted_count
    stats["failed"] = failed_count
    if errors:
        stats["errors"] = errors

    logger.info("Batch extract complete: %d OK, %d failed, %d skipped",
                 extracted_count, failed_count, stats["skipped"])
    return stats
