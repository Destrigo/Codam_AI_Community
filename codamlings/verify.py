"""Run and verify exercises."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from codamlings.checks import check_output, requires_mistral
from codamlings.config import apply_mistral_env, require_mistral_key
from codamlings.exercises import Exercise, exercises_for, mark_complete
from codamlings.mock_server import mock_api_base, start_mock_server

MOCK_PORT = 0


def _run_process(cmd: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=120)


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
        echo_root = mock_base.rsplit("/v1", 1)[0]
        env["CODAMLINGS_ECHO_URL"] = f"{echo_root}/echo"
    else:
        apply_mistral_env(env, mock_base=None)
        env.setdefault("CODAMLINGS_ECHO_URL", "https://httpbin.org/post")
    return env


def _prepare_env(exercise: Exercise, use_mock: bool) -> tuple[dict[str, str], object | None]:
    if use_mock:
        server = start_mock_server(MOCK_PORT)
        env = exercise_env(True, mock_api_base(server))
        return env, server
    if requires_mistral(exercise.slug):
        require_mistral_key()
    return exercise_env(False), None


def run_exercise(exercise: Exercise, lang: str, use_mock: bool = False) -> int:
    env, server = _prepare_env(exercise, use_mock)
    try:
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


def verify_exercise(exercise: Exercise, lang: str, use_mock: bool = False) -> bool:
    env, server = _prepare_env(exercise, use_mock)
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

        ok, msg = check_output(exercise.slug, proc.stdout, proc.stderr, use_mock=use_mock)
        if ok:
            mark_complete(exercise.slug, lang, via="verify")
            mode = "mock" if use_mock else "live"
            print(f"PASS {exercise.slug} [{lang}] ({mode})")
            return True
        print(f"FAIL {exercise.slug} [{lang}] — {msg}")
        return False
    finally:
        if server:
            server.shutdown()


def verify_all(lang: str, module: str | None = None, use_mock: bool = False) -> int:
    pool = exercises_for("all") if module == "all" else exercises_for(module if module else "core")
    passed = sum(1 for ex in pool if verify_exercise(ex, lang, use_mock=use_mock))
    total = len(pool)
    label = module or "core"
    mode = "mock" if use_mock else "live"
    print(f"\nResult: {passed}/{total} exercises passed ({label}, {lang}, {mode})")
    return 0 if passed == total else 1
