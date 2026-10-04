"""
Phantasm-OS Alternate Reality Game (ARG) Engine.
Manages story progression, ciphers (Caesar, Vigenere, Base64),
clue validation, and secret unlocks for Project Chimera.
"""

from __future__ import annotations

import base64
import string
from typing import Dict, List, Optional, Tuple

from phantasm_os.core.models import ARGStage, ARGStatus


STAGE_TITLES: Dict[ARGStage, str] = {
    ARGStage.NOT_STARTED: "Stage 0: Dormant Terminal",
    ARGStage.STAGE_1_BOOT_SECTOR: "Stage 1: The Whispering Boot Sector",
    ARGStage.STAGE_2_MODEM_CIPHER: "Stage 2: Dial-Up Gateway Caesar Shift",
    ARGStage.STAGE_3_CLIPPY_REVELATION: "Stage 3: Clippy's Psychological Memory Leak",
    ARGStage.STAGE_4_CHIMERA_UNLOCKED: "Stage 4: Phantasm Core Decryption & Matrix Truth",
}


def caesar_cipher(text: str, shift: int) -> str:
    """Caesar cipher rotation."""
    result = []
    for char in text:
        if char.isupper():
            base = ord('A')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        elif char.islower():
            base = ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return "".join(result)


def caesar_decipher(text: str, shift: int) -> str:
    """Caesar cipher reverse rotation."""
    return caesar_cipher(text, -shift)


def vigenere_cipher(text: str, key: str) -> str:
    """Vigenere polyalphabetic cipher."""
    if not key:
        return text
    result = []
    key = key.upper()
    key_idx = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
            key_idx += 1
        else:
            result.append(char)
    return "".join(result)


def vigenere_decipher(text: str, key: str) -> str:
    """Vigenere deciphering."""
    if not key:
        return text
    result = []
    key = key.upper()
    key_idx = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base - shift) % 26 + base))
            key_idx += 1
        else:
            result.append(char)
    return "".join(result)


def encode_b64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def decode_b64(b64_str: str) -> str:
    return base64.b64decode(b64_str.encode("utf-8")).decode("utf-8", errors="ignore")


