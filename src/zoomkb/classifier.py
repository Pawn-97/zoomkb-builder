"""Product relevance classifier: rule-based scoring with optional LLM fallback."""

import json
import logging
import os
from dataclasses import dataclass

from zoomkb.constants import PRODUCT_ALIASES

logger = logging.getLogger("zoomkb.classifier")


@dataclass(frozen=True)
class ClassificationResult:
    score: int
    confidence: str  # high | medium | low
    signals: list[str]


def _score_text(text: str, title: str, product_key: str) -> ClassificationResult:
    config = PRODUCT_ALIASES.get(product_key)
    if not config:
        logger.warning("No alias config for product '%s'", product_key)
        return ClassificationResult(score=0, confidence="low", signals=["unknown product"])

    combined = f"{title}\n{text}".lower()
    signals: list[str] = []
    score = 0

    for signal in config.get("strong_signals", []):
        if signal.lower() in combined:
            score += 5
            signals.append(f"strong: {signal}")

    for signal in config.get("medium_signals", []):
        count = combined.count(signal.lower())
        if count >= 3:
            score += 3
            signals.append(f"medium (x{count}): {signal}")
        elif count >= 1:
            score += 1
            signals.append(f"weak mention: {signal}")

    for signal in config.get("weak_signals", []):
        count = combined.count(signal.lower())
        if count >= 5:
            score += 2
            signals.append(f"frequent weak: {signal}")

    # Negative signals
    for neg in config.get("negative_signals", []):
        if neg.lower() in title.lower():
            score -= 5
            signals.append(f"negative title: {neg}")
        count = combined.count(neg.lower())
        if count >= 3:
            score -= 3
            signals.append(f"negative body: {neg}")

    # Title bonus
    product_name = config["name"].lower()
    if product_name in title.lower():
        score += 3
        signals.append("title contains product name")

    # Word count penalty — very short articles are rarely useful for UX design
    words = len(text.split())
    if words < 80:
        score -= 5
        signals.append(f"penalty: very short ({words} words)")
    elif words < 150:
        score -= 3
        signals.append(f"penalty: short ({words} words)")

    # Confidence tiers
    if score >= 8:
        confidence = "high"
    elif score >= 4:
        confidence = "medium"
    else:
        confidence = "low"

    return ClassificationResult(score=score, confidence=confidence, signals=signals)


def classify_relevance(body: str, title: str, product: str = "zoom-phone") -> tuple[int, str]:
    """Classify article relevance. Returns (score, confidence)."""
    result = _score_text(body, title, product)

    # Optional LLM refinement (disabled by default, enable via env)
    if os.getenv("ZOOMKB_LLM_CLASSIFIER") == "1":
        result = _llm_classify(body, title, product, result)

    logger.debug(
        "Classified %s: score=%d confidence=%s signals=%s",
        title[:50], result.score, result.confidence, result.signals,
    )
    return result.score, result.confidence


def _llm_classify(
    body: str, title: str, product: str, rule_result: ClassificationResult
) -> ClassificationResult:
    """Optional LLM-based classification refinement."""
    try:
        import openai

        client = openai.OpenAI()
        prompt = f"""You are a product relevance classifier for Zoom Support articles.

Product: {product}
Article title: {title}
Article body (first 2000 chars):
{body[:2000]}

Rule-based score: {rule_result.score}
Rule-based confidence: {rule_result.confidence}

Task: Evaluate if this article is primarily about {product}.
Respond with JSON only:
{{
  "score": <int, -10 to 20>,
  "confidence": "high" | "medium" | "low",
  "reasoning": "<brief explanation>"
}}
"""
        resp = client.chat.completions.create(
            model=os.getenv("ZOOMKB_LLM_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0,
        )
        data = json.loads(resp.choices[0].message.content)
        score = data.get("score", rule_result.score)
        confidence = data.get("confidence", rule_result.confidence)
        return ClassificationResult(
            score=score,
            confidence=confidence,
            signals=rule_result.signals + [f"llm: {data.get('reasoning', '')}"],
        )
    except Exception as e:
        logger.debug("LLM classification failed, using rule-based: %s", e)
        return rule_result
