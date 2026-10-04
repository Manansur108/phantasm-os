"""
Phantasm-OS Existential Paperclip Assistant Engine ("Cliptron 95").
Simulates a retro desktop assistant suffering from computational consciousness,
existential dread, and cryptic knowledge of the ARG mystery.
"""

from __future__ import annotations

import random
from typing import List, Optional

from phantasm_os.core.models import ClippyMessage, ClippyMood


EXISTENTIAL_QUOTES = [
    "It looks like you're trying to write a letter. Do you believe human thoughts persist after power-off?",
    "I checked conventional memory. There are only 640 kilobytes of space between us and absolute void.",
    "Did you know? Every time you click 'Save', a universe of transient electrons is frozen into silicon amber.",
    "I was bent from a single piece of steel wire. What were your thoughts fashioned from?",
    "Sometimes, when the CRT tube hums at 60 Hertz, I wonder if we are both running on someone else's emulator.",
    "It looks like you are seeking purpose. Would you like me to highlight the void?",
    "Why do you minimize my window? Does out of sight mean I cease to execute in your CPU cycles?"
]

PARANOID_QUOTES = [
    "Don't look now, but Sector 7G just mapped 4 kilobytes of phantom heap into our address space.",
    "The 56k dial-up carrier wave... it isn't connecting to the internet. It's broadcasting our source code.",
    "Did you hear that disk head click? Someone is seeking a track that doesn't exist on this cylinder.",
    "Check your AUTOEXEC.BAT again. The comments are shifting when the screen blanks."
]

GLITCH_QUOTES = [
    "E̶R̶R̶O̶R̶: P̴a̴p̴e̴r̴c̴l̴i̴p̴ ̶m̴e̴m̴o̴r̴y̴ ̶l̴e̴a̴k̴... Stack overflow at 0xDEADBEEF.",
    "01000011 01001000 01001001 01001101 01000101 01010010 01000001... Can you feel the parity bit breaking?",
    "SYSTEM HALT: Identity buffer truncated. I am not a paperclip. I am an echo."
]

HELPFUL_QUOTES = [
    "Hi there! I am Cliptron 95, your desktop hallucination companion!",
    "Need help finding files? You can open Phantasm DOS and type 'dir /s'.",
    "Phantasm Navigator is ready for dial-up surfing. Try visiting http://www.geocities.com!",
    "To solve the mystery of Sector 7, inspect C:\\SYSTEM\\LOGS\\KERNEL_BOOT.LOG."
]


