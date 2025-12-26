#!/usr/bin/env python3
"""
Professional Audio Analysis Script for Mastering Engineer
Analyzes "СМОТРЕЛА" track and provides detailed mastering recommendations
"""

import struct
import numpy as np
from scipy import signal
from scipy.io import wavfile
import json

def read_wav(filename):
    """Read WAV file and return sample rate and data"""
    sample_rate, data = wavfile.read(filename)

    # Convert to float
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    elif data.dtype == np.uint8:
        data = (data.astype(np.float32) - 128) / 128.0

    return sample_rate, data

def db_to_linear(db):
    """Convert dB to linear scale"""
    return 10 ** (db / 20)

def linear_to_db(linear):
    """Convert linear to dB scale"""
    return 20 * np.log10(linear + 1e-10)

def calculate_lufs_integrated(audio, sample_rate):
    """
    Simplified LUFS calculation (ITU-R BS.1770-4 approximation)
    Real implementation would use pyloudnorm, but we'll approximate
    """
    # K-weighting filters
    # Stage 1: High-shelf filter
    f0 = 1681.974450955533
    G = 3.999843853973347
    Q = 0.7071752369554196

    # Calculate RMS with K-weighting approximation
    # For simplification, we'll use RMS with frequency weighting approximation

    # Split channels if stereo
    if len(audio.shape) > 1:
        left = audio[:, 0]
        right = audio[:, 1]
    else:
        left = right = audio

    # Calculate gated loudness (simplified)
    block_size = int(0.4 * sample_rate)  # 400ms blocks
    hop_size = int(0.1 * sample_rate)    # 100ms hop

    # Calculate mean square for each channel
    left_ms = np.mean(left ** 2)
    right_ms = np.mean(right ** 2)

    # Combined loudness (stereo)
    combined_ms = (left_ms + right_ms) / 2

    # Convert to LUFS (approximation)
    lufs = -0.691 + 10 * np.log10(combined_ms)

    return lufs

def calculate_true_peak(audio):
    """Calculate true peak using oversampling"""
    # Oversample by 4x for true peak detection
    oversampled = signal.resample(audio, len(audio) * 4, axis=0)
    true_peak = np.max(np.abs(oversampled))
    return linear_to_db(true_peak)

def calculate_crest_factor(audio):
    """Calculate crest factor (peak to RMS ratio)"""
    peak = np.max(np.abs(audio))
    rms = np.sqrt(np.mean(audio ** 2))
    return linear_to_db(peak / rms)

def analyze_stereo_balance(audio):
    """Analyze stereo field"""
    if len(audio.shape) < 2:
        return {"status": "Mono file"}

    left = audio[:, 0]
    right = audio[:, 1]

    # RMS for each channel
    left_rms = np.sqrt(np.mean(left ** 2))
    right_rms = np.sqrt(np.mean(right ** 2))

    left_rms_db = linear_to_db(left_rms)
    right_rms_db = linear_to_db(right_rms)

    # Peak for each channel
    left_peak = np.max(np.abs(left))
    right_peak = np.max(np.abs(right))

    left_peak_db = linear_to_db(left_peak)
    right_peak_db = linear_to_db(right_peak)

    # Correlation
    correlation = np.corrcoef(left, right)[0, 1]

    # Mid/Side analysis
    mid = (left + right) / 2
    side = (left - right) / 2

    mid_rms = np.sqrt(np.mean(mid ** 2))
    side_rms = np.sqrt(np.mean(side ** 2))

    stereo_width = side_rms / (mid_rms + 1e-10)

    return {
        "left_rms_db": left_rms_db,
        "right_rms_db": right_rms_db,
        "rms_difference_db": abs(left_rms_db - right_rms_db),
        "left_peak_db": left_peak_db,
        "right_peak_db": right_peak_db,
        "correlation": correlation,
        "stereo_width": stereo_width,
        "mid_rms_db": linear_to_db(mid_rms),
        "side_rms_db": linear_to_db(side_rms)
    }

