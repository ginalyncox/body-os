"""Entry point: python -m brain [--simulate] [--autonomy]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .autonomy.care_loop import build_care_loop
from .config import RobotConfig
from .data.store import DataStore
from .router import Router
from .sync_server import run_sync_server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="body-os assistive robot brain")
    parser.add_argument("--simulate", action="store_true", help="Terminal simulation mode")
    parser.add_argument("--sync-server", action="store_true", help="Start companion sync HTTP server")
    parser.add_argument("--autonomy", action="store_true", help="Run mutual-care autonomy loop")
    parser.add_argument("--config", type=Path, default=None, help="Path to config.yaml")
    args = parser.parse_args(argv)

    config = RobotConfig.load(args.config)
    store = DataStore(config.data_dir)
    sync_srv = None
    care_loop = None

    if args.sync_server or config.sync_enabled:
        sync_srv = run_sync_server(config, store, config.sync_host, config.sync_port)

    router = Router(config)

    if args.autonomy or config.autonomy_enabled:
        care_loop = build_care_loop(router)
        care_loop.start()

    router.greeting()

    print("\n--- body-os robot ---")
    print("Type commands as if speaking to the robot. 'quit' to exit.")
    if sync_srv:
        print(f"Companion sync: http://127.0.0.1:{config.sync_port}/api/sync")
    if care_loop:
        print("Autonomy: mutual care loop active (battery + vitals)")
    print()

    try:
        while True:
            text = router.voice.listen()
            if not router.handle(text):
                break
    except KeyboardInterrupt:
        print("\nInterrupted.")
    finally:
        if care_loop:
            care_loop.stop()
        if hasattr(router.motor, "cleanup"):
            router.motor.cleanup()
        if sync_srv:
            sync_srv.shutdown()

    return 0


if __name__ == "__main__":
    sys.exit(main())
