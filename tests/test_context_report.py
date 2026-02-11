from pathlib import Path

from scripts.context_report import Thresholds, build_context_report


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_context_report_resolves_track(tmp_path):
    repo_root = tmp_path
    conductor_dir = repo_root / "conductor"
    _write(conductor_dir / "product.md", "product")
    _write(conductor_dir / "tech-stack.md", "stack")
    _write(conductor_dir / "workflow.md", "workflow")
    tracks_entry = "- [~] **Track: Test**\n" "*Link: [./conductor/tracks/t1/](./conductor/tracks/t1/)*\n"
    _write(conductor_dir / "tracks.md", tracks_entry)

    track_dir = conductor_dir / "tracks" / "t1"
    _write(track_dir / "spec.md", "spec")
    _write(track_dir / "plan.md", "plan")
    _write(track_dir / "metadata.json", "{}")

    thresholds = Thresholds(1, 3, 10, 20)
    report = build_context_report(repo_root, None, thresholds)

    assert report["track_id"] == "t1"
    assert report["missing"] == []
    assert report["total_bytes"] > 0


def test_context_report_flags_sizes(tmp_path):
    repo_root = tmp_path
    conductor_dir = repo_root / "conductor"
    _write(conductor_dir / "product.md", "x" * 2)
    _write(conductor_dir / "tech-stack.md", "x")
    _write(conductor_dir / "workflow.md", "x")
    tracks_entry = "- [ ] **Track: Test**\n" "*Link: [./conductor/tracks/t2/](./conductor/tracks/t2/)*\n"
    _write(conductor_dir / "tracks.md", tracks_entry)

    track_dir = conductor_dir / "tracks" / "t2"
    _write(track_dir / "spec.md", "x")
    _write(track_dir / "plan.md", "x")
    _write(track_dir / "metadata.json", "{}")

    thresholds = Thresholds(
        warn_file_bytes=1,
        block_file_bytes=3,
        warn_total_bytes=5,
        block_total_bytes=20,
    )
    report = build_context_report(repo_root, "t2", thresholds)

    statuses = {item.path.name: item.status for item in report["files"]}
    assert statuses["product.md"] == "WARN"
    assert report["total_status"] in {"WARN", "BLOCK", "OK"}