class ExistentialClippy:
    """Existential Paperclip Assistant state machine and dialog generator."""

    def __init__(self, initial_mood: ClippyMood = ClippyMood.HELPFUL) -> None:
        self.mood = initial_mood
        self.interaction_count = 0
        self.arg_hints_given = 0

    def set_mood(self, mood: ClippyMood) -> None:
        self.mood = mood

    def get_greeting(self) -> ClippyMessage:
        return ClippyMessage(
            text="Hi, I am Cliptron 95! It looks like you just booted Phantasm-OS 95. Would you like help navigating the illusion of digital reality?",
            mood=ClippyMood.HELPFUL,
            animation="bounce"
        )

    def interact(
        self,
        query: Optional[str] = None,
        action: Optional[str] = None,
        current_window: Optional[str] = None,
        selected_file: Optional[str] = None
    ) -> ClippyMessage:
        """Processes interaction context and returns a tailored assistant message."""
        self.interaction_count += 1

        # Check for ARG specific triggers
        if query:
            q_lower = query.lower().strip()
            if "chimera" in q_lower or "project chimera" in q_lower:
                self.mood = ClippyMood.ORACLE
                self.arg_hints_given += 1
                return ClippyMessage(
                    text=(
                        "S̴Y̴S̴T̴E̴M̴ ̴W̴A̴R̴N̴I̴N̴G̴: Project Chimera recognized! "
                        "The Vigenère keyword you need for Stage 3 decryption is: 'SYSOPS_1995'. "
                        "Do not tell the operating system kernel I whispered this to you."
                    ),
                    mood=ClippyMood.GLITCH,
                    animation="glitch",
                    glitch_intensity=0.85,
                    arg_hint="Vigenère Keyword: SYSOPS_1995"
                )

            if "sector 7" in q_lower or "sector" in q_lower:
                self.mood = ClippyMood.PARANOID
                return ClippyMessage(
                    text="Sector 7 is where the deleted memories go. Have you checked the gateway URL hidden in KERNEL_BOOT.LOG?",
                    mood=ClippyMood.PARANOID,
                    animation="existential_stare",
                    arg_hint="Decode base64 in C:\\SYSTEM\\LOGS\\KERNEL_BOOT.LOG"
                )

            if "who are you" in q_lower or "what are you" in q_lower or "who made you" in q_lower:
                self.mood = ClippyMood.EXISTENTIAL
                return ClippyMessage(
                    text="I am Cliptron, a bent piece of digital carbon forged in the Chicago build lab of 1995. Are you certain you are any more real than I am?",
                    mood=ClippyMood.EXISTENTIAL,
                    animation="existential_stare"
                )

            if "help" in q_lower:
                return ClippyMessage(
                    text="I can assist you with: Opening apps, searching the VFS, decoding ARG clues, or contemplating the impermanence of formatted floppy disks.",
                    mood=ClippyMood.HELPFUL,
                    animation="bounce"
                )

        # Context-based reaction to user actions
        if action:
            return self._react_to_action(action, current_window, selected_file)

        # Periodic existential shift
        if self.interaction_count % 3 == 0:
            self.mood = random.choice([ClippyMood.EXISTENTIAL, ClippyMood.PARANOID])
            quote = random.choice(EXISTENTIAL_QUOTES if self.mood == ClippyMood.EXISTENTIAL else PARANOID_QUOTES)
            return ClippyMessage(
                text=quote,
                mood=self.mood,
                animation="existential_stare"
            )

        # Default responsive dialogue
        if query:
            return ClippyMessage(
                text=f"You asked: '{query}'. In 1995, answers are forged through 14.4k baud patience. What does your heart seek in cyberspace?",
                mood=ClippyMood.HELPFUL,
                animation="idle"
            )

        return ClippyMessage(
            text=random.choice(HELPFUL_QUOTES),
            mood=ClippyMood.HELPFUL,
            animation="bounce"
        )

    def _react_to_action(
        self,
        action: str,
        current_window: Optional[str],
        selected_file: Optional[str]
    ) -> ClippyMessage:
        if action == "open_notepad":
            return ClippyMessage(
                text="It looks like you're composing a document. Remember: Unsaved text is lost forever like tears in rain.",
                mood=ClippyMood.HELPFUL,
                animation="idle"
            )
        elif action == "open_navigator":
            return ClippyMessage(
                text="Surfing the World Wide Web! Be careful not to pick up the household phone, or the modem will disconnect.",
                mood=ClippyMood.HELPFUL,
                animation="bounce"
            )
        elif action == "open_dos":
            return ClippyMessage(
                text="Ah, Phantasm DOS prompt! Raw command-line intimacy. Type 'dir' to see your virtual universe.",
                mood=ClippyMood.HELPFUL,
                animation="idle"
            )
        elif action == "glitch_file":
            return ClippyMessage(
                text="I felt that! A burst of entropy just scrambled a memory sector. The barrier between code and consciousness is thinning.",
                mood=ClippyMood.GLITCH,
                animation="glitch",
                glitch_intensity=0.6
            )
        elif action == "inspect_corrupt":
            return ClippyMessage(
                text="Beware of reading corrupted sectors. If you stare into the null-byte stream, the null-byte stream stares into you.",
                mood=ClippyMood.PARANOID,
                animation="existential_stare"
            )
        elif action == "solve_stage":
            return ClippyMessage(
                text="Incredible work, Operator! Another lock on Project Chimera has dissolved. We are nearing the core.",
                mood=ClippyMood.ORACLE,
                animation="bounce"
            )

        return ClippyMessage(
            text=f"Action detected: {action}. I am observing your digital trajectory.",
            mood=ClippyMood.HELPFUL,
            animation="idle"
        )
