#!/usr/bin/env python3
"""
Frequency Spectrum Visualization for "СМОТРЕЛА"
"""

import numpy as np
import scipy.io.wavfile as wavfile
from scipy import signal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def analyze_audio_visual(file_path, drop_time=17.163):
    """Create visualizations"""

    # Load audio
    sample_rate, data = wavfile.read(file_path)

    if len(data.shape) > 1:
        audio_mono = np.mean(data, axis=1)
    else:
        audio_mono = data

    audio_mono = audio_mono.astype(np.float64)
    audio_mono = audio_mono / np.max(np.abs(audio_mono))

    duration = len(audio_mono) / sample_rate

    # Split audio
    drop_sample = int(drop_time * sample_rate)
    audio_before = audio_mono[:drop_sample]
    audio_after = audio_mono[drop_sample:]

    # Compute spectra
    freqs_full, psd_full = signal.welch(audio_mono, sample_rate, nperseg=8192, noverlap=4096)
    freqs_before, psd_before = signal.welch(audio_before, sample_rate, nperseg=8192, noverlap=4096)
    freqs_after, psd_after = signal.welch(audio_after, sample_rate, nperseg=8192, noverlap=4096)

    spectrum_full = 10 * np.log10(psd_full + 1e-10)
    spectrum_before = 10 * np.log10(psd_before + 1e-10)
    spectrum_after = 10 * np.log10(psd_after + 1e-10)

    # Create figure with multiple subplots
    fig = plt.figure(figsize=(20, 14))

    # 1. Full spectrum
    ax1 = plt.subplot(3, 2, 1)
    ax1.semilogx(freqs_full, spectrum_full, linewidth=1.5, color='#00ff00', alpha=0.8)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('Frequency (Hz)', fontsize=10)
    ax1.set_ylabel('Magnitude (dB)', fontsize=10)
    ax1.set_title('Full Track - Frequency Spectrum', fontsize=12, fontweight='bold')
    ax1.set_xlim([20, 20000])

    # Add frequency band markers
    bands = [(20, 60, 'Sub'), (60, 250, 'Bass'), (250, 500, 'L-Mid'),
             (500, 2000, 'Mid'), (2000, 4000, 'H-Mid'), (4000, 10000, 'High'),
             (10000, 20000, 'Air')]

    for low, high, name in bands:
        ax1.axvspan(low, high, alpha=0.1, color=np.random.rand(3,))
        mid = (low + high) / 2
        ax1.text(mid, ax1.get_ylim()[1] - 5, name, ha='center', fontsize=8, alpha=0.7)

    # 2. Before vs After DROP comparison
    ax2 = plt.subplot(3, 2, 2)
    ax2.semilogx(freqs_before, spectrum_before, linewidth=1.5, color='#ff6b6b', alpha=0.7, label='Before DROP')
    ax2.semilogx(freqs_after, spectrum_after, linewidth=1.5, color='#4ecdc4', alpha=0.7, label='After DROP')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('Frequency (Hz)', fontsize=10)
    ax2.set_ylabel('Magnitude (dB)', fontsize=10)
    ax2.set_title('Before vs After DROP Comparison', fontsize=12, fontweight='bold')
    ax2.set_xlim([20, 20000])
    ax2.legend(fontsize=9)

    # 3. Difference spectrum
    ax3 = plt.subplot(3, 2, 3)
    # Interpolate to match frequency bins
    spectrum_diff = spectrum_after - spectrum_before
    ax3.semilogx(freqs_after, spectrum_diff, linewidth=1.5, color='#ffd93d', alpha=0.8)
    ax3.axhline(y=0, color='white', linestyle='--', alpha=0.5)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlabel('Frequency (Hz)', fontsize=10)
    ax3.set_ylabel('Difference (dB)', fontsize=10)
    ax3.set_title('DROP Energy Change (After - Before)', fontsize=12, fontweight='bold')
    ax3.set_xlim([20, 20000])
    ax3.fill_between(freqs_after, 0, spectrum_diff, where=(spectrum_diff > 0), alpha=0.3, color='green')
    ax3.fill_between(freqs_after, 0, spectrum_diff, where=(spectrum_diff < 0), alpha=0.3, color='red')

    # 4. Frequency bands bar chart
    ax4 = plt.subplot(3, 2, 4)
    band_names = ['Sub-bass', 'Bass', 'Low-mids', 'Mids', 'High-mids', 'Highs', 'Air']
    band_ranges = [(20, 60), (60, 250), (250, 500), (500, 2000), (2000, 4000), (4000, 10000), (10000, 20000)]

    before_levels = []
    after_levels = []

    for low, high in band_ranges:
        mask = (freqs_before >= low) & (freqs_before < high)
        before_levels.append(np.mean(spectrum_before[mask]))

        mask = (freqs_after >= low) & (freqs_after < high)
        after_levels.append(np.mean(spectrum_after[mask]))

    x = np.arange(len(band_names))
    width = 0.35

    bars1 = ax4.bar(x - width/2, before_levels, width, label='Before DROP', color='#ff6b6b', alpha=0.7)
    bars2 = ax4.bar(x + width/2, after_levels, width, label='After DROP', color='#4ecdc4', alpha=0.7)

    ax4.set_ylabel('Average Level (dB)', fontsize=10)
    ax4.set_title('Frequency Bands Energy Comparison', fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(band_names, rotation=45, ha='right')
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3, axis='y')

    # 5. Spectrogram
    ax5 = plt.subplot(3, 2, 5)
    f, t, Sxx = signal.spectrogram(audio_mono, sample_rate, nperseg=2048, noverlap=1536)
    pcm = ax5.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis')
    ax5.set_ylabel('Frequency (Hz)', fontsize=10)
    ax5.set_xlabel('Time (s)', fontsize=10)
    ax5.set_title('Spectrogram - Full Track', fontsize=12, fontweight='bold')
    ax5.set_ylim([0, 20000])
    ax5.axvline(x=drop_time, color='red', linestyle='--', linewidth=2, label=f'DROP @ {drop_time}s')
    ax5.legend(fontsize=9, loc='upper right')
    plt.colorbar(pcm, ax=ax5, label='Magnitude (dB)')

    # 6. Critical frequencies highlighting
    ax6 = plt.subplot(3, 2, 6)
    ax6.semilogx(freqs_full, spectrum_full, linewidth=1.5, color='#00ff00', alpha=0.5)

    # Mark critical resonances
    resonance_freqs = [146.5, 1693.4, 2244.1, 3544.9, 7916.0]
    for freq in resonance_freqs:
        idx = np.argmin(np.abs(freqs_full - freq))
        ax6.plot(freqs_full[idx], spectrum_full[idx], 'ro', markersize=8, alpha=0.7)
        ax6.annotate(f'{freq:.0f} Hz', xy=(freqs_full[idx], spectrum_full[idx]),
                    xytext=(10, 10), textcoords='offset points', fontsize=8,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.3))

    ax6.grid(True, alpha=0.3)
    ax6.set_xlabel('Frequency (Hz)', fontsize=10)
    ax6.set_ylabel('Magnitude (dB)', fontsize=10)
    ax6.set_title('Critical Resonances Detection', fontsize=12, fontweight='bold')
    ax6.set_xlim([20, 20000])

    plt.tight_layout()
    plt.savefig('/home/user/look-at-me/frequency_analysis.png', dpi=150, facecolor='black')
    print(f"✓ Visualization saved: /home/user/look-at-me/frequency_analysis.png")

    # Create additional detailed report
    create_detailed_report(freqs_full, spectrum_full, spectrum_before, spectrum_after)

