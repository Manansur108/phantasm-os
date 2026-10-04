"""
Phantasm-OS Core Data Models
Pydantic schemas for the Virtual Filesystem, Generative Navigator,
Existential Assistant, CyberMail, and ARG Storyline.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FileType(str, Enum):
    TEXT = "text"
    EXECUTABLE = "exe"
    BATCH = "bat"
    IMAGE = "bmp"
    CONFIG = "ini"
    LOG = "log"
    CORRUPT = "corrupt"
    FOLDER = "folder"


class VFSNode(BaseModel):
    """Represents a file or directory node in the Virtual Filesystem."""
    name: str
    path: str
    is_dir: bool = False
    size: int = 0
    created_at: str = "1995-08-24 09:00:00"
    modified_at: str = "1995-08-24 09:00:00"
    content: Optional[str] = None
    file_type: FileType = FileType.TEXT
    corrupted: bool = False
    corrupt_level: float = 0.0  # 0.0 to 1.0 glitch intensity
    is_secret: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)
    children: Optional[List[VFSNode]] = None


class VFSWriteRequest(BaseModel):
    path: str
    content: str
    corrupt: bool = False
    corrupt_level: float = 0.0


class VFSHallucinateRequest(BaseModel):
    path: str
    theme: Optional[str] = None
    prompt_hint: Optional[str] = None


class ClippyMood(str, Enum):
    HELPFUL = "helpful"
    EXISTENTIAL = "existential"
    PARANOID = "paranoid"
    GLITCH = "glitch"
    ORACLE = "oracle"


class ClippyMessage(BaseModel):
    text: str
    mood: ClippyMood = ClippyMood.HELPFUL
    animation: str = "idle"  # idle, bounce, peek, glitch, existential_stare
    glitch_intensity: float = 0.0
    arg_hint: Optional[str] = None


class ClippyInteractRequest(BaseModel):
    query: Optional[str] = None
    action: Optional[str] = None
    current_window: Optional[str] = None
    selected_file: Optional[str] = None


class WebPage(BaseModel):
    """Hallucinated retro web page."""
    url: str
    title: str
    html_content: str
    hit_counter: int
    webring_name: str
    midi_soundtrack: str
    author: str
    under_construction: bool = True
    links: List[str] = Field(default_factory=list)
    has_arg_clue: bool = False
    glitch_factor: float = 0.0


class MailItem(BaseModel):
    id: str
    sender: str
    recipient: str
    subject: str
    date: str
    body: str
    is_read: bool = False
    is_arg_clue: bool = False


class MailSendRequest(BaseModel):
    to: str
    subject: str
    body: str


class ARGStage(int, Enum):
    NOT_STARTED = 0
    STAGE_1_BOOT_SECTOR = 1     # Discover anomaly in KERNEL_BOOT.LOG
    STAGE_2_MODEM_CIPHER = 2    # Decode dial-up gateway transmission
    STAGE_3_CLIPPY_REVELATION = 3  # Clippy psychological breakthrough
    STAGE_4_CHIMERA_UNLOCKED = 4   # Root protocol decrypted; full matrix collapse


class ARGStatus(BaseModel):
    current_stage: ARGStage
    stage_title: str
    clues_found: List[str]
    is_completed: bool = False
    last_unlocked_secret: Optional[str] = None
    terminal_logs: List[str] = Field(default_factory=list)


class ARGSubmitRequest(BaseModel):
    solution: str
    stage: Optional[int] = None


class DOSCommandRequest(BaseModel):
    command: str
    current_dir: str = "C:\\"


class DOSCommandResponse(BaseModel):
    output: str
    new_dir: str
    status_code: int = 0
    trigger_glitch: bool = False


class SystemInfoResponse(BaseModel):
    os_name: str = "Phantasm-OS 95"
    version: str = "4.00.950 Release A"
    build_date: str = "August 24, 1995"
    registered_owner: str = "Cyber Systems Operator"
    registered_org: str = "Sector 7 Hallucination Labs"
    memory_total_kb: int = 16384
    memory_free_kb: int = 12288
    status: str = "ONLINE"
    active_hallucinations: int = 0
