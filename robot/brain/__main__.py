"""Entry point: python -m brain [--simulate] [--sync-server]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import RobotConfig
from .data.store import DataStore
from .router import Router
from .sync_server import run_sync_server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="body-os assistive robot brain")
    parser.add_argument("--simulate", action="store_true", help="Terminal simulation mode")
    parser.add_argument("--sync-server", action="store_true", help="Start companion sync HTTP server")
    parser.add_argument("--config", type=Path, default=None, help="Path to config.yaml")
    args = parser.parse_args(argv)

    config = RobotConfig.load(args.config)
    store = DataStore(config.data_dir)
    sync_srv = None

    if args.sync_server or config.sync_enabled:
        sync_srv = run_sync_server(config, store, config.sync_host, config.sync_port)

    router = Router(config)
    router.greeting()

    print("\n--- body-os robot ---")
    print("Type commands as if speaking to the robot. 'quit' to exit.")
    if sync_srv:
        print(f"Companion sync: http://127.0.0.1:{config.sync_port}/api/sync\n")

    try:
        while True:
            text = router.voice.listen()
            if not router.handle(text):
                break
    except KeyboardInterrupt:
        print("\nInterrupted.")
    finally:
        if hasattr(router.motor, "cleanup"):
            router.motor.cleanup()
        if sync_srv:
            sync_srv.shutdown()

    return 0


if __name__ == "__main__":
    sys.exit(main())
