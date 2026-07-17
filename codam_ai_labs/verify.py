"""Run and verify exercises."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from codam_ai_labs.checks import check_output, requires_mistral
from codam_ai_labs.config import apply_mistral_env, require_mistral_key
from codam_ai_labs.exercises import Exercise, exercises_for, mark_complete
from codam_ai_labs.mock_server import mock_api_base, start_mock_server

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
    env.setdefault("FETCHCONTENT_BASE_DIR", str(Path(__file__).resolve().parent.parent / ".codam-ai-labs" / "deps"))
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
    env.setdefault("APP_NAME", "codam-ai-labs")
    env.setdefault("MISTRAL_MODEL", "mistral-small-latest")
    if use_mock and mock_base:
        apply_mistral_env(env, mock_base=mock_base)
        echo_root = mock_base.rsplit("/v1", 1)[0]
        env["CODAM_LABS_ECHO_URL"] = f"{echo_root}/echo"
        env["CODAM_LABS_TODO_URL"] = f"{echo_root}/todos/1"
        env["CODAM_LABS_MCP_BASE"] = f"{echo_root}/mcp"
        env["CODAM_LABS_OLLAMA_BASE"] = echo_root
        env.setdefault("OLLAMA_MODEL", "llama3.2")
    else:
        apply_mistral_env(env, mock_base=None)
        env.setdefault("CODAM_LABS_ECHO_URL", "https://httpbin.org/post")
        env.setdefault(
            "CODAM_LABS_TODO_URL",
            "https://jsonplaceholder.typicode.com/todos/1",
        )
        env.setdefault("CODAM_LABS_OLLAMA_BASE", "http://localhost:11434")
        env.setdefault("OLLAMA_MODEL", "llama3.2")
    return env


def _prepare_env(exercise: Exercise, use_mock: bool) -> tuple[dict[str, str], object | None]:
    if use_mock:
        server = start_mock_server(MOCK_PORT)
        env = exercise_env(True, mock_api_base(server))
        return env, server
    if requires_mistral(exercise.slug):
        require_mistral_key()
    return exercise_env(False), None


def run_exercise(exercise: Exercise, lang: str, use_mock: bool = False, *, capture: bool = False) -> int | tuple[int, str, str]:
    env, server = _prepare_env(exercise, use_mock)
    try:
        if lang == "python":
            entry = _python_entry(exercise)
            if not entry.exists():
                message = f"File not found: {entry}"
                if capture:
                    return 1, "", message
                print(message)
                return 1
            if capture:
                proc = _run_process([sys.executable, str(entry)], entry.parent, env)
                return proc.returncode, proc.stdout or "", proc.stderr or ""
            return subprocess.run([sys.executable, str(entry)], env=env).returncode
        if lang == "cpp":
            ok, err = _build_cpp(exercise)
            if not ok:
                if capture:
                    return 1, "", err
                print(err)
                return 1
            binary = _cpp_binary(exercise)
            if not binary:
                message = "C++ executable not found after build."
                if capture:
                    return 1, "", message
                print(message)
                return 1
            if capture:
                proc = _run_process([str(binary)], binary.parent, env)
                return proc.returncode, proc.stdout or "", proc.stderr or ""
            return subprocess.run([str(binary)], env=env).returncode
        message = f"Unsupported language: {lang}"
        if capture:
            return 1, "", message
        print(message)
        return 1
    finally:
        if server:
            server.shutdown()


def format_run_summary(
    exercise: Exercise,
    *,
    returncode: int,
    stdout: str,
    stderr: str,
    use_mock: bool,
) -> list[str]:
    """Human-readable run report (does not mark exercises complete)."""
    lines: list[str] = []
    out = stdout or ""
    err = stderr or ""
    out_stripped = out.strip()
    err_stripped = err.strip()

    if returncode != 0:
        lines.append(f"$ run [crashed - exit {returncode}]")
        if err_stripped:
            lines.append("stderr:")
            lines.extend(err_stripped.splitlines()[:12])
        elif out_stripped:
            lines.append("stdout:")
            lines.extend(out_stripped.splitlines()[:12])
        lines.append("fix the error, then press v to verify")
        return lines

    if not out_stripped and not err_stripped:
        lines.append("$ run [exit 0 - ran successfully but printed nothing]")
        lines.append("(stub with only `pass` does this — your code is not finished yet)")
    elif not out_stripped and err_stripped:
        lines.append("$ run [exit 0 - stderr only, no stdout]")
    else:
        nlines = len(out_stripped.splitlines())
        lines.append(f"$ run [exit 0 - {nlines} stdout line(s)]")

    rubric_ok, rubric_msg = check_output(exercise.slug, out, err, use_mock=use_mock)
    if rubric_ok:
        lines.append("rubric preview: output matches - press v to confirm PASS")
    else:
        headline = rubric_msg.split("\n", 1)[0]
        lines.append(f"rubric preview: not passing yet - {headline}")
        lines.append("press v for full verify details")

    return lines


def verify_exercise(
    exercise: Exercise, lang: str, use_mock: bool = False, *, record_progress: bool = True
) -> bool:
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
            if exercise.slug == "03_http_post" and (
                "503" in (proc.stderr or "") or "503" in (proc.stdout or "")
            ):
                print(
                    "hint: httpbin.org often returns 503. "
                    "Use `codam-labs --mock verify 03_http_post` and read CODAM_LABS_ECHO_URL."
                )
            return False

        ok, msg = check_output(exercise.slug, proc.stdout, proc.stderr, use_mock=use_mock)
        if ok:
            if record_progress:
                mark_complete(exercise.slug, lang, via="verify")
            mode = "mock" if use_mock else "live"
            print(f"PASS {exercise.slug} [{lang}] ({mode})")
            return True
        print(f"FAIL {exercise.slug} [{lang}] — {msg}")
        if exercise.slug == "03_http_post" and not use_mock:
            print(
                "hint: prefer `codam-labs --mock verify 03_http_post` "
                "(local echo). Use response['json']['name'], not ['data']."
            )
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
