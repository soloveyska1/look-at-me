#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ◉  САЙМУРР — СМОТРЕЛА                                                    ║
║     PROFESSIONAL MASTERING SCRIPT                                            ║
║                                                                              ║
║     Основано на анализе команды экспертов:                                   ║
║     - Mastering Engineer                                                     ║
║     - Frequency Analyst                                                      ║
║     - Loudness Engineer                                                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import scipy.io.wavfile as wav
from scipy import signal
from scipy.ndimage import uniform_filter1d
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

INPUT_FILE = "/home/user/look-at-me/СМОТРЕЛА_teaser.wav"
OUTPUT_STREAMING = "/home/user/look-at-me/СМОТРЕЛА_MASTER_STREAMING.wav"
OUTPUT_CLUB = "/home/user/look-at-me/СМОТРЕЛА_MASTER_CLUB.wav"

# From expert analysis:
TARGET_LUFS_STREAMING = -14.0  # Spotify/YouTube/Apple Music
TARGET_LUFS_CLUB = -9.0        # Club/DJ/Promo
DROP_TIME = 17.163             # Critical moment

# =============================================================================
# DSP FUNCTIONS
# =============================================================================

def db_to_linear(db):
    """Convert dB to linear scale"""
    return 10 ** (db / 20)

def linear_to_db(linear):
    """Convert linear to dB scale"""
    return 20 * np.log10(np.maximum(linear, 1e-10))

def calculate_rms(audio):
    """Calculate RMS level"""
    return np.sqrt(np.mean(audio ** 2))

def calculate_lufs_simple(audio, sample_rate):
    """Simplified LUFS calculation (ITU-R BS.1770 inspired)"""
    # K-weighting filters
    # Pre-filter (high shelf)
    b_pre = [1.53512485958697, -2.69169618940638, 1.19839281085285]
    a_pre = [1.0, -1.69065929318241, 0.73248077421585]

    # High-pass filter
    b_hp = [1.0, -2.0, 1.0]
    a_hp = [1.0, -1.99004745483398, 0.99007225036621]

    if len(audio.shape) > 1:
        # Stereo
        left = signal.lfilter(b_pre, a_pre, audio[:, 0])
        left = signal.lfilter(b_hp, a_hp, left)
        right = signal.lfilter(b_pre, a_pre, audio[:, 1])
        right = signal.lfilter(b_hp, a_hp, right)

        # Mean square
        ms_left = np.mean(left ** 2)
        ms_right = np.mean(right ** 2)

        # Weighted sum (no surround channels)
        loudness = -0.691 + 10 * np.log10(ms_left + ms_right)
    else:
        # Mono
        filtered = signal.lfilter(b_pre, a_pre, audio)
        filtered = signal.lfilter(b_hp, a_hp, filtered)
        ms = np.mean(filtered ** 2)
        loudness = -0.691 + 10 * np.log10(ms)

    return loudness

def parametric_eq_band(audio, sample_rate, freq, gain_db, q):
    """Apply parametric EQ band (peaking filter)"""
    if abs(gain_db) < 0.1:
        return audio

    A = db_to_linear(gain_db / 2)
    w0 = 2 * np.pi * freq / sample_rate
    alpha = np.sin(w0) / (2 * q)

    b0 = 1 + alpha * A
    b1 = -2 * np.cos(w0)
    b2 = 1 - alpha * A
    a0 = 1 + alpha / A
    a1 = -2 * np.cos(w0)
    a2 = 1 - alpha / A

    b = [b0/a0, b1/a0, b2/a0]
    a = [1, a1/a0, a2/a0]

    if len(audio.shape) > 1:
        result = np.zeros_like(audio)
        for ch in range(audio.shape[1]):
            result[:, ch] = signal.lfilter(b, a, audio[:, ch])
        return result
    else:
        return signal.lfilter(b, a, audio)

def high_pass_filter(audio, sample_rate, freq, order=4):
    """High-pass filter"""
    nyq = sample_rate / 2
    normalized_freq = freq / nyq
    b, a = signal.butter(order, normalized_freq, btype='high')

    if len(audio.shape) > 1:
        result = np.zeros_like(audio)
        for ch in range(audio.shape[1]):
            result[:, ch] = signal.filtfilt(b, a, audio[:, ch])
        return result
    else:
        return signal.filtfilt(b, a, audio)

