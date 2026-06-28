"""Entry point: python -m brain [--simulate]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import RobotConfig
from .router import Router


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="body-os assistive robot brain")
    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Terminal simulation mode (default)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to config.yaml",
    )
    args = parser.parse_args(argv)

    config = RobotConfig.load(args.config)
    router = Router(config)
    router.greeting()

    print("\n--- body-os robot simulation ---")
    print("Type commands as if speaking to the robot. 'quit' to exit.\n")

    try:
        while True:
            text = router.voice.listen()
            if not router.handle(text):
                break
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
