#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path


TIME_LIMIT_SECONDS = 2.0
COMPILE_FLAGS = ["-std=c11", "-Wall", "-Wextra"]


@dataclass(frozen=True)
class TestCase:
    name: str
    input: str
    expected: str


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def find_compiler() -> str | None:
    for compiler in ("gcc", "clang"):
        path = shutil.which(compiler)
        if path:
            return path
    return None


def load_tests(problem_id: str) -> list[TestCase]:
    tests_path = project_root() / "problems" / problem_id / "tests.json"
    if not tests_path.exists():
        raise FileNotFoundError(
            f"Problem '{problem_id}' was not found. Expected: {tests_path}"
        )

    try:
        raw_tests = json.loads(tests_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"tests.json is not valid JSON: {error}") from error

    if not isinstance(raw_tests, list) or not raw_tests:
        raise ValueError("tests.json must be a non-empty JSON array.")

    tests: list[TestCase] = []
    for index, item in enumerate(raw_tests, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Test case #{index} must be an object.")
        for key in ("name", "input", "expected"):
            if key not in item or not isinstance(item[key], str):
                raise ValueError(f"Test case #{index} needs a string field '{key}'.")
        tests.append(TestCase(item["name"], item["input"], item["expected"]))
    return tests


def compile_submission(compiler: str, submission: Path, executable: Path) -> tuple[bool, str]:
    command = [compiler, *COMPILE_FLAGS, str(submission), "-o", str(executable)]
    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=TIME_LIMIT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, "Compilation timed out."

    output = (completed.stdout + completed.stderr).strip()
    return completed.returncode == 0, output


def run_test(executable: Path, test: TestCase) -> tuple[str, str, float]:
    started_at = time.perf_counter()
    try:
        completed = subprocess.run(
            [str(executable)],
            input=test.input,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=TIME_LIMIT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "TLE", "", TIME_LIMIT_SECONDS

    elapsed = time.perf_counter() - started_at
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        message = stderr if stderr else f"Process exited with code {completed.returncode}."
        return "RE", message, elapsed

    if completed.stdout == test.expected:
        return "AC", completed.stdout, elapsed
    return "WA", completed.stdout, elapsed


def print_wrong_answer_detail(expected: str, actual: str) -> None:
    print("  Expected:")
    print(indent_block(repr(expected)))
    print("  Actual:")
    print(indent_block(repr(actual)))


def indent_block(text: str) -> str:
    return "\n".join(f"    {line}" for line in text.splitlines())


def judge(problem_id: str, submission_file: Path) -> int:
    if not submission_file.exists():
        print(f"Error: submission file was not found: {submission_file}", file=sys.stderr)
        return 2

    compiler = find_compiler()
    if compiler is None:
        print("Error: gcc or clang was not found. Please install one compiler.", file=sys.stderr)
        return 2

    try:
        tests = load_tests(problem_id)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    print(f"=== {problem_id} ===")
    print(f"Compiler: {Path(compiler).name}")

    with tempfile.TemporaryDirectory(prefix="algo-trainer-") as temp_dir:
        executable = Path(temp_dir) / "submission.out"
        ok, compile_output = compile_submission(compiler, submission_file, executable)
        if not ok:
            print("Compile: CE")
            if compile_output:
                print(indent_block(compile_output))
            print(f"\nResult: 0/{len(tests)} passed")
            return 1

        print("Compile: OK")
        passed = 0
        for test in tests:
            status, output, elapsed = run_test(executable, test)
            if status == "AC":
                passed += 1
                print(f"Test {test.name}: AC ({elapsed:.3f}s)")
            elif status == "WA":
                print(f"Test {test.name}: WA ({elapsed:.3f}s)")
                print_wrong_answer_detail(test.expected, output)
            elif status == "RE":
                print(f"Test {test.name}: RE")
                if output:
                    print(indent_block(output))
            else:
                print(f"Test {test.name}: TLE (>{TIME_LIMIT_SECONDS:.1f}s)")

    print(f"\nResult: {passed}/{len(tests)} passed")
    return 0 if passed == len(tests) else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compile and judge a C submission against JSON test cases."
    )
    parser.add_argument("problem_id", help="Problem directory name under problems/")
    parser.add_argument("submission_file", type=Path, help="Path to submitted C source file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return judge(args.problem_id, args.submission_file)


if __name__ == "__main__":
    raise SystemExit(main())
