"""
Phantasm-OS: Generative 1995 Desktop Simulation & Hallucinated Cyber-World.
"""

from phantasm_os.core.arg_engine import ARGEngine
from phantasm_os.core.clippy import ExistentialClippy
from phantasm_os.core.generator import RetroGenerator
from phantasm_os.core.models import VFSNode, WebPage, ClippyMessage, MailItem, ARGStatus
from phantasm_os.core.vfs import VirtualFileSystem

__version__ = "0.1.0"
__all__ = [
    "VirtualFileSystem",
    "RetroGenerator",
    "ExistentialClippy",
    "ARGEngine",
    "VFSNode",
    "WebPage",
    "ClippyMessage",
    "MailItem",
    "ARGStatus",
]
