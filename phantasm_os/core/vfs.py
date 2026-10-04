"""
Phantasm-OS Virtual Filesystem (VFS).
Deterministic hierarchical in-memory filesystem with 1995 authenticity,
corruption glitching, search, and JSON export/import.
"""

from __future__ import annotations

import copy
import random
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from phantasm_os.core.models import FileType, VFSNode


GLITCH_CHARACTERS = ["░", "▒", "▓", "█", "§", "¶", "µ", "æ", "Ø", "¥", "©", "Ø", "¶", "▲", "▼", "◄", "►", "■", "♦", "0x7F", "???"]


class VirtualFileSystem:
    """Hierarchical virtual filesystem representing an authentic 1995 C:\\ drive."""

    def __init__(self, seed_defaults: bool = True) -> None:
        self._root: Dict[str, Any] = {}
        if seed_defaults:
            self.reset()

    @staticmethod
    def normalize_path(path: str) -> str:
        """Converts any path representation into standard C:\\DIR\\SUBDIR format."""
        if not path or path.strip() == "":
            return "C:\\"
        clean = path.replace("/", "\\").strip()
        if not clean.upper().startswith("C:"):
            if clean.startswith("\\"):
                clean = "C:" + clean
            else:
                clean = "C:\\" + clean
        else:
            # e.g., C:MYDOCS -> C:\MYDOCS
            if len(clean) == 2:
                clean = "C:\\"
            elif clean[2] != "\\":
                clean = "C:\\" + clean[2:]

        # Eliminate duplicate backslashes except root
        parts = [p for p in clean.split("\\") if p]
        if not parts:
            return "C:\\"
        drive = parts[0].upper()
        if not drive.endswith(":"):
            drive = drive + ":"
        subparts = parts[1:]
        # Normalize .. and .
        resolved: List[str] = []
        for segment in subparts:
            if segment == ".":
                continue
            elif segment == "..":
                if resolved:
                    resolved.pop()
            else:
                resolved.append(segment.upper())
        if not resolved:
            return f"{drive}\\"
        return f"{drive}\\" + "\\".join(resolved)

    def reset(self) -> None:
        """Re-seeds the filesystem with authentic 1995 files and ARG secrets."""
        self._root = {
            "name": "C:",
            "path": "C:\\",
            "is_dir": True,
            "size": 0,
            "created_at": "1995-08-24 09:00:00",
            "modified_at": "1995-08-24 09:00:00",
            "file_type": FileType.FOLDER.value,
            "children": {}
        }

        # Root files
        self._seed_file(
            "C:\\AUTOEXEC.BAT",
            "@ECHO OFF\r\n"
            "PROMPT $P$G\r\n"
            "PATH C:\\WINDOWS;C:\\WINDOWS\\COMMAND;C:\\DOS\r\n"
            "SET TEMP=C:\\TEMP\r\n"
            "SET BLASTER=A220 I5 D1 T4\r\n"
            "SET MODEM_PORT=COM2\r\n"
            "SET MODEM_BAUD=14400\r\n"
            "REM CIPHER_SEED: OFFSET_SHIFT_PLUS_SEVEN\r\n"
            "REM CAUTION: SECTOR 7 PARITY CHECK DISABLED\r\n"
            "ECHO Phantasm-OS 1995 Kernel Initialized.\r\n",
            file_type=FileType.BATCH
        )

        self._seed_file(
            "C:\\CONFIG.SYS",
            "DEVICE=C:\\WINDOWS\\HIMEM.SYS\r\n"
            "DEVICE=C:\\WINDOWS\\EMM386.EXE NOEMS\r\n"
            "DOS=HIGH,UMB\r\n"
            "FILES=40\r\n"
            "BUFFERS=40\r\n",
            file_type=FileType.CONFIG
        )

        self._seed_file(
            "C:\\README.TXT",
            "=====================================================\r\n"
            "  WELCOME TO PHANTASM-OS (RELEASE AUGUST 1995)\r\n"
            "=====================================================\r\n\r\n"
            "Welcome to the ultimate generative desktop simulation.\r\n"
            "Explore the dial-up web via Phantasm Navigator.\r\n"
            "Organize your thoughts with RetroMail.\r\n"
            "If Clippy appears, do not panic.\r\n\r\n"
            "WARNING:\r\n"
            "Certain files within C:\\RESTRICTED and C:\\SYSTEM\\LOGS\r\n"
            "have experienced temporal memory decay. Do not execute\r\n"
            "unverified .EXE files without root authorization.\r\n\r\n"
            "Have a productive day in cyberspace!\r\n",
            file_type=FileType.TEXT
        )

        # C:\WINDOWS
        self.create_dir("C:\\WINDOWS")
        self._seed_file(
            "C:\\WINDOWS\\SYSTEM.INI",
            "[boot]\r\nshell=Explorer.exe\r\ndrivers=mmsystem.dll\r\n[386Enh]\r\n"
            "Paging=Enabled\r\nMinPagingFileSize=32768\r\n",
            file_type=FileType.CONFIG
        )
        self._seed_file(
            "C:\\WINDOWS\\WIN.INI",
            "[windows]\r\nload=\r\nrun=\r\nBeep=Yes\r\nBorderWidth=3\r\nKeyboardDelay=2\r\n",
            file_type=FileType.CONFIG
        )
        self._seed_file("C:\\WINDOWS\\NOTEPAD.EXE", "[PHANTASM-OS WIN32 BINARY HEADER: NOTEPAD]", file_type=FileType.EXECUTABLE)
        self._seed_file("C:\\WINDOWS\\NAVIGAT.EXE", "[PHANTASM-OS WIN32 BINARY HEADER: PHANTASM NAVIGATOR 2.0]", file_type=FileType.EXECUTABLE)
        self._seed_file("C:\\WINDOWS\\CLIPPY.EXE", "[PHANTASM-OS WIN32 BINARY HEADER: CLIPTRON ASSISTANT DAEMON]", file_type=FileType.EXECUTABLE)

        # C:\MYDOCS
        self.create_dir("C:\\MYDOCS")
        self._seed_file(
            "C:\\MYDOCS\\DIARY_1995.TXT",
            "August 24, 1995\r\n"
            "Today I finally installed the 28.8k baud modem. The dialing noise sounds like an\r\n"
            "alien mothership contacting deep space. I signed up for a GeoCities account\r\n"
            "and put a flaming skull GIF on my homepage.\r\n\r\n"
            "Late last night while browsing early Usenet boards, I received a strange transmission\r\n"
            "referencing 'Project Chimera' and Sector 7G. Clippy started glitching on the screen,\r\n"
            "asking me if I felt the heat from the CRT tube. Probably just a corrupt driver.\r\n",
            file_type=FileType.TEXT
        )
        self._seed_file(
            "C:\\MYDOCS\\TODO_AUGUST95.TXT",
            "[ ] Buy CD-ROM drive (4X speed)\r\n"
            "[ ] Download Netscape Navigator 2.0 beta\r\n"
            "[ ] Back up floppy disks\r\n"
            "[ ] Solve the strange modem beep in KERNEL_BOOT.LOG\r\n"
            "[ ] Tell Clippy to stop talking about existential dread\r\n",
            file_type=FileType.TEXT
        )

        # C:\SYSTEM\LOGS
        self.create_dir("C:\\SYSTEM")
        self.create_dir("C:\\SYSTEM\\LOGS")
        self._seed_file(
            "C:\\SYSTEM\\LOGS\\KERNEL_BOOT.LOG",
            "[BOOT_SEQ: 00:00:01] CMOS Check OK\r\n"
            "[BOOT_SEQ: 00:00:02] VESA BIOS Extensions detected\r\n"
            "[BOOT_SEQ: 00:00:03] Sound Blaster 16 DSP 4.05 ready\r\n"
            "[BOOT_SEQ: 00:00:04] Loading Virtual Filesystem...\r\n"
            "[ANOMALY: SECTOR_7G] Unexpected transmission in buffer:\r\n"
            ">> RECON_DATA: aHR0cDovL3d3dy5waGFudGFzbS5uZXQvc2VjdG9yNy9jaGltZXJh <<\r\n"
            "[BOOT_SEQ: 00:00:05] Kernel loaded successfully. Hallucination engine active.\r\n",
            file_type=FileType.LOG,
            is_secret=True
        )

        # C:\RESTRICTED
        self.create_dir("C:\\RESTRICTED")
        self._seed_file(
            "C:\\RESTRICTED\\CHIMERA.EXE",
            "PROJECT CHIMERA // PHANTASM CORE OVERRIDE\r\n"
            "Access requires authorization code phrase from the gateway.\r\n"
            "Run 'chimera --unlock <code-phrase>' in Phantasm DOS or Sector 7G Console.\r\n",
            file_type=FileType.EXECUTABLE,
            is_secret=True
        )
        self._seed_file(
            "C:\\RESTRICTED\\PARITY_GLITCH.DAT",
            "0x00FF 0x7E1A 0xDEADBEEF 0x4348494D455241\r\n"
            "§§§ SECTOR REALLOCATION FAILURE §§§\r\n"
            "THE SYSTEM CANNOT DISTINGUISH MEMORY FROM REALITY\r\n",
            file_type=FileType.CORRUPT,
            corrupted=True,
            corrupt_level=0.75
        )

        # C:\CORRUPT_SECTOR
        self.create_dir("C:\\CORRUPT_SECTOR")
        self._seed_file(
            "C:\\CORRUPT_SECTOR\\MEMORY_DUMP_0x7F.DAT",
            "░▒▓█ ERROR IN TIME RUNTIME: 1995.08.24.23:59:59 █▓▒░\r\n"
            "You were not supposed to read this sector.\r\n"
            "Clippy knows you are here.\r\n"
            "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\r\n",
            file_type=FileType.CORRUPT,
            corrupted=True,
            corrupt_level=0.9
        )

    def _seed_file(
        self,
        path: str,
        content: str,
        file_type: FileType = FileType.TEXT,
        is_secret: bool = False,
        corrupted: bool = False,
        corrupt_level: float = 0.0
    ) -> None:
        norm = self.normalize_path(path)
        parts = [p for p in norm.split("\\") if p]
        parent = self._get_or_create_parent(parts[:-1])
        filename = parts[-1]
        parent["children"][filename] = {
            "name": filename,
            "path": norm,
            "is_dir": False,
            "size": len(content.encode("utf-8")),
            "created_at": "1995-08-24 09:00:00",
            "modified_at": "1995-08-24 09:00:00",
            "content": content,
            "file_type": file_type.value,
            "corrupted": corrupted,
            "corrupt_level": corrupt_level,
            "is_secret": is_secret,
            "metadata": {}
        }

    def _get_or_create_parent(self, parts: List[str]) -> Dict[str, Any]:
        curr = self._root
        current_path = parts[0] + "\\"
        for part in parts[1:]:
            if "children" not in curr:
                curr["children"] = {}
            if part not in curr["children"]:
                current_path = (current_path.rstrip("\\") + "\\" + part).upper()
                curr["children"][part] = {
                    "name": part,
                    "path": current_path,
                    "is_dir": True,
                    "size": 0,
                    "created_at": "1995-08-24 09:00:00",
                    "modified_at": "1995-08-24 09:00:00",
                    "file_type": FileType.FOLDER.value,
                    "children": {}
                }
            curr = curr["children"][part]
        return curr

    def _traverse(self, norm_path: str) -> Optional[Dict[str, Any]]:
        parts = [p for p in norm_path.split("\\") if p]
        if not parts:
            return None
        if len(parts) == 1:
            return self._root
        curr = self._root
        for part in parts[1:]:
            if not curr.get("is_dir"):
                return None
            children = curr.get("children", {})
            if part not in children:
                return None
            curr = children[part]
        return curr

    def exists(self, path: str) -> bool:
        norm = self.normalize_path(path)
        return self._traverse(norm) is not None

    def get_node(self, path: str) -> Optional[VFSNode]:
        norm = self.normalize_path(path)
        raw = self._traverse(norm)
        if raw is None:
            return None
        return self._node_from_raw(raw)

    def list_dir(self, path: str) -> List[VFSNode]:
        norm = self.normalize_path(path)
        raw = self._traverse(norm)
        if raw is None or not raw.get("is_dir"):
            return []
        nodes: List[VFSNode] = []
        for child_raw in raw.get("children", {}).values():
            nodes.append(self._node_from_raw(child_raw))
        # Sort folders first, then alphabetically
        nodes.sort(key=lambda n: (not n.is_dir, n.name.lower()))
        return nodes

    def create_dir(self, path: str) -> VFSNode:
        norm = self.normalize_path(path)
        existing = self._traverse(norm)
        if existing:
            if not existing.get("is_dir"):
                raise ValueError(f"Path '{path}' exists and is not a directory.")
            return self._node_from_raw(existing)
        parts = [p for p in norm.split("\\") if p]
        parent = self._get_or_create_parent(parts[:-1])
        dirname = parts[-1]
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_dir = {
            "name": dirname,
            "path": norm,
            "is_dir": True,
            "size": 0,
            "created_at": now_str,
            "modified_at": now_str,
            "file_type": FileType.FOLDER.value,
            "children": {}
        }
        parent["children"][dirname] = new_dir
        return self._node_from_raw(new_dir)

    def write_file(
        self,
        path: str,
        content: str,
        corrupt: bool = False,
        corrupt_level: float = 0.0
    ) -> VFSNode:
        norm = self.normalize_path(path)
        parts = [p for p in norm.split("\\") if p]
        if len(parts) <= 1:
            raise ValueError("Cannot write file as drive root.")
        parent = self._get_or_create_parent(parts[:-1])
        filename = parts[-1]
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Determine file type from extension
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        ft = FileType.TEXT
        if ext in ("exe", "com"):
            ft = FileType.EXECUTABLE
        elif ext in ("bat", "cmd"):
            ft = FileType.BATCH
        elif ext in ("ini", "cfg", "sys"):
            ft = FileType.CONFIG
        elif ext in ("log",):
            ft = FileType.LOG
        elif ext in ("bmp", "art", "gif"):
            ft = FileType.IMAGE
        elif ext in ("dat", "corrupt"):
            ft = FileType.CORRUPT

        if corrupt or corrupt_level > 0.0:
            content = self._apply_corruption_artifacts(content, corrupt_level or 0.3)
            ft = FileType.CORRUPT

        file_node = {
            "name": filename,
            "path": norm,
            "is_dir": False,
            "size": len(content.encode("utf-8")),
            "created_at": now_str,
            "modified_at": now_str,
            "content": content,
            "file_type": ft.value,
            "corrupted": corrupt or (corrupt_level > 0),
            "corrupt_level": corrupt_level,
            "is_secret": False,
            "metadata": {}
        }
        parent["children"][filename] = file_node
        return self._node_from_raw(file_node)

    def delete_node(self, path: str) -> bool:
        norm = self.normalize_path(path)
        parts = [p for p in norm.split("\\") if p]
        if len(parts) <= 1:
            return False  # Cannot delete root C:\
        parent_raw = self._traverse("\\".join(parts[:-1]))
        if not parent_raw or not parent_raw.get("is_dir"):
            return False
        target_name = parts[-1]
        if target_name in parent_raw.get("children", {}):
            del parent_raw["children"][target_name]
            return True
        return False

    def search(self, query: str) -> List[VFSNode]:
        """Search files by name substring or file content."""
        results: List[VFSNode] = []
        q = query.lower()

        def _walk(curr: Dict[str, Any]) -> None:
            name = curr.get("name", "").lower()
            content = curr.get("content", "") or ""
            if q in name or q in content.lower():
                results.append(self._node_from_raw(curr))
            if curr.get("is_dir"):
                for child in curr.get("children", {}).values():
                    _walk(child)

        _walk(self._root)
        return results

    def glitch_file(self, path: str, intensity: float = 0.5) -> VFSNode:
        """Introduce digital corruption artifacts to an existing file."""
        norm = self.normalize_path(path)
        raw = self._traverse(norm)
        if not raw or raw.get("is_dir"):
            raise ValueError(f"File '{path}' not found or is a directory.")
        content = raw.get("content", "") or ""
        glitched_content = self._apply_corruption_artifacts(content, intensity)
        raw["content"] = glitched_content
        raw["corrupted"] = True
        raw["corrupt_level"] = max(raw.get("corrupt_level", 0.0), intensity)
        raw["file_type"] = FileType.CORRUPT.value
        raw["size"] = len(glitched_content.encode("utf-8"))
        raw["modified_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self._node_from_raw(raw)

    def hallucinate_file(self, path: str, theme: Optional[str] = None) -> VFSNode:
        """Dynamically hallucinates content for a non-existent or requested retro file."""
        norm = self.normalize_path(path)
        filename = norm.split("\\")[-1]
        ext = filename.split(".")[-1].lower() if "." in filename else "txt"

        samples = [
            f"=== ARCHIVE LOG: {filename} ===\r\nTimestamp: 1995-10-14 02:44 AM\r\n"
            f"System detected abnormal packet relay through virtual IRQ 5.\r\n"
            f"Note: If Clippy inquires about this memo, discard immediately.\r\n",
            f"REM -- {filename} AUTO-GENERATED BATCH --\r\n"
            f"ECHO Synchronizing dials with cyberspace gateway...\r\n"
            f"ECHO Baud rate: 28800 bps\r\n",
            f"SECRET MEMORANDUM // EYES ONLY\r\n"
            f"Subject: Project Chimera Protocol\r\n"
            f"Status: Sector 7 simulation boundaries stable at 99.4% fidelity.\r\n",
            f"CYBERSPORTS & BBS NOTES 1995\r\n"
            f"Dialup Node: 555-0195\r\n"
            f"User: cyber_surfer_95\r\n"
            f"Remember: The CRT phosphor never truly fades.\r\n",
        ]
        chosen = random.choice(samples)
        if theme:
            chosen = f"[THEME: {theme.upper()}]\r\n" + chosen

        return self.write_file(norm, chosen)

    @staticmethod
    def _apply_corruption_artifacts(text: str, intensity: float) -> str:
        """Injects glitch characters and visual noise into text."""
        chars = list(text)
        total = len(chars)
        glitch_count = int(total * min(max(intensity, 0.05), 0.95))
        for _ in range(glitch_count):
            idx = random.randint(0, total - 1)
            chars[idx] = random.choice(GLITCH_CHARACTERS)
        return "".join(chars)

    def _node_from_raw(self, raw: Dict[str, Any]) -> VFSNode:
        children_nodes: Optional[List[VFSNode]] = None
        if raw.get("is_dir") and "children" in raw:
            children_nodes = [
                self._node_from_raw(child) for child in raw["children"].values()
            ]
        return VFSNode(
            name=raw.get("name", ""),
            path=raw.get("path", ""),
            is_dir=raw.get("is_dir", False),
            size=raw.get("size", 0),
            created_at=raw.get("created_at", "1995-08-24 09:00:00"),
            modified_at=raw.get("modified_at", "1995-08-24 09:00:00"),
            content=raw.get("content"),
            file_type=FileType(raw.get("file_type", FileType.TEXT.value)),
            corrupted=raw.get("corrupted", False),
            corrupt_level=raw.get("corrupt_level", 0.0),
            is_secret=raw.get("is_secret", False),
            metadata=raw.get("metadata", {}),
            children=children_nodes
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes entire VFS tree to JSON-compatible dict."""
        return copy.deepcopy(self._root)

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Restores filesystem from JSON dictionary."""
        self._root = copy.deepcopy(data)