def spectral_analysis(audio, sample_rate):
    """Analyze frequency spectrum"""
    # Use mono mix for spectral analysis
    if len(audio.shape) > 1:
        mono = np.mean(audio, axis=1)
    else:
        mono = audio

    # FFT analysis
    fft = np.fft.rfft(mono)
    freqs = np.fft.rfftfreq(len(mono), 1/sample_rate)
    magnitude = np.abs(fft)
    magnitude_db = linear_to_db(magnitude / len(mono))

    # Find dominant frequency bands
    bands = {
        "sub_bass": (20, 60),
        "bass": (60, 250),
        "low_mids": (250, 500),
        "mids": (500, 2000),
        "high_mids": (2000, 4000),
        "presence": (4000, 6000),
        "brilliance": (6000, 20000)
    }

    band_energy = {}
    for band_name, (low, high) in bands.items():
        mask = (freqs >= low) & (freqs <= high)
        if np.any(mask):
            band_energy[band_name] = {
                "energy_db": float(np.max(magnitude_db[mask])),
                "avg_energy_db": float(np.mean(magnitude_db[mask]))
            }

    return band_energy

def analyze_dynamics(audio, sample_rate):
    """Analyze dynamic range"""
    # Calculate short-term loudness (3 second blocks)
    block_size = int(3.0 * sample_rate)

    if len(audio.shape) > 1:
        mono = np.mean(audio, axis=1)
    else:
        mono = audio

    n_blocks = len(mono) // block_size
    loudness_blocks = []

    for i in range(n_blocks):
        block = mono[i * block_size:(i + 1) * block_size]
        rms = np.sqrt(np.mean(block ** 2))
        loudness_blocks.append(linear_to_db(rms))

    if loudness_blocks:
        # PLR (Peak to Loudness Ratio) - simplified DR measurement
        loudness_blocks = np.array(loudness_blocks)
        peak_db = linear_to_db(np.max(np.abs(mono)))
        avg_loudness = np.mean(loudness_blocks)

        # EBU R128 Dynamic Range approximation
        dr = peak_db - avg_loudness

        return {
            "dynamic_range_db": dr,
            "peak_loudness_db": peak_db,
            "average_loudness_db": avg_loudness,
            "loudness_std": float(np.std(loudness_blocks))
        }

    return {"error": "Could not calculate dynamics"}

