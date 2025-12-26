#!/usr/bin/env python3
"""
Visual Dynamics Profile Generator
"""

import numpy as np
from scipy.io import wavfile
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

def create_ascii_waveform(filepath, width=120, height=20):
    """Create ASCII art representation of waveform and energy"""

    sr, audio = wavfile.read(filepath)

    # Convert to mono
    if len(audio.shape) > 1:
        mono = np.mean(audio, axis=1)
    else:
        mono = audio

    # Normalize
    mono = mono.astype(np.float64)
    if mono.max() > 1.0:
        mono = mono / np.abs(mono).max()

    duration = len(mono) / sr

    # Calculate energy in windows
    samples_per_col = len(mono) // width
    energy = []
    rms_values = []

    for i in range(width):
        start = i * samples_per_col
        end = start + samples_per_col
        if end <= len(mono):
            segment = mono[start:end]
            # RMS
            rms = np.sqrt(np.mean(segment**2))
            rms_db = 20 * np.log10(np.maximum(rms, 1e-10))
            rms_values.append(rms_db)
            # Peak
            peak = np.max(np.abs(segment))
            energy.append(peak)

    energy = np.array(energy)
    rms_values = np.array(rms_values)

    # Normalize for display
    if len(energy) > 0 and energy.max() > 0:
        energy_norm = energy / energy.max()
    else:
        energy_norm = energy

    # Create ASCII waveform
    print("\n" + "=" * width)
    print("ENERGY PROFILE VISUALIZATION")
    print("=" * width)

    # Draw waveform
    for row in range(height-1, -1, -1):
        line = ""
        threshold = row / height
        for col in range(len(energy_norm)):
            if energy_norm[col] >= threshold:
                # Different characters for different intensities
                if energy_norm[col] > 0.8:
                    line += "█"
                elif energy_norm[col] > 0.6:
                    line += "▓"
                elif energy_norm[col] > 0.4:
                    line += "▒"
                elif energy_norm[col] > 0.2:
                    line += "░"
                else:
                    line += "·"
            else:
                line += " "

        # Add scale
        if row == height - 1:
            print(f"0dB  │{line}│")
        elif row == height // 2:
            print(f"-20dB│{line}│")
        elif row == 0:
            print(f"-40dB│{line}│")
        else:
            print(f"     │{line}│")

    # Time axis
    print(f"     └{'─' * width}┘")

    # Time markers
    time_markers = "     "
    time_step = duration / 10
    for i in range(11):
        time = i * time_step
        marker = f"{time:.0f}s"
        time_markers += marker + " " * (width // 10 - len(marker))
    print(time_markers[:width + 5])

    print()

    # RMS profile
    print("=" * width)
    print("RMS LOUDNESS PROFILE")
    print("=" * width)

    # Find min/max for scaling
    rms_min = rms_values.min()
    rms_max = rms_values.max()
    rms_range = rms_max - rms_min

    if rms_range > 0:
        rms_norm = (rms_values - rms_min) / rms_range
    else:
        rms_norm = np.zeros_like(rms_values)

    for row in range(height-1, -1, -1):
        line = ""
        threshold = row / height
        for col in range(len(rms_norm)):
            if rms_norm[col] >= threshold:
                if rms_norm[col] > 0.8:
                    line += "█"
                elif rms_norm[col] > 0.6:
                    line += "▓"
                elif rms_norm[col] > 0.4:
                    line += "▒"
                else:
                    line += "░"
            else:
                line += " "

        # Add RMS scale
        rms_at_row = rms_min + (row / height) * rms_range
        if row == height - 1:
            print(f"{rms_at_row:>5.1f}│{line}│")
        elif row == height // 2:
            print(f"{rms_at_row:>5.1f}│{line}│")
        elif row == 0:
            print(f"{rms_at_row:>5.1f}│{line}│")
        else:
            print(f"     │{line}│")

    print(f"     └{'─' * width}┘")
    print(time_markers[:width + 5])
    print()

    # Section markers
    print("=" * width)
    print("STRUCTURAL SECTIONS")
    print("=" * width)

    sections = [
        {'name': 'Intro', 'start': 0, 'end': 17.02},
        {'name': 'Verse 1', 'start': 17.02, 'end': 27.71},
        {'name': 'Pre-Chorus 1', 'start': 27.71, 'end': 38.11},
        {'name': 'Chorus 1', 'start': 38.11, 'end': 42.20},
        {'name': 'Verse 2', 'start': 42.20, 'end': 46.69},
        {'name': 'Pre-Chorus 2', 'start': 46.69, 'end': 51.33},
        {'name': 'Chorus 2', 'start': 51.33, 'end': 55.36},
        {'name': 'Bridge', 'start': 55.36, 'end': 61.74},
        {'name': 'Chorus 3', 'start': 61.74, 'end': 81.59},
        {'name': 'Outro', 'start': 81.59, 'end': 84.72}
    ]

    # Create timeline
    timeline = [' '] * width
    labels = [''] * width

    for section in sections:
        start_col = int((section['start'] / duration) * width)
        end_col = int((section['end'] / duration) * width)

        # Mark boundaries
        if start_col < width:
            timeline[start_col] = '│'

        # Add label
        label = section['name']
        mid_col = (start_col + end_col) // 2
        label_start = max(0, mid_col - len(label)//2)
        label_end = min(width, label_start + len(label))

        if label_start < width:
            for i, char in enumerate(label[:label_end - label_start]):
                if label_start + i < width:
                    labels[label_start + i] = char

    print('     ' + ''.join(timeline))
    print('     ' + ''.join(labels))
    print()

    # Dynamic range summary
    print("=" * width)
    print("QUICK DYNAMICS SUMMARY")
    print("=" * width)
    print()

    # Calculate overall stats
    overall_rms = 20 * np.log10(np.maximum(np.sqrt(np.mean(mono**2)), 1e-10))
    overall_peak = 20 * np.log10(np.maximum(np.max(np.abs(mono)), 1e-10))
    crest_factor = overall_peak - overall_rms

    print(f"Overall RMS:      {overall_rms:>7.2f} dB")
    print(f"Peak Level:       {overall_peak:>7.2f} dB")
    print(f"Crest Factor:     {crest_factor:>7.2f} dB")
    print(f"Headroom:         {0 - overall_peak:>7.2f} dB")
    print()

    # Sections with highest/lowest energy
    section_energies = []
    for section in sections:
        start_sample = int(section['start'] * sr)
        end_sample = int(section['end'] * sr)
        segment = mono[start_sample:end_sample]

        if len(segment) > 0:
            rms = np.sqrt(np.mean(segment**2))
            rms_db = 20 * np.log10(np.maximum(rms, 1e-10))
            section_energies.append((section['name'], rms_db))

    section_energies.sort(key=lambda x: x[1], reverse=True)

    print("LOUDEST SECTIONS:")
    for i, (name, rms) in enumerate(section_energies[:3], 1):
        print(f"  {i}. {name:<20} {rms:>7.2f} dB RMS")

    print()
    print("QUIETEST SECTIONS:")
    for i, (name, rms) in enumerate(reversed(section_energies[-3:]), 1):
        print(f"  {i}. {name:<20} {rms:>7.2f} dB RMS")

    print()
    print("=" * width)


if __name__ == "__main__":
    create_ascii_waveform('/home/user/look-at-me/SmotrelaА.wav')