def high_shelf(audio, sample_rate, freq, gain_db):
    """High shelf filter for 'air' frequencies"""
    if abs(gain_db) < 0.1:
        return audio

    A = db_to_linear(gain_db / 2)
    w0 = 2 * np.pi * freq / sample_rate
    alpha = np.sin(w0) / 2 * np.sqrt((A + 1/A) * (1/0.7 - 1) + 2)

    b0 = A * ((A + 1) + (A - 1) * np.cos(w0) + 2 * np.sqrt(A) * alpha)
    b1 = -2 * A * ((A - 1) + (A + 1) * np.cos(w0))
    b2 = A * ((A + 1) + (A - 1) * np.cos(w0) - 2 * np.sqrt(A) * alpha)
    a0 = (A + 1) - (A - 1) * np.cos(w0) + 2 * np.sqrt(A) * alpha
    a1 = 2 * ((A - 1) - (A + 1) * np.cos(w0))
    a2 = (A + 1) - (A - 1) * np.cos(w0) - 2 * np.sqrt(A) * alpha

    b = [b0/a0, b1/a0, b2/a0]
    a = [1, a1/a0, a2/a0]

    if len(audio.shape) > 1:
        result = np.zeros_like(audio)
        for ch in range(audio.shape[1]):
            result[:, ch] = signal.lfilter(b, a, audio[:, ch])
        return result
    else:
        return signal.lfilter(b, a, audio)

def soft_clipper(audio, threshold=0.95):
    """Soft clipper to prevent harsh clipping"""
    # Soft knee saturation
    mask = np.abs(audio) > threshold
    audio_clipped = np.copy(audio)

    # Apply soft saturation above threshold
    over = np.abs(audio[mask]) - threshold
    audio_clipped[mask] = np.sign(audio[mask]) * (threshold + np.tanh(over * 2) * (1 - threshold))

    return audio_clipped

def true_peak_limiter(audio, ceiling_db=-1.0, release_ms=100, sample_rate=48000):
    """True peak limiter with smooth release - ensures no peaks exceed ceiling"""
    ceiling = db_to_linear(ceiling_db)

    # Hard limit first - ensure nothing exceeds ceiling
    audio = np.clip(audio, -ceiling, ceiling)

    # Additional smoothing for transients
    release_samples = max(int(release_ms * sample_rate / 1000), 10)

    if len(audio.shape) > 1:
        # Stereo: find max peak across channels
        peak_envelope = np.max(np.abs(audio), axis=1)
    else:
        peak_envelope = np.abs(audio)

    # Smooth envelope for gain calculation
    smoothed_envelope = uniform_filter1d(peak_envelope, size=release_samples, mode='nearest')

    # Calculate gain reduction where needed
    gain_reduction = np.where(smoothed_envelope > ceiling * 0.95,
                              (ceiling * 0.95) / np.maximum(smoothed_envelope, 1e-10),
                              1.0)

    # Apply
    if len(audio.shape) > 1:
        result = audio * gain_reduction.reshape(-1, 1)
    else:
        result = audio * gain_reduction

    # Final hard clip to guarantee ceiling
    result = np.clip(result, -ceiling, ceiling)

    return result

def multiband_compress(audio, sample_rate, bands_config):
    """
    Simple multiband compression
    bands_config: list of (low_freq, high_freq, threshold_db, ratio, attack_ms, release_ms)
    """
    result = np.zeros_like(audio)

    for low, high, thresh_db, ratio, attack_ms, release_ms in bands_config:
        # Bandpass filter
        nyq = sample_rate / 2
        low_n = max(low / nyq, 0.001)
        high_n = min(high / nyq, 0.999)

        try:
            b, a = signal.butter(2, [low_n, high_n], btype='band')
        except:
            continue

        if len(audio.shape) > 1:
            band_audio = np.zeros_like(audio)
            for ch in range(audio.shape[1]):
                band_audio[:, ch] = signal.lfilter(b, a, audio[:, ch])
        else:
            band_audio = signal.lfilter(b, a, audio)

        # Simple compression
        threshold = db_to_linear(thresh_db)
        attack_samples = int(attack_ms * sample_rate / 1000)
        release_samples = int(release_ms * sample_rate / 1000)

        # Envelope follower
        envelope = np.abs(band_audio)
        if len(envelope.shape) > 1:
            envelope = np.max(envelope, axis=1)

        # Smooth envelope
        envelope = uniform_filter1d(envelope, size=attack_samples, mode='nearest')

        # Calculate gain
        gain = np.where(envelope > threshold,
                       (threshold / envelope) ** ((ratio - 1) / ratio),
                       1.0)

        # Smooth gain changes
        gain = uniform_filter1d(gain, size=release_samples, mode='nearest')

        # Apply
        if len(band_audio.shape) > 1:
            result += band_audio * gain.reshape(-1, 1)
        else:
            result += band_audio * gain

    return result

