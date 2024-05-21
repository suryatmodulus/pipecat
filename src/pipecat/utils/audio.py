#
# Copyright (c) 2024, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import numpy as np
import pyloudnorm as pyln


def compute_rms(audio: np.ndarray):
    return np.sqrt(np.mean(audio**2))


def normalize_value(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)


def calculate_audio_volume(audio: bytes, sample_rate: int) -> float:
    audio_np = np.frombuffer(audio, dtype=np.int16)
    audio_float = audio_np.astype(np.float64)

    block_size = audio_np.size / sample_rate
    meter = pyln.Meter(sample_rate, block_size=block_size)
    loudness = meter.integrated_loudness(audio_float)

    # Loudness goes from -20 to 80 (more or less), where -20 is quiet and 80 is
    # loud.
    loudness = normalize_value(loudness, -20, 80)

    return loudness


def exp_smoothing(value: float, prev_value: float, factor: float) -> float:
    return prev_value + factor * (value - prev_value)
