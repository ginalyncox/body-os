#!/usr/bin/env python3
"""Quick setup: copy config and install dependencies."""

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main() -> int:
    example = ROOT / "config.example.yaml"
    target = ROOT / "config.yaml"
    if not target.exists() and example.exists():
        shutil.copy(example, target)
        print(f"Created {target}")

    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("\nReady. Run:")
    print("  python3 -m brain --simulate")
    print("\nWith speaker (edge TTS):")
    print("  pip install edge-tts")
    print("  python3 -m brain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
