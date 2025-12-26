#!/usr/bin/env python3
"""
Spectral Visualization Tool
"""

import numpy as np
import scipy.io.wavfile as wavfile
from scipy import signal
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

def visualize_spectrum(audio_file):
    """Create comprehensive spectral visualizations"""

    # Read audio
    sample_rate, audio_data = wavfile.read(audio_file)

    # Convert to mono
    if len(audio_data.shape) > 1:
        audio_mono = np.mean(audio_data, axis=1)
    else:
        audio_mono = audio_data

    # Normalize
    if audio_data.dtype == np.int16:
        audio_mono = audio_mono.astype(np.float32) / 32768.0
    elif audio_data.dtype == np.int32:
        audio_mono = audio_mono.astype(np.float32) / 2147483648.0

    # Create figure with subplots
    fig = plt.figure(figsize=(20, 12))

    # 1. Full Spectrogram
    ax1 = plt.subplot(3, 2, 1)
    f, t, Sxx = signal.spectrogram(
        audio_mono,
        sample_rate,
        window='hann',
        nperseg=4096,
        noverlap=3072,
        scaling='density'
    )

    Sxx_db = 10 * np.log10(Sxx + 1e-10)
    im1 = ax1.pcolormesh(t, f, Sxx_db, shading='gouraud', cmap='inferno', vmin=-100, vmax=-40)
    ax1.set_ylabel('Frequency [Hz]')
    ax1.set_xlabel('Time [s]')
    ax1.set_title('Full Spectrogram', fontsize=14, fontweight='bold')
    ax1.set_ylim([20, 20000])
    ax1.set_yscale('log')
    plt.colorbar(im1, ax=ax1, label='Power [dB]')

    # 2. Average Spectrum
    ax2 = plt.subplot(3, 2, 2)
    spectrum_avg = np.mean(Sxx, axis=1)
    spectrum_db = 10 * np.log10(spectrum_avg + 1e-10)

    ax2.semilogx(f, spectrum_db, linewidth=2, color='#00ff41', label='Average Spectrum')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_ylabel('Level [dB]')
    ax2.set_title('Average Frequency Response', fontsize=14, fontweight='bold')
    ax2.set_xlim([20, 20000])
    ax2.set_ylim([spectrum_db.min() - 5, spectrum_db.max() + 5])

    # Mark frequency bands
    bands = [60, 250, 500, 2000, 6000, 12000]
    band_names = ['Bass', 'Low-mid', 'Mid', 'High-mid', 'High', 'Air']
    for band, name in zip(bands, band_names):
        ax2.axvline(band, color='red', linestyle='--', alpha=0.5, linewidth=1)
        ax2.text(band, ax2.get_ylim()[1], f' {name}', rotation=0, va='top', fontsize=8)

    ax2.legend()

    # 3. Low Frequency Detail (20-500 Hz)
    ax3 = plt.subplot(3, 2, 3)
    low_freq_mask = (f >= 20) & (f <= 500)
    ax3.plot(f[low_freq_mask], spectrum_db[low_freq_mask], linewidth=2, color='#ff6b35')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlabel('Frequency [Hz]')
    ax3.set_ylabel('Level [dB]')
    ax3.set_title('Low Frequency Detail (20-500 Hz)', fontsize=14, fontweight='bold')
    ax3.set_xlim([20, 500])

    # 4. Mid Frequency Detail (500-6000 Hz)
    ax4 = plt.subplot(3, 2, 4)
    mid_freq_mask = (f >= 500) & (f <= 6000)
    ax4.plot(f[mid_freq_mask], spectrum_db[mid_freq_mask], linewidth=2, color='#4ecdc4')
    ax4.grid(True, alpha=0.3)
    ax4.set_xlabel('Frequency [Hz]')
    ax4.set_ylabel('Level [dB]')
    ax4.set_title('Mid Frequency Detail (500-6000 Hz)', fontsize=14, fontweight='bold')
    ax4.set_xlim([500, 6000])

    # 5. High Frequency Detail (6-20 kHz)
    ax5 = plt.subplot(3, 2, 5)
    high_freq_mask = (f >= 6000) & (f <= 20000)
    ax5.plot(f[high_freq_mask], spectrum_db[high_freq_mask], linewidth=2, color='#c44569')
    ax5.grid(True, alpha=0.3)
    ax5.set_xlabel('Frequency [Hz]')
    ax5.set_ylabel('Level [dB]')
    ax5.set_title('High Frequency Detail (6-20 kHz)', fontsize=14, fontweight='bold')
    ax5.set_xlim([6000, 20000])

    # 6. Band Energy Distribution
    ax6 = plt.subplot(3, 2, 6)
    bands_def = {
        'Sub\n20-60': (20, 60),
        'Bass\n60-250': (60, 250),
        'Low-mid\n250-500': (250, 500),
        'Mid\n500-2k': (500, 2000),
        'High-mid\n2-6k': (2000, 6000),
        'High\n6-12k': (6000, 12000),
        'Air\n12-20k': (12000, 20000)
    }

    band_energies = []
    band_labels = []

    for label, (low, high) in bands_def.items():
        mask = (f >= low) & (f <= high)
        if np.any(mask):
            energy = np.mean(spectrum_db[mask])
            band_energies.append(energy)
            band_labels.append(label)

    colors = ['#8e44ad', '#3498db', '#1abc9c', '#2ecc71', '#f39c12', '#e74c3c', '#c0392b']
    bars = ax6.bar(range(len(band_energies)), band_energies, color=colors, edgecolor='black', linewidth=1.5)
    ax6.set_xticks(range(len(band_labels)))
    ax6.set_xticklabels(band_labels, rotation=45, ha='right')
    ax6.set_ylabel('Average Level [dB]')
    ax6.set_title('Frequency Band Energy Distribution', fontsize=14, fontweight='bold')
    ax6.grid(True, alpha=0.3, axis='y')
    ax6.axhline(y=-30, color='green', linestyle='--', alpha=0.7, label='Reference Level')
    ax6.legend()

    # Add value labels on bars
    for i, (bar, energy) in enumerate(zip(bars, band_energies)):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'{energy:.1f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()

    # Save
    output_path = Path(audio_file).with_suffix('.spectrum_analysis.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n✓ Spectral visualization saved to: {output_path}")

    plt.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python visualize_spectrum.py <audio_file.wav>")
        sys.exit(1)

    visualize_spectrum(sys.argv[1])
