"""Tests for discovery candidate filtering."""

from zoomkb.discover import _matches_product


def test_untitled_articles_do_not_match_by_default():
    matched, signals = _matches_product(
        None,
        "https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0012345",
        "zoom-rooms",
    )

    assert matched is False
    assert "use --fetch-titles or --broad-discovery" in signals[0]


def test_broad_discovery_explicitly_accepts_untitled_articles():
    matched, signals = _matches_product(
        None,
        "https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0012345",
        "zoom-rooms",
        allow_untitled=True,
    )

    assert matched is True
    assert "broad discovery" in signals[0]


def test_untitled_url_can_still_match_product_signal():
    matched, signals = _matches_product(
        None,
        "https://support.zoom.com/hc/en/zoom-rooms/article?sysparm_article=KB0012345",
        "zoom-rooms",
    )

    assert matched is True
    assert any("zoom rooms" in signal for signal in signals)