def stereo_balance_fix(audio, right_gain_db):
    """Fix stereo balance by adjusting one channel"""
    if len(audio.shape) < 2:
        return audio

    result = audio.copy()
    result[:, 1] *= db_to_linear(right_gain_db)
    return result

def normalize_to_lufs(audio, sample_rate, target_lufs):
    """Normalize audio to target LUFS"""
    current_lufs = calculate_lufs_simple(audio, sample_rate)
    gain_db = target_lufs - current_lufs
    gain = db_to_linear(gain_db)
    return audio * gain, gain_db

# =============================================================================
# MASTERING CHAIN
# =============================================================================

def apply_mastering_chain(audio, sample_rate, target_lufs, aggressive=False):
    """
    Full mastering chain based on expert recommendations
    """
    print(f"\n  Starting mastering chain (target: {target_lufs} LUFS)...")

    # 1. STEREO BALANCE FIX (from expert analysis: RIGHT is 0.83 dB quieter)
    print("    [1/8] Fixing stereo balance (+0.42 dB on RIGHT)...")
    audio = stereo_balance_fix(audio, +0.42)

    # 2. HIGH-PASS FILTER (remove sub-bass rumble below 25 Hz)
    print("    [2/8] High-pass filter (25 Hz)...")
    audio = high_pass_filter(audio, sample_rate, 25, order=4)

    # 3. CORRECTIVE EQ (problem frequencies from analysis)
    print("    [3/8] Corrective EQ (problem frequencies)...")

    # Critical resonances
    audio = parametric_eq_band(audio, sample_rate, 146, -3.5, 3.0)   # Low mud
    audio = parametric_eq_band(audio, sample_rate, 350, -2.0, 1.5)   # Low-mid mud
    audio = parametric_eq_band(audio, sample_rate, 1693, -3.0, 3.0)  # Mid harshness
    audio = parametric_eq_band(audio, sample_rate, 2244, -2.5, 3.0)  # High-mid resonance
    audio = parametric_eq_band(audio, sample_rate, 3545, -2.0, 2.5)  # Upper-mid
    audio = parametric_eq_band(audio, sample_rate, 7916, -1.5, 2.0)  # Sibilance

    # 4. ENHANCEMENT EQ
    print("    [4/8] Enhancement EQ...")
    audio = parametric_eq_band(audio, sample_rate, 40, +1.0, 0.7)    # Sub warmth
    audio = parametric_eq_band(audio, sample_rate, 3000, +1.5, 1.2)  # Presence
    audio = high_shelf(audio, sample_rate, 10000, +2.0)              # Air

    # 5. MULTIBAND COMPRESSION
    print("    [5/8] Multiband compression...")

    if aggressive:
        # Club/Loud version - more compression
        bands = [
            (20, 120, -18, 3.0, 15, 100),    # Low
            (120, 500, -15, 2.5, 10, 80),    # Low-mid
            (500, 2000, -12, 3.0, 5, 60),    # Mid
            (2000, 8000, -10, 2.0, 3, 40),   # High-mid
            (8000, 20000, -8, 2.0, 1, 30),   # High
        ]
    else:
        # Streaming version - gentle compression
        bands = [
            (20, 120, -20, 2.0, 20, 120),
            (120, 500, -18, 1.8, 15, 100),
            (500, 2000, -16, 1.5, 10, 80),
            (2000, 8000, -14, 1.5, 5, 60),
            (8000, 20000, -12, 1.5, 3, 50),
        ]

    compressed = multiband_compress(audio, sample_rate, bands)
    # Mix: 60% compressed, 40% original (parallel compression feel)
    audio = 0.6 * compressed + 0.4 * audio

    # 6. SOFT CLIPPER (before limiter)
    print("    [6/8] Soft clipper...")
    audio = soft_clipper(audio, threshold=0.92 if aggressive else 0.95)

    # 7. LOUDNESS NORMALIZATION
    print("    [7/8] Normalizing to target LUFS...")
    audio, gain_applied = normalize_to_lufs(audio, sample_rate, target_lufs)
    print(f"           Applied: {gain_applied:+.1f} dB")

    # 8. TRUE PEAK LIMITER
    ceiling = -0.5 if aggressive else -1.0
    print(f"    [8/8] True peak limiter (ceiling: {ceiling} dBTP)...")
    audio = true_peak_limiter(audio, ceiling_db=ceiling, release_ms=100, sample_rate=sample_rate)

    # Final check
    final_lufs = calculate_lufs_simple(audio, sample_rate)
    peak = linear_to_db(np.max(np.abs(audio)))
    print(f"\n  Final: {final_lufs:.1f} LUFS, Peak: {peak:.1f} dBTP")

    return audio

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("  ◉ САЙМУРР — СМОТРЕЛА")
    print("  PROFESSIONAL MASTERING")
    print("=" * 70)

    # Load audio
    print(f"\n  Loading: {INPUT_FILE}")
    sample_rate, audio = wav.read(INPUT_FILE)

    # Convert to float64 for processing
    if audio.dtype == np.int16:
        audio = audio.astype(np.float64) / 32768.0
    elif audio.dtype == np.int32:
        audio = audio.astype(np.float64) / 2147483648.0
    elif audio.dtype == np.float32:
        audio = audio.astype(np.float64)

    print(f"  Sample rate: {sample_rate} Hz")
    print(f"  Duration: {len(audio) / sample_rate:.2f}s")
    print(f"  Channels: {'Stereo' if len(audio.shape) > 1 else 'Mono'}")

    # Initial analysis
    initial_lufs = calculate_lufs_simple(audio, sample_rate)
    initial_peak = linear_to_db(np.max(np.abs(audio)))
    print(f"\n  Original: {initial_lufs:.1f} LUFS, Peak: {initial_peak:.1f} dBTP")

    # ==========================================================================
    # MASTER 1: STREAMING VERSION (-14 LUFS)
    # ==========================================================================
    print("\n" + "=" * 70)
    print("  MASTER 1: STREAMING VERSION (Spotify/YouTube/Apple)")
    print("=" * 70)

    streaming_audio = apply_mastering_chain(
        audio.copy(),
        sample_rate,
        TARGET_LUFS_STREAMING,
        aggressive=False
    )

    # Convert back to int24 for high quality
    streaming_int = np.clip(streaming_audio * 2147483648.0, -2147483648, 2147483647).astype(np.int32)
    wav.write(OUTPUT_STREAMING, sample_rate, streaming_int)
    print(f"\n  Saved: {OUTPUT_STREAMING}")
    print(f"  Size: {os.path.getsize(OUTPUT_STREAMING) / 1024 / 1024:.1f} MB")

    # ==========================================================================
    # MASTER 2: CLUB VERSION (-9 LUFS)
    # ==========================================================================
    print("\n" + "=" * 70)
    print("  MASTER 2: CLUB VERSION (DJ/Promo)")
    print("=" * 70)

    club_audio = apply_mastering_chain(
        audio.copy(),
        sample_rate,
        TARGET_LUFS_CLUB,
        aggressive=True
    )

    # Convert back to int24
    club_int = np.clip(club_audio * 2147483648.0, -2147483648, 2147483647).astype(np.int32)
    wav.write(OUTPUT_CLUB, sample_rate, club_int)
    print(f"\n  Saved: {OUTPUT_CLUB}")
    print(f"  Size: {os.path.getsize(OUTPUT_CLUB) / 1024 / 1024:.1f} MB")

    # ==========================================================================
    # SUMMARY
    # ==========================================================================
    print("\n" + "=" * 70)
    print("  ✓ MASTERING COMPLETE!")
    print("=" * 70)
    print(f"""
  DELIVERABLES:

  1. STREAMING MASTER: {OUTPUT_STREAMING}
     - Target: -14 LUFS (Spotify/YouTube/Apple Music)
     - True Peak: -1.0 dBTP
     - Optimized for normalization

  2. CLUB MASTER: {OUTPUT_CLUB}
     - Target: -9 LUFS (Maximum loudness)
     - True Peak: -0.5 dBTP
     - For DJ sets, club systems, promo

  MASTERING CHAIN APPLIED:
  ✓ Stereo balance correction (+0.42 dB RIGHT)
  ✓ High-pass filter (25 Hz)
  ✓ Corrective EQ (146, 350, 1693, 2244, 3545, 7916 Hz)
  ✓ Enhancement EQ (40 Hz warmth, 3kHz presence, 10kHz+ air)
  ✓ Multiband compression (5 bands)
  ✓ Soft clipper
  ✓ Loudness normalization
  ✓ True peak limiting
""")

if __name__ == "__main__":
    main()
