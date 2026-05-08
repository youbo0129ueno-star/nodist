from __future__ import annotations

import json
from pathlib import Path

from app.judge import judge_submission, load_tests
from app.registry import get_levels_dir, load_level_meta


REQUIRED_FILES = [
    "meta.json",
    "task_ja.md",
    "template.c",
    "answer.c",
    "tests.json",
]


def validate_required_files(level_dir: Path) -> list[str]:
    errors = []
    for filename in REQUIRED_FILES:
        path = level_dir / filename
        if not path.exists():
            errors.append(f"missing {filename}")
        elif path.is_file() and path.stat().st_size == 0:
            errors.append(f"empty {filename}")
    return errors


def validate_meta(level_id: str, known_level_ids: set[str]) -> list[str]:
    errors = []
    try:
        meta = load_level_meta(level_id)
    except json.JSONDecodeError as error:
        return [f"invalid meta.json: {error}"]

    if meta is None:
        return ["missing meta.json"]

    if meta.get("id") != level_id:
        errors.append(f"meta id must be {level_id}")

    for field in ("title", "previous_level", "hints"):
        if field not in meta:
            errors.append(f"missing meta field: {field}")

    if "title_ja" not in meta:
        errors.append("missing meta field: title_ja")

    hints = meta.get("hints")
    if not isinstance(hints, list) or not all(isinstance(item, str) for item in hints):
        errors.append("hints must be a list of strings")

    hints_ja = meta.get("hints_ja")
    if hints_ja is not None and (
        not isinstance(hints_ja, list) or not all(isinstance(item, str) for item in hints_ja)
    ):
        errors.append("hints_ja must be a list of strings")

    previous_level = meta.get("previous_level")
    if previous_level is not None and previous_level not in known_level_ids:
        errors.append(f"previous_level not found: {previous_level}")

    return errors


def validate_tests(level_id: str) -> list[str]:
    try:
        load_tests(level_id)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        return [f"invalid tests.json: {error}"]
    return []


def validate_answer(level_id: str, answer_path: Path) -> list[str]:
    result = judge_submission(level_id, answer_path)
    if result.compile_status != "OK":
        output = result.compile_output.splitlines()[0] if result.compile_output else "compile failed"
        return [f"answer.c CE: {output}"]
    if result.passed != result.total:
        failed = [test.name for test in result.tests if test.status != "AC"]
        return [f"answer.c failed tests: {', '.join(failed)}"]
    return []


def validate_all_levels() -> tuple[bool, list[str]]:
    levels_dir = get_levels_dir()
    if not levels_dir.exists():
        return False, [f"levels directory not found: {levels_dir}"]

    level_dirs = sorted(path for path in levels_dir.iterdir() if path.is_dir())
    known_level_ids = {path.name for path in level_dirs}
    messages = []
    ok = True

    for level_dir in level_dirs:
        level_id = level_dir.name
        errors = []
        errors.extend(validate_required_files(level_dir))
        errors.extend(validate_meta(level_id, known_level_ids))
        errors.extend(validate_tests(level_id))

        answer_path = level_dir / "answer.c"
        if answer_path.exists():
            errors.extend(validate_answer(level_id, answer_path))

        if errors:
            ok = False
            messages.append(f"[FAIL] {level_id}")
            messages.extend(f"  - {error}" for error in errors)
        else:
            messages.append(f"[OK] {level_id}")

    if not level_dirs:
        ok = False
        messages.append("[FAIL] no levels found")

    return ok, messages
