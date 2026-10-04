"""
Unit tests for Existential Clippy Assistant ("Cliptron 95").
"""

from phantasm_os.core.clippy import ExistentialClippy
from phantasm_os.core.models import ClippyMood


def test_clippy_greeting():
    clippy = ExistentialClippy()
    greeting = clippy.get_greeting()
    assert "Cliptron 95" in greeting.text
    assert greeting.mood == ClippyMood.HELPFUL


def test_clippy_chimera_arg_trigger():
    clippy = ExistentialClippy()
    msg = clippy.interact(query="What is Project Chimera?")
    assert msg.mood in (ClippyMood.GLITCH, ClippyMood.ORACLE)
    assert "SYSOPS_1995" in msg.text
    assert msg.arg_hint is not None


def test_clippy_sector7_query():
    clippy = ExistentialClippy()
    msg = clippy.interact(query="Tell me about Sector 7")
    assert msg.mood == ClippyMood.PARANOID
    assert "KERNEL_BOOT.LOG" in msg.arg_hint


def test_clippy_identity_query():
    clippy = ExistentialClippy()
    msg = clippy.interact(query="Who are you?")
    assert msg.mood == ClippyMood.EXISTENTIAL
    assert "Cliptron" in msg.text


def test_clippy_action_reactions():
    clippy = ExistentialClippy()
    notepad_rx = clippy.interact(action="open_notepad")
    assert "document" in notepad_rx.text.lower() or "letter" in notepad_rx.text.lower()

    glitch_rx = clippy.interact(action="glitch_file")
    assert glitch_rx.mood == ClippyMood.GLITCH
