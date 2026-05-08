from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from app.registry import get_level_tests_path


TIME_LIMIT_SECONDS = 2.0
COMPILE_FLAGS = ["-std=c11", "-Wall", "-Wextra"]


@dataclass(frozen=True)
class TestCase:
    name: str
    input: str
    expected: str


@dataclass(frozen=True)
class TestResult:
    name: str
    status: str
    elapsed: float
    expected: str = ""
    actual: str = ""
    message: str = ""


@dataclass(frozen=True)
class JudgeResult:
    compile_status: str
    compiler: str | None
    passed: int
    total: int
    tests: list[TestResult]
    compile_output: str = ""


def find_compiler() -> str | None:
    for compiler in ("gcc", "clang"):
        path = shutil.which(compiler)
        if path:
            return path
    return None


def load_tests(level_id: str) -> list[TestCase]:
    tests_path = get_level_tests_path(level_id)
    if tests_path is None:
        raise FileNotFoundError(f"tests.json was not found for level: {level_id}")

    raw_tests = json.loads(tests_path.read_text(encoding="utf-8"))
    if not isinstance(raw_tests, list) or not raw_tests:
        raise ValueError("tests.json must be a non-empty JSON array.")

    tests = []
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


def run_test(executable: Path, test: TestCase) -> TestResult:
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
        return TestResult(test.name, "TLE", TIME_LIMIT_SECONDS)

    elapsed = time.perf_counter() - started_at
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        message = stderr if stderr else f"Process exited with code {completed.returncode}."
        return TestResult(test.name, "RE", elapsed, message=message)

    if completed.stdout == test.expected:
        return TestResult(test.name, "AC", elapsed, expected=test.expected, actual=completed.stdout)
    return TestResult(test.name, "WA", elapsed, expected=test.expected, actual=completed.stdout)


def judge_submission(level_id: str, submission_file: Path) -> JudgeResult:
    tests = load_tests(level_id)
    compiler = find_compiler()
    if compiler is None:
        return JudgeResult("CE", None, 0, len(tests), [], "gcc or clang was not found.")

    with tempfile.TemporaryDirectory(prefix="nodist-") as temp_dir:
        executable = Path(temp_dir) / "submission.out"
        ok, compile_output = compile_submission(compiler, submission_file, executable)
        if not ok:
            return JudgeResult("CE", Path(compiler).name, 0, len(tests), [], compile_output)

        results = [run_test(executable, test) for test in tests]

    passed = sum(1 for result in results if result.status == "AC")
    return JudgeResult("OK", Path(compiler).name, passed, len(tests), results)


def indent_block(text: str) -> str:
    return "\n".join(f"    {line}" for line in text.splitlines())


def print_judge_result(level_id: str, result: JudgeResult) -> None:
    print(f"=== {level_id} ===")
    if result.compiler is not None:
        print(f"Compiler: {result.compiler}")

    if result.compile_status != "OK":
        print("Compile: CE")
        if result.compile_output:
            print(indent_block(result.compile_output))
        print(f"\nResult: 0/{result.total} passed")
        return

    print("Compile: OK")
    for test in result.tests:
        if test.status == "AC":
            print(f"Test {test.name}: AC ({test.elapsed:.3f}s)")
        elif test.status == "WA":
            print(f"Test {test.name}: WA ({test.elapsed:.3f}s)")
            print("  Expected:")
            print(indent_block(repr(test.expected)))
            print("  Actual:")
            print(indent_block(repr(test.actual)))
        elif test.status == "RE":
            print(f"Test {test.name}: RE")
            if test.message:
                print(indent_block(test.message))
        else:
            print(f"Test {test.name}: TLE (>{TIME_LIMIT_SECONDS:.1f}s)")

    print(f"\nResult: {result.passed}/{result.total} passed")
