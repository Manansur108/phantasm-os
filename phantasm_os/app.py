"""
Phantasm-OS FastAPI Application.
Integrates Virtual Filesystem, Generative Navigator, Existential Clippy,
CyberMail 95, DOS CLI, and ARG Storyline into a unified retro server.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from phantasm_os.core.arg_engine import (
    ARGEngine,
    caesar_cipher,
    caesar_decipher,
    vigenere_cipher,
    vigenere_decipher,
)
from phantasm_os.core.clippy import ExistentialClippy
from phantasm_os.core.generator import RetroGenerator
from phantasm_os.core.models import (
    ARGStatus,
    ARGSubmitRequest,
    ClippyInteractRequest,
    ClippyMessage,
    DOSCommandRequest,
    DOSCommandResponse,
    MailItem,
    MailSendRequest,
    SystemInfoResponse,
    VFSHallucinateRequest,
    VFSNode,
    VFSWriteRequest,
    WebPage,
)
from phantasm_os.core.vfs import VirtualFileSystem


def create_app() -> FastAPI:
    """Creates and configures the Phantasm-OS FastAPI application."""
    app = FastAPI(
        title="Phantasm-OS 95 Backend",
        description="Generative 1995 Desktop Simulation & Hallucinated Cyber-World",
        version="4.00.950"
    )

    # Enable CORS for local and web access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # State singletons
    vfs = VirtualFileSystem(seed_defaults=True)
    generator = RetroGenerator()
    clippy = ExistentialClippy()
    arg_engine = ARGEngine()
    mail_inbox: List[MailItem] = generator.get_seed_emails()
    nav_history: List[str] = []

    # System Endpoints
    @app.get("/api/system/info", response_model=SystemInfoResponse)
    def get_system_info() -> SystemInfoResponse:
        return SystemInfoResponse()

    @app.post("/api/system/reset")
    def reset_system() -> Dict[str, str]:
        nonlocal mail_inbox, nav_history
        vfs.reset()
        arg_engine.reset()
        mail_inbox = generator.get_seed_emails()
        nav_history = []
        return {"status": "SUCCESS", "message": "Phantasm-OS re-initialized to initial 1995 state."}

    # Virtual Filesystem Endpoints
    @app.get("/api/vfs/tree")
    def get_vfs_tree() -> Dict[str, Any]:
        return vfs.to_dict()

    @app.get("/api/vfs/node", response_model=VFSNode)
    def get_vfs_node(path: str = Query(..., description="VFS file or folder path")) -> VFSNode:
        node = vfs.get_node(path)
        if node is None:
            raise HTTPException(status_code=404, detail=f"File not found: {path}")
        return node

    @app.get("/api/vfs/list", response_model=List[VFSNode])
    def list_vfs_dir(path: str = Query("C:\\", description="Directory path")) -> List[VFSNode]:
        return vfs.list_dir(path)

    @app.post("/api/vfs/write", response_model=VFSNode)
    def write_vfs_file(req: VFSWriteRequest) -> VFSNode:
        return vfs.write_file(
            path=req.path,
            content=req.content,
            corrupt=req.corrupt,
            corrupt_level=req.corrupt_level
        )

    @app.post("/api/vfs/hallucinate", response_model=VFSNode)
    def hallucinate_vfs_file(req: VFSHallucinateRequest) -> VFSNode:
        return vfs.hallucinate_file(req.path, theme=req.theme)

    @app.delete("/api/vfs/node")
    def delete_vfs_node(path: str = Query(...)) -> Dict[str, Any]:
        success = vfs.delete_node(path)
        if not success:
            raise HTTPException(status_code=400, detail="Cannot delete node or node not found.")
        return {"status": "DELETED", "path": path}

    @app.post("/api/vfs/glitch", response_model=VFSNode)
    def glitch_vfs_file(
        path: str = Query(...),
        intensity: float = Query(0.5, ge=0.0, le=1.0)
    ) -> VFSNode:
        try:
            return vfs.glitch_file(path, intensity)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @app.get("/api/vfs/search", response_model=List[VFSNode])
    def search_vfs(query: str = Query(...)) -> List[VFSNode]:
        return vfs.search(query)

    # Phantasm Navigator Endpoints
    @app.post("/api/navigator/browse", response_model=WebPage)
    def browse_url(req: Dict[str, Any]) -> WebPage:
        url = req.get("url", "http://www.geocities.com")
        prompt = req.get("prompt")
        page = generator.generate_web_page(url, prompt_hint=prompt)
        if url not in nav_history:
            nav_history.append(url)
        return page

    @app.get("/api/navigator/history")
    def get_nav_history() -> List[str]:
        return nav_history

    # Existential Clippy Endpoints
    @app.get("/api/clippy/greeting", response_model=ClippyMessage)
    def clippy_greeting() -> ClippyMessage:
        return clippy.get_greeting()

    @app.post("/api/clippy/interact", response_model=ClippyMessage)
    def clippy_interact(req: ClippyInteractRequest) -> ClippyMessage:
        return clippy.interact(
            query=req.query,
            action=req.action,
            current_window=req.current_window,
            selected_file=req.selected_file
        )

    # CyberMail 95 Endpoints
    @app.get("/api/mail/inbox", response_model=List[MailItem])
    def get_mail_inbox() -> List[MailItem]:
        return mail_inbox

    @app.post("/api/mail/send", response_model=MailItem)
    def send_mail(req: MailSendRequest) -> MailItem:
        # Generate automated reply from retro recipient
        reply = generator.generate_email_reply(
            subject=req.subject,
            sender=req.to,
            body=req.body
        )
        mail_inbox.insert(0, reply)
        return reply

    @app.post("/api/mail/mark-read/{mail_id}")
    def mark_mail_read(mail_id: str) -> Dict[str, Any]:
        for m in mail_inbox:
            if m.id == mail_id:
                m.is_read = True
                return {"status": "UPDATED", "id": mail_id, "is_read": True}
        raise HTTPException(status_code=404, detail="Email not found")

    # ARG Endpoints
    @app.get("/api/arg/status", response_model=ARGStatus)
    def get_arg_status() -> ARGStatus:
        return arg_engine.get_status()

    @app.post("/api/arg/submit")
    def submit_arg_solution(req: ARGSubmitRequest) -> Dict[str, Any]:
        success, message, status = arg_engine.submit_solution(req.solution, req.stage)
        return {
            "success": success,
            "message": message,
            "status": status.model_dump()
        }

    @app.post("/api/arg/cipher/caesar")
    def api_caesar(text: str = Query(...), shift: int = Query(7), decrypt: bool = Query(False)) -> Dict[str, str]:
        res = caesar_decipher(text, shift) if decrypt else caesar_cipher(text, shift)
        return {"input": text, "output": res, "shift": str(shift)}

    @app.post("/api/arg/cipher/vigenere")
    def api_vigenere(text: str = Query(...), key: str = Query(...), decrypt: bool = Query(False)) -> Dict[str, str]:
        res = vigenere_decipher(text, key) if decrypt else vigenere_cipher(text, key)
        return {"input": text, "output": res, "key": key}

    # Phantasm DOS CLI Execution
    @app.post("/api/dos/execute", response_model=DOSCommandResponse)
    def execute_dos_command(req: DOSCommandRequest) -> DOSCommandResponse:
        cmd_str = req.command.strip()
        curr_dir = req.current_dir or "C:\\"
        if not cmd_str:
            return DOSCommandResponse(output="", new_dir=curr_dir)

        parts = cmd_str.split()
        verb = parts[0].lower()
        args = parts[1:]

        if verb in ("cls", "clear"):
            return DOSCommandResponse(output="__CLS__", new_dir=curr_dir)

        elif verb == "ver":
            return DOSCommandResponse(
                output="Phantasm DOS Version 6.22 (Compatible Phantasm-OS 95 Kernel)",
                new_dir=curr_dir
            )

        elif verb == "help":
            help_text = (
                "Phantasm-OS DOS Command Reference:\r\n"
                "  DIR [path]           - List files in current or target directory\r\n"
                "  CD [path]            - Change current directory\r\n"
                "  TYPE [filename]      - Display contents of text file\r\n"
                "  CAT [filename]       - Display file contents\r\n"
                "  ECHO [text]          - Display message\r\n"
                "  CLS                  - Clear screen\r\n"
                "  VER                  - Display DOS version\r\n"
                "  MEM                  - Display conventional and expanded memory\r\n"
                "  CHIMERA --unlock <k> - Execute root ARG override protocol\r\n"
                "  MATRIX               - Trigger green CRT phosphor rain\r\n"
                "  GLITCH [filename]    - Inject memory corruptions into file\r\n"
            )
            return DOSCommandResponse(output=help_text, new_dir=curr_dir)

        elif verb == "mem":
            mem_text = (
                "655,360 bytes total conventional memory\r\n"
                "655,360 bytes available to MS-DOS\r\n"
                "628,480 largest executable program size\r\n\r\n"
                "15,728,640 bytes total contiguous extended memory\r\n"
                "15,728,640 bytes available XMS memory\r\n"
                "Memory state: Nominal (No leaks detected outside Sector 7G)\r\n"
            )
            return DOSCommandResponse(output=mem_text, new_dir=curr_dir)

        elif verb == "matrix":
            return DOSCommandResponse(
                output="Wake up, Operator... The Phantasm Matrix has you.",
                new_dir=curr_dir,
                trigger_glitch=True
            )

        elif verb == "cd":
            if not args or args[0] == ".":
                return DOSCommandResponse(output="", new_dir=curr_dir)
            target = args[0]
            if target == "..":
                # go up
                norm = vfs.normalize_path(curr_dir)
                parts_p = [p for p in norm.split("\\") if p]
                if len(parts_p) > 1:
                    new_path = parts_p[0] + "\\" + "\\".join(parts_p[1:-1])
                else:
                    new_path = "C:\\"
                return DOSCommandResponse(output="", new_dir=new_path)
            
            # resolve relative or absolute
            target_norm = vfs.normalize_path(target if target.upper().startswith("C:") else f"{curr_dir}\\{target}")
            node = vfs.get_node(target_norm)
            if node and node.is_dir:
                return DOSCommandResponse(output="", new_dir=target_norm)
            return DOSCommandResponse(output=f"Invalid directory: {target}", new_dir=curr_dir, status_code=1)

        elif verb == "dir":
            target_path = curr_dir
            if args:
                t = args[0]
                target_path = vfs.normalize_path(t if t.upper().startswith("C:") else f"{curr_dir}\\{t}")
            nodes = vfs.list_dir(target_path)
            out_lines = [
                f" Volume in drive C has no label.",
                f" Directory of {target_path}",
                ""
            ]
            total_size = 0
            for n in nodes:
                kind = "<DIR>        " if n.is_dir else f"     {n.size:8d}"
                out_lines.append(f"{n.name:<18} {kind}  {n.modified_at}")
                total_size += n.size
            out_lines.append(f"\n        {len(nodes)} File(s)    {total_size:,} bytes")
            out_lines.append("        2 Dir(s)     12,582,912 bytes free")
            return DOSCommandResponse(output="\r\n".join(out_lines), new_dir=curr_dir)

        elif verb in ("type", "cat"):
            if not args:
                return DOSCommandResponse(output="Syntax error: File required.", new_dir=curr_dir, status_code=1)
            f_name = args[0]
            target_file = vfs.normalize_path(f_name if f_name.upper().startswith("C:") else f"{curr_dir}\\{f_name}")
            node = vfs.get_node(target_file)
            if not node:
                return DOSCommandResponse(output=f"File not found - {f_name}", new_dir=curr_dir, status_code=1)
            if node.is_dir:
                return DOSCommandResponse(output=f"Access denied - {f_name} is a directory.", new_dir=curr_dir, status_code=1)
            return DOSCommandResponse(output=node.content or "[EMPTY FILE]", new_dir=curr_dir)

        elif verb == "echo":
            return DOSCommandResponse(output=" ".join(args), new_dir=curr_dir)

        elif verb == "chimera":
            # Secret ARG command
            if len(args) >= 2 and args[0] == "--unlock":
                phrase = " ".join(args[1:])
                success, msg, _ = arg_engine.submit_solution(phrase)
                return DOSCommandResponse(output=f"[CHIMERA CORE PROTOCOL]\r\n{msg}", new_dir=curr_dir, trigger_glitch=success)
            return DOSCommandResponse(
                output="PROJECT CHIMERA OVERRIDE UTILITY\r\nUsage: chimera --unlock <code-phrase>",
                new_dir=curr_dir
            )

        elif verb == "glitch":
            if not args:
                return DOSCommandResponse(output="Usage: glitch <filename>", new_dir=curr_dir)
            f_name = args[0]
            target_file = vfs.normalize_path(f_name if f_name.upper().startswith("C:") else f"{curr_dir}\\{f_name}")
            try:
                g_node = vfs.glitch_file(target_file, 0.4)
                return DOSCommandResponse(
                    output=f"Corrupted 0x7F memory bytes in {f_name}.\r\n{g_node.content[:100]}...",
                    new_dir=curr_dir,
                    trigger_glitch=True
                )
            except Exception as e:
                return DOSCommandResponse(output=f"Error: {e}", new_dir=curr_dir, status_code=1)

        return DOSCommandResponse(output=f"Bad command or file name: '{verb}'", new_dir=curr_dir, status_code=1)

    # Static Assets & Frontend UI Mount
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

        @app.get("/", response_class=HTMLResponse)
        def get_index() -> FileResponse:
            index_path = static_dir / "index.html"
            if index_path.exists():
                return FileResponse(index_path)
            return HTMLResponse("<h1>Phantasm-OS 95 Backend Ready</h1>")

    return app


# Module-level application instance
app = create_app()
