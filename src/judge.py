#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.judge import judge_submission, print_judge_result
from app.registry import list_levels


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compile and judge a C submission against JSON test cases."
    )
    parser.add_argument("level_id", help="Level id, such as level_00")
    parser.add_argument("submission_file", type=Path, help="Path to submitted C source file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    level_id = args.level_id

    if args.submission_file.exists() is False:
        print(f"Error: submission file was not found: {args.submission_file}", file=sys.stderr)
        return 2

    known_level_ids = {level["id"] for level in list_levels()}
    if level_id not in known_level_ids:
        print(f"Error: level was not found: {level_id}", file=sys.stderr)
        return 2

    try:
        result = judge_submission(level_id, args.submission_file)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    print_judge_result(level_id, result)
    return 0 if result.passed == result.total else 1


if __name__ == "__main__":
    raise SystemExit(main())
