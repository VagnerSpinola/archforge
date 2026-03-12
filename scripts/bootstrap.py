from __future__ import annotations

import subprocess
import sys


def main() -> int:
    command = [sys.executable, "-m", "pip", "install", "-e", ".[dev]"]
    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())