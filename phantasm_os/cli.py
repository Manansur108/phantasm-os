"""
Phantasm-OS Command Line Interface.
Runs the retro web server, inspects VFS structures, or plays the ARG.
"""

from __future__ import annotations

import argparse
import sys
import uvicorn

from phantasm_os.core.arg_engine import ARGEngine
from phantasm_os.core.clippy import ExistentialClippy
from phantasm_os.core.vfs import VirtualFileSystem


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="phantasm-os",
        description="Phantasm-OS: Generative 1995 Desktop Simulation & Hallucinated Cyber-World"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Run the Phantasm-OS 95 web server")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000)")
    serve_parser.add_argument("--reload", action="store_true", help="Enable live reloads")

    # VFS list command
    vfs_parser = subparsers.add_parser("vfs-list", help="List files in Virtual Filesystem")
    vfs_parser.add_argument("--dir", default="C:\\", help="Directory path to inspect (default: C:\\)")

    # ARG status command
    subparsers.add_parser("arg-status", help="Inspect ARG puzzle stages and status")

    # Clippy chat command
    clippy_parser = subparsers.add_parser("clippy", help="Interact with the existential paperclip")
    clippy_parser.add_argument("query", nargs="?", default="Hello Clippy!", help="Query or question for Clippy")

    args = parser.parse_args()

    if args.command == "serve" or args.command is None:
        host = getattr(args, "host", "127.0.0.1")
        port = getattr(args, "port", 8000)
        reload_flag = getattr(args, "reload", False)
        print(f"[*] Booting Phantasm-OS 95 Desktop Server at http://{host}:{port}")
        uvicorn.run("phantasm_os.app:app", host=host, port=port, reload=reload_flag)

    elif args.command == "vfs-list":
        vfs = VirtualFileSystem(seed_defaults=True)
        nodes = vfs.list_dir(args.dir)
        print(f"\nDirectory listing for {args.dir}:")
        print("-" * 60)
        for node in nodes:
            kind = "<DIR> " if node.is_dir else f"{node.size:6d}B"
            corrupt_flag = " [CORRUPT]" if node.corrupted else ""
            print(f"{node.name:<25} {kind} {node.modified_at}{corrupt_flag}")
        print("-" * 60)

    elif args.command == "arg-status":
        arg = ARGEngine()
        status = arg.get_status()
        print("\n=== PROJECT CHIMERA ARG STATUS ===")
        print(f"Stage: {status.stage_title}")
        print(f"Completed: {status.is_completed}")
        print("Clues Discovered:")
        for clue in status.clues_found:
            print(f" - {clue}")

    elif args.command == "clippy":
        clippy = ExistentialClippy()
        response = clippy.interact(query=args.query)
        print(f"\n[CLIPTRON 95] ({response.mood.value.upper()}): {response.text}")
        if response.arg_hint:
            print(f"[ARG HINT]: {response.arg_hint}")


if __name__ == "__main__":
    main()