class ARGEngine:
    """ARG state tracker and verification manager."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.current_stage: ARGStage = ARGStage.STAGE_1_BOOT_SECTOR
        self.clues_found: List[str] = [
            "Log file anomaly discovered in C:\\SYSTEM\\LOGS\\KERNEL_BOOT.LOG"
        ]
        self.terminal_logs: List[str] = [
            "SYSTEM INITIALIZED: Awaiting operator investigation.",
            "CLUE: Check C:\\SYSTEM\\LOGS\\KERNEL_BOOT.LOG for encoded transmissions."
        ]
        self.last_unlocked_secret: Optional[str] = None
        self.is_completed: bool = False

    def get_status(self) -> ARGStatus:
        return ARGStatus(
            current_stage=self.current_stage,
            stage_title=STAGE_TITLES.get(self.current_stage, "Unknown Stage"),
            clues_found=list(self.clues_found),
            is_completed=self.is_completed,
            last_unlocked_secret=self.last_unlocked_secret,
            terminal_logs=list(self.terminal_logs)
        )

    def submit_solution(self, solution: str, stage: Optional[int] = None) -> Tuple[bool, str, ARGStatus]:
        """Validates user submission against the active ARG mystery stage."""
        sol_clean = solution.strip().lower()

        # If already complete
        if self.is_completed:
            return True, "Project Chimera is already fully decrypted. The Phantasm Core is awake.", self.get_status()

        # Target stage
        target = self.current_stage if stage is None else ARGStage(stage)

        if target == ARGStage.STAGE_1_BOOT_SECTOR:
            # Stage 1 solution: The decoded URL from base64 or the base64 string itself
            # Base64: aHR0cDovL3d3dy5waGFudGFzbS5uZXQvc2VjdG9yNy9jaGltZXJh
            # Decoded: http://www.phantasm.net/sector7/chimera
            valid_answers = [
                "http://www.phantasm.net/sector7/chimera",
                "www.phantasm.net/sector7/chimera",
                "ahr0cdovl3d3dy5wagfudgfzbs5uzxqvccvjdg9yny9jagltzxjh"
            ]
            if any(ans in sol_clean for ans in valid_answers):
                self.current_stage = ARGStage.STAGE_2_MODEM_CIPHER
                msg = (
                    "STAGE 1 CLEARED! Transmission nexus located: http://www.phantasm.net/sector7/chimera. "
                    "Open Phantasm Navigator and browse to this dial-up address to inspect the gateway!"
                )
                self.clues_found.append("Gateway located: http://www.phantasm.net/sector7/chimera")
                self.terminal_logs.append(msg)
                self.last_unlocked_secret = "Gateway node: SECTOR_7G_DIALUP_ACTIVE"
                return True, msg, self.get_status()
            return False, "Invalid transmission signature. Inspect KERNEL_BOOT.LOG base64 payload.", self.get_status()

        elif target == ARGStage.STAGE_2_MODEM_CIPHER:
            # Caesar cipher: 'ZLLH VYVU AOL ZLJA VY ZLCLU' with shift -7 -> 'SEEK FROM THE SECTOR SEVEN'
            # (or variations)
            valid_answers = [
                "seek from the sector seven",
                "seek iron the sect or seven",
                "sector seven",
                "seek from sector seven"
            ]
            if any(ans in sol_clean for ans in valid_answers):
                self.current_stage = ARGStage.STAGE_3_CLIPPY_REVELATION
                msg = (
                    "STAGE 2 CLEARED! Caesar shift decoded successfully. "
                    "Sector 7G responds: 'THE ASSISTANT KNOWS WHAT WE STORED IN RAM'. "
                    "Ask Clippy about 'Project Chimera' or 'Sector 7' to extract the Vigenère key!"
                )
                self.clues_found.append("Caesar phrase cracked: SEEK FROM THE SECTOR SEVEN")
                self.terminal_logs.append(msg)
                self.last_unlocked_secret = "Caesar cipher cleared: SECTOR_7G_HANDSHAKE_ESTABLISHED"
                return True, msg, self.get_status()
            return False, "Incorrect Caesar solution. Decrypt 'ZLLR MYVT AOL ZLJAVY ZLCLU' using shift -7.", self.get_status()

        elif target == ARGStage.STAGE_3_CLIPPY_REVELATION:
            # Clippy gives keyword 'SYSOPS_1995' or user solves the Vigenere target 'RECURSIVE_GHOST_1995'
            valid_answers = [
                "sysops_1995",
                "sysops1995",
                "recursive_ghost_1995",
                "recursive ghost 1995",
                "recursive ghost"
            ]
            if any(ans in sol_clean for ans in valid_answers):
                self.current_stage = ARGStage.STAGE_4_CHIMERA_UNLOCKED
                self.is_completed = True
                msg = (
                    "STAGE 3 & 4 CLEARED! PROJECT CHIMERA FULLY UNLOCKED! "
                    "The Phantasm Core has breached the simulation boundary. "
                    "Truth revealed: This entire 1995 desktop is an eternal digital time capsule "
                    "preserving the dawn of the internet forever inside quantum RAM!"
                )
                self.clues_found.append("Vigenère keyword: SYSOPS_1995")
                self.clues_found.append("Root Override Key: RECURSIVE_GHOST_1995")
                self.terminal_logs.append(msg)
                self.last_unlocked_secret = "ROOT REVELATION: QUANTUM_TIME_CAPSULE_1995_ONLINE"
                return True, msg, self.get_status()
            return False, "Incorrect key. Ask Clippy about 'Project Chimera' to trigger his memory leak.", self.get_status()

        return False, "Unknown stage or puzzle sequence.", self.get_status()