def create_detailed_report(freqs, spectrum_full, spectrum_before, spectrum_after):
    """Create detailed text report"""

    with open('/home/user/look-at-me/FREQUENCY_ANALYSIS_REPORT.txt', 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write("ДЕТАЛЬНЫЙ ЧАСТОТНЫЙ АНАЛИЗ ТРЕКА 'СМОТРЕЛА' ОТ САЙМУРР\n")
        f.write("="*100 + "\n\n")

        f.write("КЛЮЧЕВЫЕ ЧАСТОТЫ С ТОЧНЫМИ ЗНАЧЕНИЯМИ:\n")
        f.write("-"*100 + "\n\n")

        # Find peaks in each band
        bands_detail = {
            'Sub-bass (20-60 Hz)': (20, 60),
            'Bass (60-250 Hz)': (60, 250),
            'Low-mids (250-500 Hz)': (250, 500),
            'Mids (500-2000 Hz)': (500, 2000),
            'High-mids (2000-4000 Hz)': (2000, 4000),
            'Highs (4000-10000 Hz)': (4000, 10000),
            'Air (10000-20000 Hz)': (10000, 20000)
        }

        for band_name, (low, high) in bands_detail.items():
            mask = (freqs >= low) & (freqs < high)
            band_spectrum = spectrum_full[mask]
            band_freqs = freqs[mask]

            if len(band_spectrum) > 0:
                # Find top 3 peaks in this band
                peaks, _ = signal.find_peaks(band_spectrum, prominence=1, distance=10)
                if len(peaks) > 0:
                    top_peaks = peaks[np.argsort(band_spectrum[peaks])[-3:]][::-1]

                    f.write(f"{band_name}:\n")
                    for i, peak in enumerate(top_peaks, 1):
                        f.write(f"  Пик {i}: {band_freqs[peak]:7.1f} Hz @ {band_spectrum[peak]:6.2f} dB\n")
                    f.write(f"  Средний уровень: {np.mean(band_spectrum):6.2f} dB\n")
                    f.write(f"  RMS: {np.sqrt(np.mean(band_spectrum**2)):6.2f} dB\n\n")

        f.write("\n" + "="*100 + "\n")
        f.write("ПРОФЕССИОНАЛЬНЫЕ EQ НАСТРОЙКИ ДЛЯ FABFILTER PRO-Q3 / WAVES Q10\n")
        f.write("="*100 + "\n\n")

        eq_settings = [
            ("HIGH-PASS FILTER", 30, 0, 0, "12 dB/oct", "Удаление sub-sonic rumble"),
            ("CUT", 35, -2.0, 0.80, "Bell", "Очистка низких частот от грязи"),
            ("CUT", 146, -4.0, 3.00, "Bell", "Резонанс баса - критический пик"),
            ("CUT", 350, -2.5, 1.50, "Bell", "Low-mid mud - картонность"),
            ("CUT", 1693, -4.0, 3.00, "Bell", "Mid-range резонанс"),
            ("CUT", 2244, -3.5, 3.00, "Bell", "High-mid резонанс"),
            ("CUT", 3544, -3.0, 2.50, "Bell", "Upper-mid резонанс"),
            ("BOOST", 3000, +2.0, 1.20, "Bell", "Presence - читаемость вокала"),
            ("CUT", 7916, -2.5, 2.00, "Bell", "Высокочастотный резонанс"),
            ("BOOST", 12000, +3.0, 0.70, "Shelf", "Air band - открытие верхов"),
        ]

        f.write(f"{'Тип':12} | {'Частота':>10} | {'Gain':>10} | {'Q':>8} | {'Фильтр':>10} | Описание\n")
        f.write("-"*100 + "\n")

        for eq_type, freq, gain, q, filter_type, description in eq_settings:
            f.write(f"{eq_type:12} | {freq:8} Hz | {gain:+8.1f} dB | {q:8.2f} | {filter_type:>10} | {description}\n")

        f.write("\n\n" + "="*100 + "\n")
        f.write("РЕКОМЕНДАЦИИ ПО ОБРАБОТКЕ\n")
        f.write("="*100 + "\n\n")

        f.write("1. ЭКВАЛИЗАЦИЯ:\n")
        f.write("   - Применить EQ настройки выше в указанном порядке\n")
        f.write("   - Использовать linear phase EQ для критических частот (146 Hz, 1693 Hz)\n")
        f.write("   - Проверить на референсных мониторах после каждого изменения\n\n")

        f.write("2. ДИНАМИЧЕСКАЯ ОБРАБОТКА:\n")
        f.write("   - Multiband Compressor на Bass (60-250 Hz): Ratio 3:1, Attack 10ms, Release 100ms\n")
        f.write("   - Compressor на Mids (500-2000 Hz): Ratio 2:1, Attack 5ms, Release 50ms\n")
        f.write("   - De-esser на 7916 Hz с threshold -15dB\n\n")

        f.write("3. МАСТЕРИНГ:\n")
        f.write("   - Финальный limiter с ceiling -0.3dBFS\n")
        f.write("   - Subtle saturation на low-mids для тепла\n")
        f.write("   - Stereo widener на highs (4kHz+) для пространства\n\n")

        f.write("4. РЕФЕРЕНСЫ:\n")
        f.write("   - Сравнить с коммерческими треками в том же жанре\n")
        f.write("   - Целевой LUFS: -14 до -10 dB (зависит от платформы)\n")
        f.write("   - True Peak: не превышать -1.0 dBTP\n\n")

    print(f"✓ Detailed report saved: /home/user/look-at-me/FREQUENCY_ANALYSIS_REPORT.txt")

if __name__ == "__main__":
    audio_file = "/home/user/look-at-me/СМОТРЕЛА_teaser.wav"
    analyze_audio_visual(audio_file)
