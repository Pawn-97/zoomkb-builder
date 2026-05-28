"""Tests for CLI orchestration behavior."""

import argparse
import json
import os

from zoomkb import cli


def _build_args(**overrides):
    args = {
        "product": "Zoom Rooms",
        "output": "",
        "skip_discover": False,
        "skip_crawl": True,
        "urls": None,
        "url_file": None,
        "dry_run": False,
        "force": False,
    }
    args.update(overrides)
    return argparse.Namespace(**args)


def test_build_derives_output_once_and_passes_to_subcommands(monkeypatch, tmp_path):
    """build --product without --output must not fall back to subcommand defaults."""
    seen_outputs: list[tuple[str, str]] = []

    def _record(name):
        def _cmd(args):
            seen_outputs.append((name, args.output))
            return 0

        return _cmd

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, "cmd_init", _record("init"))
    monkeypatch.setattr(cli, "cmd_discover", _record("discover"))
    monkeypatch.setattr(cli, "cmd_validate", _record("validate"))
    monkeypatch.setattr(cli, "cmd_ingest", _record("ingest"))
    monkeypatch.setattr(cli, "cmd_lint", _record("lint"))

    args = _build_args()

    rc = cli.cmd_build(args)

    assert rc == 0
    assert seen_outputs
    assert {output for _, output in seen_outputs} == {"zoom-rooms-kb"}
    assert not (tmp_path / "zoom-rooms-kb" / "build.lock").exists()


def test_build_refuses_active_lock(monkeypatch, tmp_path):
    """A live build.lock must block a second build."""
    output = tmp_path / "rooms-kb"
    output.mkdir()
    (output / "build.lock").write_text(
        json.dumps({"pid": os.getpid(), "product": "Zoom Rooms"}),
        encoding="utf-8",
    )

    def _fail_if_called(args):
        raise AssertionError("build should stop before init")

    monkeypatch.setattr(cli, "cmd_init", _fail_if_called)

    rc = cli.cmd_build(_build_args(output=str(output)))

    assert rc == 1
    assert (output / "build.lock").exists()


def test_build_releases_lock_and_marks_abort_on_interrupt(monkeypatch, tmp_path):
    """Interrupted builds should not leave a stale lock behind."""
    output = tmp_path / "rooms-kb"

    def _interrupt(args):
        assert (output / "build.lock").exists()
        raise KeyboardInterrupt("test interrupt")

    monkeypatch.setattr(cli, "cmd_init", _interrupt)

    rc = cli.cmd_build(_build_args(output=str(output)))

    assert rc == 130
    assert not (output / "build.lock").exists()
    assert (output / "build-aborted.json").exists()


def test_clean_removes_stale_lock_abort_marker_and_raw_orphans(monkeypatch, tmp_path):
    """clean should remove stale run state and only raw files outside manifest."""
    output = tmp_path / "rooms-kb"
    raw_dir = output / "raw" / "support-articles"
    raw_dir.mkdir(parents=True)
    (output / "manifest.json").write_text(
        json.dumps({
            "articles": [
                {
                    "article_id": "KB0012345",
                    "local_path": "raw/support-articles/KB0012345-test.md",
                }
            ]
        }),
        encoding="utf-8",
    )
    kept = raw_dir / "KB0012345-test.md"
    orphan = raw_dir / "KB0099999-leftover.md"
    kept.write_text("---\narticle_id: KB0012345\n---\nKeep me.\n", encoding="utf-8")
    orphan.write_text("---\narticle_id: KB0099999\n---\nRemove me.\n", encoding="utf-8")
    (output / "build.lock").write_text(
        json.dumps({"pid": 999999, "product": "Zoom Rooms"}),
        encoding="utf-8",
    )
    (output / "build-aborted.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(cli, "_pid_is_running", lambda pid: False)

    rc = cli.cmd_clean(
        argparse.Namespace(output=str(output), dry_run=False, force_lock=False)
    )

    assert rc == 0
    assert kept.exists()
    assert not orphan.exists()
    assert not (output / "build.lock").exists()
    assert not (output / "build-aborted.json").exists()


def test_clean_refuses_active_lock(monkeypatch, tmp_path):
    """clean must not delete files while another build appears active."""
    output = tmp_path / "rooms-kb"
    raw_dir = output / "raw" / "support-articles"
    raw_dir.mkdir(parents=True)
    orphan = raw_dir / "KB0099999-leftover.md"
    orphan.write_text("---\narticle_id: KB0099999\n---\nKeep while active.\n", encoding="utf-8")
    (output / "manifest.json").write_text(json.dumps({"articles": []}), encoding="utf-8")
    (output / "build.lock").write_text(
        json.dumps({"pid": 12345, "product": "Zoom Rooms"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(cli, "_pid_is_running", lambda pid: True)

    rc = cli.cmd_clean(
        argparse.Namespace(output=str(output), dry_run=False, force_lock=False)
    )

    assert rc == 1
    assert orphan.exists()
    assert (output / "build.lock").exists()
