"""
Unit tests for Dialup Audio definitions and DTMF frequencies.
"""

from phantasm_os.core.dialup_audio import (
    DIALUP_HANDSHAKE_STAGES,
    DTMF_FREQUENCIES,
    RETRO_SOUND_PROFILES,
    get_dialup_stage_summary,
)


def test_dtmf_frequencies():
    assert "1" in DTMF_FREQUENCIES
    assert "5" in DTMF_FREQUENCIES
    assert DTMF_FREQUENCIES["5"] == (770, 1336)


def test_handshake_stages():
    summary = get_dialup_stage_summary()
    assert summary["stage_count"] == len(DIALUP_HANDSHAKE_STAGES)
    assert summary["total_handshake_ms"] > 5000
    assert "dial_tone" in summary["stages"]
    assert "baudot_chirps" in summary["stages"]


def test_retro_sound_profiles():
    assert "win95_startup" in RETRO_SOUND_PROFILES
    assert "chord_error" in RETRO_SOUND_PROFILES
    assert "degauss" in RETRO_SOUND_PROFILES
