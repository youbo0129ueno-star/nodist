from __future__ import annotations

import json
import os
from pathlib import Path


def normalize_progress(progress: dict | None) -> dict[str, list[str]]:
    progress = progress or {}
    return {
        "completed_levels": list(progress.get("completed_levels", [])),
        "unlocked_levels": list(progress.get("unlocked_levels", [])),
        "locked_levels": list(progress.get("locked_levels", [])),
    }


def get_progress_path(base_dir: str | Path | None = None) -> Path:
    if base_dir is not None:
        base = Path(base_dir)
    else:
        base = Path(os.environ.get("NODIST_HOME", Path.home()))
    return base / ".nodist" / "progress.json"


def load_progress(base_dir: str | Path | None = None) -> dict[str, list[str]]:
    path = get_progress_path(base_dir)
    if not path.exists():
        return normalize_progress(None)

    try:
        return normalize_progress(json.loads(path.read_text(encoding="utf-8")))
    except json.JSONDecodeError:
        return normalize_progress(None)


def save_progress(
    progress: dict[str, list[str]], base_dir: str | Path | None = None
) -> dict[str, list[str]]:
    path = get_progress_path(base_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = normalize_progress(progress)
    path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    return normalized


def reset_progress(base_dir: str | Path | None = None) -> dict[str, list[str]]:
    progress = normalize_progress(None)
    return save_progress(progress, base_dir)


def mark_completed(progress: dict[str, list[str]], level_id: str) -> dict[str, list[str]]:
    progress = normalize_progress(progress)
    if level_id not in progress["completed_levels"]:
        progress["completed_levels"].append(level_id)
    if level_id in progress["locked_levels"]:
        progress["locked_levels"].remove(level_id)
    return progress


def mark_unlocked(progress: dict[str, list[str]], level_id: str) -> dict[str, list[str]]:
    progress = normalize_progress(progress)
    if level_id not in progress["unlocked_levels"]:
        progress["unlocked_levels"].append(level_id)
    if level_id in progress["locked_levels"]:
        progress["locked_levels"].remove(level_id)
    return progress


def mark_locked(progress: dict[str, list[str]], level_id: str) -> dict[str, list[str]]:
    progress = normalize_progress(progress)
    if level_id in progress["completed_levels"]:
        progress["completed_levels"].remove(level_id)
    if level_id in progress["unlocked_levels"]:
        progress["unlocked_levels"].remove(level_id)
    if level_id not in progress["locked_levels"]:
        progress["locked_levels"].append(level_id)
    return progress


def is_unlocked(level_id: str, progress: dict[str, list[str]], previous_level: str | None) -> bool:
    progress = normalize_progress(progress)
    if level_id in progress["locked_levels"]:
        return False
    if level_id in progress["unlocked_levels"]:
        return True
    if previous_level is None:
        return True
    return previous_level in progress["completed_levels"]
