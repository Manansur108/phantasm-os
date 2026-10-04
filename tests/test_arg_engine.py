"""
Unit tests for Alternate Reality Game (ARG) Engine and Ciphers.
"""

from phantasm_os.core.arg_engine import (
    ARGEngine,
    caesar_cipher,
    caesar_decipher,
    decode_b64,
    encode_b64,
    vigenere_cipher,
    vigenere_decipher,
)
from phantasm_os.core.models import ARGStage


def test_caesar_cipher_roundtrip():
    orig = "SEEK FROM THE SECTOR SEVEN"
    shift = 7
    encrypted = caesar_cipher(orig, shift)
    decrypted = caesar_decipher(encrypted, shift)
    assert decrypted == orig
    assert encrypted == "ZLLR MYVT AOL ZLJAVY ZLCLU"


def test_vigenere_cipher_roundtrip():
    orig = "PHANTASM_CORE"
    key = "SYSOPS"
    enc = vigenere_cipher(orig, key)
    dec = vigenere_decipher(enc, key)
    assert dec == orig


def test_base64_roundtrip():
    url = "http://www.phantasm.net/sector7/chimera"
    b64 = encode_b64(url)
    assert decode_b64(b64) == url


def test_arg_progression_flow():
    arg = ARGEngine()
    status = arg.get_status()
    assert status.current_stage == ARGStage.STAGE_1_BOOT_SECTOR
    assert not status.is_completed

    # Submit invalid stage 1
    success, _, _ = arg.submit_solution("wrong answer")
    assert success is False
    assert arg.current_stage == ARGStage.STAGE_1_BOOT_SECTOR

    # Submit correct stage 1 solution
    success, msg, status = arg.submit_solution("http://www.phantasm.net/sector7/chimera")
    assert success is True
    assert status.current_stage == ARGStage.STAGE_2_MODEM_CIPHER

    # Submit correct stage 2 solution
    success, msg, status = arg.submit_solution("seek from the sector seven")
    assert success is True
    assert status.current_stage == ARGStage.STAGE_3_CLIPPY_REVELATION

    # Submit correct stage 3 & 4 solution
    success, msg, status = arg.submit_solution("SYSOPS_1995")
    assert success is True
    assert status.is_completed is True
    assert status.current_stage == ARGStage.STAGE_4_CHIMERA_UNLOCKED
