"""
Phantasm-OS Sound Synthesis & Audio Spectrum Definitions.
Defines parameters for 56k dialup handshake, DTMF tones,
Win95 startup chimes, and CRT degauss sound waves.
"""

from typing import Dict, List, Tuple


# DTMF Dual-Tone Frequencies (Hz) for authentic dial-up tone generation
DTMF_FREQUENCIES: Dict[str, Tuple[int, int]] = {
    "1": (697, 1209),
    "2": (697, 1336),
    "3": (697, 1477),
    "4": (770, 1209),
    "5": (770, 1336),
    "6": (770, 1477),
    "7": (852, 1209),
    "8": (852, 1336),
    "9": (852, 1477),
    "*": (941, 1209),
    "0": (941, 1336),
    "#": (941, 1477),
}

# 56k Modem Handshake Sequence Stages (V.34 / V.90 simulation)
DIALUP_HANDSHAKE_STAGES: List[Dict[str, object]] = [
    {
        "stage": "dial_tone",
        "duration_ms": 1200,
        "frequencies": [350, 440],
        "type": "dual_sine",
        "description": "Continuous dial tone"
    },
    {
        "stage": "dtmf_dialing",
        "duration_ms": 1600,
        "sequence": ["5", "5", "5", "0", "1", "9", "5"],
        "tone_duration_ms": 120,
        "pause_ms": 60,
        "description": "Pulsed DTMF tones dialing ISP gateway"
    },
    {
        "stage": "ringback",
        "duration_ms": 2000,
        "frequencies": [440, 480],
        "cadence_ms": [1000, 1000],
        "description": "Remote ringback signal"
    },
    {
        "stage": "carrier_detect_ans",
        "duration_ms": 1800,
        "frequencies": [2100],
        "phase_reversals": True,
        "description": "V.25 ANS tone with 180-degree phase reversal"
    },
    {
        "stage": "scrambled_ones_v8",
        "duration_ms": 1500,
        "frequencies": [980, 1180, 1650, 1850],
        "type": "fsk_negotiation",
        "description": "V.8 modulation negotiation and capability exchange"
    },
    {
        "stage": "baudot_chirps",
        "duration_ms": 1400,
        "frequencies": [1200, 2400],
        "modulation": "line_probing",
        "description": "Line probing chirps measuring high-frequency attenuation"
    },
    {
        "stage": "white_noise_burst",
        "duration_ms": 2200,
        "type": "shaped_noise",
        "filter_low": 300,
        "filter_high": 3400,
        "description": "Scrambled symbol constellation training"
    },
    {
        "stage": "carrier_lock",
        "duration_ms": 600,
        "frequencies": [1800],
        "description": "Carrier locked at 56,000 bps - Handshake complete"
    }
]

# Retro Sound FX Profiles
RETRO_SOUND_PROFILES: Dict[str, Dict[str, object]] = {
    "win95_startup": {
        "description": "Ethereal synthesized ambient boot chord",
        "notes": [130.81, 196.00, 261.63, 329.63, 392.00, 523.25], # C3, G3, C4, E4, G4, C5
        "decay_sec": 3.8,
        "reverb": 0.65
    },
    "chord_error": {
        "description": "Windows classic chord.wav error alert",
        "frequencies": [523.25, 659.25, 783.99], # C5, E5, G5
        "duration_ms": 400
    },
    "ding": {
        "description": "Notification ding tone",
        "frequencies": [880.0],
        "decay_ms": 300
    },
    "degauss": {
        "description": "CRT monitor heavy coil degauss thud and electromagnetic hum",
        "sweep_start_hz": 60,
        "sweep_end_hz": 12,
        "duration_ms": 850
    },
    "glitch_burst": {
        "description": "Corrupted audio buffer memory static",
        "type": "fm_noise",
        "carrier_hz": 440,
        "modulator_hz": 880,
        "duration_ms": 250
    }
}


def get_dialup_stage_summary() -> Dict[str, object]:
    """Returns timing and summary statistics for the dialup handshake."""
    total_ms = sum(s.get("duration_ms", 0) for s in DIALUP_HANDSHAKE_STAGES)
    return {
        "total_handshake_ms": total_ms,
        "stage_count": len(DIALUP_HANDSHAKE_STAGES),
        "stages": [s["stage"] for s in DIALUP_HANDSHAKE_STAGES],
    }
