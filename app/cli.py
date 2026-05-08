from __future__ import annotations

import sys
from pathlib import Path

from app.config import load_config, set_language
from app.judge import judge_submission, print_judge_result
from app.progress import (
    is_unlocked,
    load_progress,
    mark_completed,
    mark_locked,
    mark_unlocked,
    reset_progress,
    save_progress,
)
from app.registry import (
    get_level,
    get_level_answer,
    get_level_explanation,
    get_level_hints,
    get_level_task,
    get_level_template,
    get_previous_level,
    list_levels,
)
from app.validate import validate_all_levels


def show_usage() -> None:
    print("Usage:")
    print("nodist list")
    print("nodist lang [ja|en]")
    print("nodist level <level_id>")
    print("nodist hint <level_id>")
    print("nodist answer <level_id>")
    print("nodist explain <level_id>")
    print("nodist submit <level_id> [answer.c]")


def ensure_level_access(level_id: str) -> str | None:
    level = get_level(level_id)
    if level is None:
        return f"Level not found: {level_id}"

    progress = load_progress()
    previous_level = get_previous_level(level_id)
    if not is_unlocked(level_id, progress, previous_level):
        if previous_level is None:
            return f"Level is locked: {level_id}"
        return f"Level is locked: {level_id} (clear {previous_level} first)"
    return None


def get_working_answer_path() -> Path:
    return Path("answer.c")


def update_answer_file(level_id: str) -> Path:
    path = get_working_answer_path()
    template = get_level_template(level_id)
    if template is None:
        template = "int main(void) {\n    return 0;\n}\n"
    path.write_text(template, encoding="utf-8")
    return path


def show_list() -> None:
    progress = load_progress()
    for level in list_levels():
        previous_level = get_previous_level(level["id"])
        if level["id"] in progress["completed_levels"]:
            status = "COMPLETED"
        elif is_unlocked(level["id"], progress, previous_level):
            status = "UNLOCKED"
        else:
            status = "LOCKED"
        print(f"[{status}] {level['id']}: {level['title']}")


def show_language() -> None:
    print(load_config()["language"])


def show_set_language(language: str) -> None:
    if language not in {"ja", "en"}:
        print(f"Unsupported language: {language}")
        return
    config = set_language(language)
    print(f"Language set to {config['language']}")


def show_level(level_id: str) -> None:
    message = ensure_level_access(level_id)
    if message is not None:
        print(message)
        return

    level = get_level(level_id)
    if level is None:
        print(f"Level not found: {level_id}")
        return

    print(f"{level['id']}: {level['title']}")
    task = get_level_task(level_id)
    if task is not None:
        print()
        print(task)

    answer_path = update_answer_file(level_id)
    print()
    print(f"Updated {answer_path}")


def show_hints(level_id: str) -> None:
    message = ensure_level_access(level_id)
    if message is not None:
        print(message)
        return
    for hint in get_level_hints(level_id):
        print(f"- {hint}")


def show_answer(level_id: str) -> None:
    message = ensure_level_access(level_id)
    if message is not None:
        print(message)
        return
    answer = get_level_answer(level_id)
    if answer is None:
        print(f"Answer not found for level: {level_id}")
        return
    print(answer)


def show_explanation(level_id: str) -> None:
    message = ensure_level_access(level_id)
    if message is not None:
        print(message)
        return
    explanation = get_level_explanation(level_id)
    if explanation is None:
        print(f"Explanation not found for level: {level_id}")
        return
    print(explanation)


def show_submit(level_id: str, answer_path_text: str = "answer.c") -> int:
    message = ensure_level_access(level_id)
    if message is not None:
        print(message)
        return 1

    answer_path = Path(answer_path_text)
    if not answer_path.exists():
        print(f"Answer file not found: {answer_path_text}")
        return 1
    if answer_path.suffix != ".c":
        print(f"Answer file must be a .c file: {answer_path_text}")
        return 1

    result = judge_submission(level_id, answer_path)
    print_judge_result(level_id, result)
    if result.passed != result.total:
        return 1

    progress = mark_completed(load_progress(), level_id)
    save_progress(progress)
    print(f"Accepted {answer_path}")
    return 0


def show_reset_progress() -> None:
    reset_progress()
    print("Progress reset")


def show_unlock_level(level_id: str) -> None:
    if get_level(level_id) is None:
        print(f"Level not found: {level_id}")
        return
    progress = mark_unlocked(load_progress(), level_id)
    save_progress(progress)
    print(f"Unlocked {level_id}")


def show_lock_level(level_id: str) -> None:
    if get_level(level_id) is None:
        print(f"Level not found: {level_id}")
        return
    progress = mark_locked(load_progress(), level_id)
    save_progress(progress)
    print(f"Locked {level_id}")


def show_validate_levels() -> int:
    ok, messages = validate_all_levels()
    for message in messages:
        print(message)
    if ok:
        print("Validation passed")
        return 0
    print("Validation failed")
    return 1


def main() -> int:
    args = sys.argv[1:]

    if args == ["list"]:
        show_list()
    elif args == ["lang"]:
        show_language()
    elif len(args) == 2 and args[0] == "lang":
        show_set_language(args[1])
    elif len(args) == 2 and args[0] == "level":
        show_level(args[1])
    elif len(args) == 2 and args[0] == "hint":
        show_hints(args[1])
    elif len(args) == 2 and args[0] == "answer":
        show_answer(args[1])
    elif len(args) == 2 and args[0] == "explain":
        show_explanation(args[1])
    elif len(args) == 2 and args[0] == "submit":
        return show_submit(args[1])
    elif len(args) == 3 and args[0] == "submit":
        return show_submit(args[1], args[2])
    elif args == ["__reset_progress"]:
        show_reset_progress()
    elif len(args) == 2 and args[0] == "__unlock_level":
        show_unlock_level(args[1])
    elif len(args) == 2 and args[0] == "__lock_level":
        show_lock_level(args[1])
    elif args == ["__validate_levels"]:
        return show_validate_levels()
    else:
        show_usage()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