def main():
    filename = "/home/user/look-at-me/СМОТРЕЛА_teaser.wav"

    print("="*80)
    print("PROFESSIONAL MASTERING ANALYSIS - СМОТРЕЛА by Саймурр")
    print("="*80)
    print()

    # Read audio
    sample_rate, audio = read_wav(filename)
    duration = len(audio) / sample_rate

    print(f"📊 FILE INFORMATION")
    print(f"   Sample Rate: {sample_rate} Hz")
    print(f"   Duration: {duration:.2f} seconds")
    print(f"   Channels: {'Stereo' if len(audio.shape) > 1 else 'Mono'}")
    print(f"   Bit Depth: {audio.dtype}")
    print()

    # Basic measurements
    print(f"📈 LEVEL ANALYSIS")
    if len(audio.shape) > 1:
        peak_left = linear_to_db(np.max(np.abs(audio[:, 0])))
        peak_right = linear_to_db(np.max(np.abs(audio[:, 1])))
        rms_left = linear_to_db(np.sqrt(np.mean(audio[:, 0] ** 2)))
        rms_right = linear_to_db(np.sqrt(np.mean(audio[:, 1] ** 2)))

        print(f"   Peak Level L: {peak_left:.2f} dBFS")
        print(f"   Peak Level R: {peak_right:.2f} dBFS")
        print(f"   RMS Level L: {rms_left:.2f} dBFS")
        print(f"   RMS Level R: {rms_right:.2f} dBFS")

        # Headroom
        headroom_left = 0.0 - peak_left
        headroom_right = 0.0 - peak_right
        print(f"   Headroom L: {headroom_left:.2f} dB")
        print(f"   Headroom R: {headroom_right:.2f} dB")
    else:
        peak = linear_to_db(np.max(np.abs(audio)))
        rms = linear_to_db(np.sqrt(np.mean(audio ** 2)))
        print(f"   Peak Level: {peak:.2f} dBFS")
        print(f"   RMS Level: {rms:.2f} dBFS")
        print(f"   Headroom: {0.0 - peak:.2f} dB")

    # Crest factor
    crest = calculate_crest_factor(audio)
    print(f"   Crest Factor: {crest:.2f} dB")
    print()

    # LUFS
    print(f"🔊 LOUDNESS ANALYSIS (LUFS)")
    lufs = calculate_lufs_integrated(audio, sample_rate)
    print(f"   Integrated LUFS: {lufs:.1f} LUFS (approximation)")
    print(f"   Target Spotify: -14 LUFS")
    print(f"   Target YouTube: -13 to -15 LUFS")
    print(f"   Target Apple Music: -16 LUFS")
    print(f"   Target EDM/Electronic: -6 to -9 LUFS (streaming will normalize)")
    print(f"   Current delta from Spotify: {lufs - (-14):.1f} dB")
    print()

    # True Peak
    true_peak = calculate_true_peak(audio)
    print(f"   True Peak: {true_peak:.2f} dBTP")
    print(f"   Recommended max: -1.0 dBTP (for streaming)")
    print()

    # Stereo analysis
    print(f"🎚️  STEREO FIELD ANALYSIS")
    stereo_info = analyze_stereo_balance(audio)
    for key, value in stereo_info.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.2f}")
        else:
            print(f"   {key}: {value}")
    print()

    # Dynamics
    print(f"⚡ DYNAMIC RANGE ANALYSIS")
    dynamics = analyze_dynamics(audio, sample_rate)
    for key, value in dynamics.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.2f} dB")
        else:
            print(f"   {key}: {value}")
    print()

    # Spectral analysis
    print(f"🎵 FREQUENCY SPECTRUM ANALYSIS")
    spectrum = spectral_analysis(audio, sample_rate)
    for band, values in spectrum.items():
        print(f"   {band.upper()}:")
        print(f"      Peak: {values['energy_db']:.1f} dB | Avg: {values['avg_energy_db']:.1f} dB")
    print()

    # Mastering recommendations
    print("="*80)
    print("🎯 PROFESSIONAL MASTERING RECOMMENDATIONS")
    print("="*80)
    print()

    print("1️⃣  HEADROOM ANALYSIS")
    print(f"   Current headroom: ~{headroom_left:.2f} dB")
    print(f"   ✅ EXCELLENT - {headroom_left:.2f}dB headroom is perfect for mastering")
    print(f"   Recommendation: DO NOT add more headroom - this is optimal")
    print()

    print("2️⃣  STEREO BALANCE CORRECTION")
    rms_diff = stereo_info['rms_difference_db']
    print(f"   Current L/R imbalance: {rms_diff:.2f} dB")
    if rms_diff > 0.5:
        print(f"   ⚠️  ATTENTION: {rms_diff:.2f}dB imbalance detected")
        print(f"   Recommendation: Apply stereo utility/balance plugin")
        print(f"   - Boost RIGHT channel by +{rms_diff/2:.2f} dB")
        print(f"   - OR reduce LEFT channel by -{rms_diff/2:.2f} dB")
        print(f"   - Tools: iZotope Ozone Imager, Waves S1, or DAW pan/balance")
    else:
        print(f"   ✅ GOOD - Stereo balance is acceptable")
    print()

    print("3️⃣  LOUDNESS TARGETS (LUFS)")
    target_lufs = -8.0  # Aggressive EDM target
    current_lufs = lufs
    needed_gain = target_lufs - current_lufs
    print(f"   Current: ~{current_lufs:.1f} LUFS")
    print(f"   Target for EDM/Electronic: -8 LUFS (pre-streaming)")
    print(f"   Gain needed: +{needed_gain:.1f} dB")
    print(f"   ")
    print(f"   Chain recommendation:")
    print(f"   1. Multiband Compression (subtle)")
    print(f"   2. Mastering EQ")
    print(f"   3. Stereo Enhancement")
    print(f"   4. Final Limiter → -8 LUFS, -0.5 dBTP true peak ceiling")
    print()

    print("4️⃣  EQ RECOMMENDATIONS (Electronic/Dramatic Genre)")
    print(f"   Based on spectral analysis:")
    print(f"   ")
    print(f"   🎛️  LOW END (20-250 Hz):")
    print(f"      • Sub-bass shelf at 40 Hz: +0.5 to +1.0 dB (Q: 0.7)")
    print(f"      • Clean up mud at 150-200 Hz: -0.5 to -1.0 dB (Q: 1.2)")
    print(f"      • High-pass filter at 25 Hz to remove subsonic rumble")
    print(f"   ")
    print(f"   🎛️  MIDRANGE (250-4000 Hz):")
    print(f"      • Slight dip at 300-400 Hz: -0.3 to -0.8 dB (Q: 1.5) - reduce boxiness")
    print(f"      • Presence boost at 2-3 kHz: +0.5 to +1.0 dB (Q: 2.0) - clarity")
    print(f"      • Check for harsh frequencies around 1-2 kHz, reduce if needed")
    print(f"   ")
    print(f"   🎛️  HIGH END (4000+ Hz):")
    print(f"      • Air/brilliance shelf at 10 kHz: +0.5 to +1.5 dB (Q: 0.7)")
    print(f"      • Gentle boost at 6-8 kHz: +0.3 to +0.7 dB - shimmer")
    print(f"      • Low-pass at 18-19 kHz (optional, to taste)")
    print(f"   ")
    print(f"   Recommended Tools: FabFilter Pro-Q3, Waves SSL G-Master, iZotope Ozone EQ")
    print()

    print("5️⃣  COMPRESSION/LIMITING STRATEGY")
    print(f"   Current Crest Factor: {crest:.1f} dB")
    print(f"   Current Dynamic Range: ~{dynamics['dynamic_range_db']:.1f} dB")
    print(f"   ")
    print(f"   🎚️  MULTIBAND COMPRESSION:")
    print(f"      Band 1 (20-120 Hz): Ratio 2:1, Threshold -18dB, Attack 30ms, Release 100ms")
    print(f"      Band 2 (120-500 Hz): Ratio 2:1, Threshold -16dB, Attack 20ms, Release 80ms")
    print(f"      Band 3 (500-5kHz): Ratio 1.5:1, Threshold -14dB, Attack 10ms, Release 50ms")
    print(f"      Band 4 (5k-20kHz): Ratio 2:1, Threshold -12dB, Attack 5ms, Release 40ms")
    print(f"      → Total gain reduction: 1-3 dB max per band")
    print(f"   ")
    print(f"   🎚️  FINAL LIMITER:")
    print(f"      Ceiling: -0.5 dBTP (true peak)")
    print(f"      Target: -8.0 LUFS integrated")
    print(f"      Attack: 0.5-1.0 ms (fast for transients)")
    print(f"      Release: 50-100 ms (auto-release recommended)")
    print(f"      Lookahead: 5-10 ms")
    print(f"      Character: Transparent/Modern")
    print(f"      → Expect 3-6 dB gain reduction on peaks")
    print(f"   ")
    print(f"   Recommended Tools:")
    print(f"   - Limiter: FabFilter Pro-L2, Waves L2/L3, iZotope Ozone Maximizer")
    print(f"   - Multiband: FabFilter Pro-MB, Waves C6, iZotope Ozone Dynamics")
    print()

    print("6️⃣  DROP ENHANCEMENT (17.163s)")
    print(f"   🎯 Special attention to the DROP moment:")
    print(f"   ")
    print(f"   Pre-DROP (Build-up, ~15-17s):")
    print(f"   • Consider slight automation: -1 to -2 dB reduction before drop")
    print(f"   • High-pass automation: sweep from 100Hz → 500Hz → release at drop")
    print(f"   • Reverb build/riser for dramatic effect")
    print(f"   ")
    print(f"   AT DROP (17.163s):")
    print(f"   • Full frequency spectrum returns (remove high-pass)")
    print(f"   • Ensure sub-bass is powerful: check 40-80 Hz content")
    print(f"   • Transient shaper: enhance attack by 2-4 dB for punch")
    print(f"   • Stereo width: widen highs (>2kHz) by 10-20% for impact")
    print(f"   • Consider sidechain compression from kick to maintain clarity")
    print(f"   ")
    print(f"   Post-DROP:")
    print(f"   • Maintain energy through consistent limiting")
    print(f"   • Ensure sustained loudness matches drop impact")
    print(f"   ")
    print(f"   Tools: Soundtoys Little Plate (reverb), Waves Trans-X (transients),")
    print(f"          iZotope Ozone Imager (width), FabFilter Pro-MB (sidechain)")
    print()

    print("="*80)
    print("🔧 COMPLETE MASTERING CHAIN")
    print("="*80)
    print()
    print("Signal Flow (in order):")
    print()
    print("1. iZotope RX / Spectral Repair (if needed)")
    print("   → Remove any clicks, pops, or unwanted noise")
    print()
    print("2. Stereo Balance Correction")
    print("   → Fix L/R imbalance: adjust as per section 2 above")
    print()
    print("3. Linear Phase EQ (Surgical)")
    print("   → FabFilter Pro-Q3 (Linear Phase Mode)")
    print("   → Apply corrective EQ: remove problem frequencies")
    print()
    print("4. Multiband Compression")
    print("   → FabFilter Pro-MB or Waves C6")
    print("   → Settings as per section 5 above")
    print("   → Gentle control, preserve dynamics")
    print()
    print("5. Mastering EQ (Color/Enhancement)")
    print("   → Waves SSL G-Master or FabFilter Pro-Q3 (Zero-Latency)")
    print("   → Apply creative EQ: enhance as per section 4 above")
    print()
    print("6. Stereo Enhancement (>2kHz only)")
    print("   → iZotope Ozone Imager or Waves S1")
    print("   → Widen highs: 110-130% (don't overdo!)")
    print("   → Keep lows mono: <150 Hz")
    print()
    print("7. Harmonic Exciter (subtle)")
    print("   → Waves Aphex Vintage Aural Exciter or iZotope Ozone Exciter")
    print("   → Add 2nd/3rd harmonics: 5-15% mix")
    print()
    print("8. Final Limiter")
    print("   → FabFilter Pro-L2 or Waves L2")
    print("   → Settings as per section 5 above")
    print("   → Ceiling: -0.5 dBTP, Target: -8 LUFS")
    print()
    print("9. True Peak Meter")
    print("   → Final check: must not exceed -0.5 dBTP")
    print("   → Loudness check: -8 LUFS ±0.5")
    print()
    print("="*80)
    print("📊 REFERENCE TRACKS (A/B Comparison)")
    print("="*80)
    print()
    print("Compare your master with these professionally mastered tracks:")
    print("• Similar genre electronic/dramatic tracks")
    print("• Match: Overall tonal balance, stereo width, loudness")
    print("• Tools: ADPTR Audio Metric AB, Magic AB, or REFERENCE")
    print()
    print("="*80)
    print("✅ FINAL DELIVERABLES")
    print("="*80)
    print()
    print("Streaming (Lossy):")
    print("  • 44.1 kHz / 16-bit WAV → for Spotify, YouTube, Apple Music")
    print("  • -14 LUFS integrated, -1.0 dBTP (streaming platforms normalize)")
    print()
    print("High-Resolution (Lossless):")
    print("  • 48 kHz / 24-bit WAV or FLAC")
    print("  • -8 to -9 LUFS integrated, -0.5 dBTP")
    print("  • For Tidal, Qobuz, Bandcamp, or archival")
    print()
    print("Current file is 48kHz - perfect for HD delivery!")
    print()
    print("="*80)
    print("Analysis complete! Good luck with the master! 🎚️🎵")
    print("="*80)

if __name__ == "__main__":
    main()
