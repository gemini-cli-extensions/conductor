from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Thresholds:
    warn_file_bytes: int
    block_file_bytes: int
    warn_total_bytes: int
    block_total_bytes: int


@dataclass(frozen=True)
class ContextFile:
    path: Path
    size_bytes: int
    status: str


def _default_thresholds() -> Thresholds:
    return Thresholds(
        warn_file_bytes=250 * 1024,
        block_file_bytes=1024 * 1024,
        warn_total_bytes=2 * 1024 * 1024,
        block_total_bytes=5 * 1024 * 1024,
    )


def _resolve_track_id(tracks_md: Path) -> str | None:
    if not tracks_md.exists():
        return None
    content = tracks_md.read_text(encoding="utf-8")
    pattern = r"(?:##|[-])\s*\[\s*([ xX~]?)\s*\]\s*(?:\*\*)?Track:.*?\r?\n" r"\*Link:\s*\[.*?/tracks/(.*?)/\].*?\*"
    matches: list[tuple[str, str]] = []
    for match in re.finditer(pattern, content):
        status_char, track_id = match.groups()
        matches.append((status_char.strip(), track_id.strip()))
    if not matches:
        return None
    for status, track_id in matches:
        if status == "~":
            return track_id
    return matches[0][1]


def _file_status(size_bytes: int, thresholds: Thresholds) -> str:
    if size_bytes >= thresholds.block_file_bytes:
        return "BLOCK"
    if size_bytes >= thresholds.warn_file_bytes:
        return "WARN"
    return "OK"


def build_context_report(repo_root: Path, track_id: str | None, thresholds: Thresholds) -> dict:
    conductor_dir = repo_root / "conductor"
    required_files = [
        conductor_dir / "product.md",
        conductor_dir / "tech-stack.md",
        conductor_dir / "workflow.md",
        conductor_dir / "tracks.md",
    ]
    optional_files = [
        conductor_dir / "product-guidelines.md",
    ]

    code_styleguides = []
    style_dir = conductor_dir / "code_styleguides"
    if style_dir.exists():
        code_styleguides = sorted(p for p in style_dir.glob("*") if p.is_file())

    resolved_track = track_id
    if resolved_track is None:
        resolved_track = _resolve_track_id(conductor_dir / "tracks.md")

    track_files: list[Path] = []
    if resolved_track:
        track_dir = conductor_dir / "tracks" / resolved_track
        track_files = [
            track_dir / "spec.md",
            track_dir / "plan.md",
            track_dir / "metadata.json",
            track_dir / "index.md",
        ]

    files = []
    missing = []
    for path in required_files + optional_files + code_styleguides + track_files:
        if path.exists():
            size_bytes = path.stat().st_size
            files.append(ContextFile(path=path, size_bytes=size_bytes, status=_file_status(size_bytes, thresholds)))
        elif path in required_files or (path in track_files and path.name in {"spec.md", "plan.md", "metadata.json"}):
            missing.append(path)

    total_bytes = sum(item.size_bytes for item in files)
    total_status = "OK"
    if total_bytes >= thresholds.block_total_bytes:
        total_status = "BLOCK"
    elif total_bytes >= thresholds.warn_total_bytes:
        total_status = "WARN"

    return {
        "track_id": resolved_track,
        "files": files,
        "missing": missing,
        "total_bytes": total_bytes,
        "total_status": total_status,
    }


def _format_bytes(size: int) -> str:
    return f"{size / 1024:.1f} KB"


def main() -> int:
    parser = argparse.ArgumentParser(description="Report Conductor context size and key files.")
    parser.add_argument("--track-id", help="Track id to report (defaults to first in-progress track).")
    parser.add_argument("--warn-file-kb", type=int, default=250)
    parser.add_argument("--block-file-kb", type=int, default=1024)
    parser.add_argument("--warn-total-kb", type=int, default=2048)
    parser.add_argument("--block-total-kb", type=int, default=5120)
    args = parser.parse_args()

    thresholds = Thresholds(
        warn_file_bytes=args.warn_file_kb * 1024,
        block_file_bytes=args.block_file_kb * 1024,
        warn_total_bytes=args.warn_total_kb * 1024,
        block_total_bytes=args.block_total_kb * 1024,
    )

    repo_root = Path(__file__).resolve().parents[1]
    report = build_context_report(repo_root, args.track_id, thresholds)

    track_label = report["track_id"] or "none"
    print(f"Context report (track: {track_label})")  # noqa: T201
    for item in report["files"]:
        rel_path = item.path.relative_to(repo_root)
        print(f"{item.status}  {_format_bytes(item.size_bytes)}  {rel_path}")  # noqa: T201

    print(f"TOTAL  {_format_bytes(report['total_bytes'])}  {report['total_status']}")  # noqa: T201

    if report["missing"]:
        print("Missing required context files:")  # noqa: T201
        for path in report["missing"]:
            print(f"- {path.relative_to(repo_root)}")  # noqa: T201
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
