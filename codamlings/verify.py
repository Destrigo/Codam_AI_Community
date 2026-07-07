"""Run and verify exercises."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from codamlings.checks import EXACT_OUTPUT, NO_MOCK_SLUGS, OUTPUT_CHECKS
from codamlings.config import apply_mistral_env
from codamlings.exercises import CORE_EXERCISES, Exercise, exercises_for, mark_complete
from codamlings.mock_server import mock_api_base, start_mock_server

MOCK_PORT = 0


def _run_process(cmd: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=60,
    )


def _python_entry(exercise: Exercise) -> Path:
    return exercise.path / "python" / "main.py"


def _cpp_build_dir(exercise: Exercise) -> Path:
    return exercise.path / "cpp" / "build"


def _build_cpp(exercise: Exercise) -> tuple[bool, str]:
    build_dir = _cpp_build_dir(exercise)
    build_dir.mkdir(parents=True, exist_ok=True)
    if not shutil.which("cmake"):
        return False, "cmake not found in PATH"
    env = os.environ.copy()
    env.setdefault("FETCHCONTENT_BASE_DIR", str(Path(__file__).resolve().parent.parent / ".codamlings" / "deps"))
    configure = subprocess.run(
        ["cmake", "..", "-DCMAKE_BUILD_TYPE=Release"],
        cwd=build_dir, capture_output=True, text=True, env=env,
    )
    if configure.returncode != 0:
        return False, configure.stderr or configure.stdout
    build = subprocess.run(
        ["cmake", "--build", ".", "--config", "Release"],
        cwd=build_dir, capture_output=True, text=True, env=env,
    )
    if build.returncode != 0:
        return False, build.stderr or build.stdout
    return True, ""


def _cpp_binary(exercise: Exercise) -> Path | None:
    build_dir = _cpp_build_dir(exercise)
    for path in [
        build_dir / "Release" / "main.exe",
        build_dir / "main.exe",
        build_dir / "main",
        build_dir / "Release" / "main",
    ]:
        if path.exists():
            return path
    return None


def exercise_env(use_mock: bool, mock_base: str | None = None) -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("APP_NAME", "codamlings")
    env.setdefault("MISTRAL_MODEL", "mistral-small-latest")
    if use_mock and mock_base:
        apply_mistral_env(env, mock_base=mock_base)
    return env


def needs_mock(exercise: Exercise) -> bool:
    return exercise.slug not in NO_MOCK_SLUGS


def run_exercise(exercise: Exercise, lang: str, use_mock: bool = False) -> int:
    server = None
    mock_base = None
    try:
        mock_on = use_mock or needs_mock(exercise)
        if mock_on:
            server = start_mock_server(MOCK_PORT)
            mock_base = mock_api_base(server)
        env = exercise_env(mock_on, mock_base)

        if lang == "python":
            entry = _python_entry(exercise)
            if not entry.exists():
                print(f"File not found: {entry}")
                return 1
            return subprocess.run([sys.executable, str(entry)], env=env).returncode

        if lang == "cpp":
            ok, err = _build_cpp(exercise)
            if not ok:
                print(err)
                return 1
            binary = _cpp_binary(exercise)
            if not binary:
                print("C++ executable not found after build.")
                return 1
            return subprocess.run([str(binary)], env=env).returncode

        print(f"Unsupported language: {lang}")
        return 1
    finally:
        if server:
            server.shutdown()


def _check_output(slug: str, stdout: str, stderr: str) -> tuple[bool, str]:
    out = stdout.strip()
    expected = OUTPUT_CHECKS.get(slug, [])
    missing = [item for item in expected if item not in out]
    if missing:
        detail = f"Missing expected output: {missing}\n--- stdout ---\n{out}\n--- stderr ---\n{stderr.strip()}"
        return False, detail
    if slug in EXACT_OUTPUT and out != EXACT_OUTPUT[slug]:
        return False, f"Expected exact output {EXACT_OUTPUT[slug]!r}, got {out!r}"
    return True, "OK"


def verify_exercise(exercise: Exercise, lang: str) -> bool:
    mock_on = needs_mock(exercise)
    server = None
    mock_base = None
    if mock_on:
        server = start_mock_server(MOCK_PORT)
        mock_base = mock_api_base(server)
    env = exercise_env(mock_on, mock_base)

    try:
        if lang == "python":
            entry = _python_entry(exercise)
            proc = _run_process([sys.executable, str(entry)], entry.parent, env)
        else:
            ok, err = _build_cpp(exercise)
            if not ok:
                print(f"FAIL {exercise.slug} [{lang}] build failed:\n{err}")
                return False
            binary = _cpp_binary(exercise)
            if not binary:
                print(f"FAIL {exercise.slug} [{lang}] executable not found")
                return False
            proc = _run_process([str(binary)], binary.parent, env)

        if proc.returncode != 0:
            print(f"FAIL {exercise.slug} [{lang}] exit code {proc.returncode}")
            print(proc.stdout)
            print(proc.stderr)
            return False

        ok, msg = _check_output(exercise.slug, proc.stdout, proc.stderr)
        if ok:
            mark_complete(exercise.slug, lang)
            print(f"PASS {exercise.slug} [{lang}]")
            return True
        print(f"FAIL {exercise.slug} [{lang}] — {msg}")
        return False
    finally:
        if server:
            server.shutdown()


def verify_all(lang: str, module: str | None = None) -> int:
    pool = exercises_for(module if module else "core")
    if module == "all":
        pool = exercises_for("all")
    passed = sum(1 for ex in pool if verify_exercise(ex, lang))
    total = len(pool)
    label = module or "core"
    print(f"\nResult: {passed}/{total} exercises passed ({label}, {lang})")
    return 0 if passed == total else 1
