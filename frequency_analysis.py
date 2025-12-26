#!/usr/bin/env python3
"""
Professional Frequency Analysis for "СМОТРЕЛА" by Саймурр
Sound Engineering Analysis Tool
"""

import numpy as np
import scipy.io.wavfile as wavfile
from scipy import signal
import sys

def analyze_frequency_band(spectrum, freqs, low_freq, high_freq):
    """Analyze specific frequency band"""
    mask = (freqs >= low_freq) & (freqs < high_freq)
    band_spectrum = spectrum[mask]
    band_freqs = freqs[mask]

    if len(band_spectrum) == 0:
        return {
            'avg_db': 0,
            'peak_db': 0,
            'peak_freq': 0,
            'rms_db': 0
        }

    avg_db = np.mean(band_spectrum)
    peak_idx = np.argmax(band_spectrum)
    peak_db = band_spectrum[peak_idx]
    peak_freq = band_freqs[peak_idx]
    rms_db = np.sqrt(np.mean(band_spectrum**2))

    return {
        'avg_db': avg_db,
        'peak_db': peak_db,
        'peak_freq': peak_freq,
        'rms_db': rms_db
    }

def find_resonances(spectrum, freqs, threshold_db=6):
    """Find problematic resonances (peaks above threshold)"""
    # Smooth spectrum to find real peaks
    from scipy.ndimage import gaussian_filter1d
    smoothed = gaussian_filter1d(spectrum, sigma=10)

    # Find local maxima
    peaks, properties = signal.find_peaks(smoothed, prominence=threshold_db, distance=50)

    resonances = []
    for peak in peaks:
        if freqs[peak] > 20 and freqs[peak] < 20000:
            resonances.append({
                'freq': freqs[peak],
                'db': spectrum[peak],
                'prominence': smoothed[peak] - np.mean(smoothed)
            })

    return sorted(resonances, key=lambda x: x['prominence'], reverse=True)

def find_dips(spectrum, freqs, threshold_db=-6):
    """Find frequency dips (valleys)"""
    from scipy.ndimage import gaussian_filter1d
    smoothed = gaussian_filter1d(spectrum, sigma=10)

    # Find local minima (invert and find peaks)
    inverted = -smoothed
    peaks, properties = signal.find_peaks(inverted, prominence=abs(threshold_db), distance=50)

    dips = []
    for peak in peaks:
        if freqs[peak] > 20 and freqs[peak] < 20000:
            avg_around = np.mean(smoothed[max(0, peak-50):min(len(smoothed), peak+50)])
            dip_depth = avg_around - smoothed[peak]
            if dip_depth > abs(threshold_db):
                dips.append({
                    'freq': freqs[peak],
                    'db': spectrum[peak],
                    'depth': dip_depth
                })

    return sorted(dips, key=lambda x: x['depth'], reverse=True)

def compute_spectrum(audio_data, sample_rate):
    """Compute frequency spectrum using FFT"""
    # Use Welch's method for better frequency resolution
    freqs, psd = signal.welch(audio_data, sample_rate,
                               nperseg=8192,
                               noverlap=4096,
                               window='hann',
                               scaling='density')

    # Convert to dB
    spectrum_db = 10 * np.log10(psd + 1e-10)

    return freqs, spectrum_db

def analyze_audio(file_path, drop_time=17.163):
    """Main analysis function"""

    print("="*80)
    print("ПРОФЕССИОНАЛЬНЫЙ ЧАСТОТНЫЙ АНАЛИЗ")
    print("Трек: СМОТРЕЛА от Саймурр")
    print("="*80)
    print()

    # Load audio file
    sample_rate, data = wavfile.read(file_path)

    # Convert to mono if stereo
    if len(data.shape) > 1:
        audio_mono = np.mean(data, axis=1)
    else:
        audio_mono = data

    # Normalize
    audio_mono = audio_mono.astype(np.float64)
    audio_mono = audio_mono / np.max(np.abs(audio_mono))

    duration = len(audio_mono) / sample_rate

    print(f"Файл загружен: {file_path}")
    print(f"Sample Rate: {sample_rate} Hz")
    print(f"Длительность: {duration:.2f} секунд")
    print(f"Каналов: {'Stereo' if len(data.shape) > 1 else 'Mono'}")
    print()

    # Split audio into before and after drop
    drop_sample = int(drop_time * sample_rate)

    audio_before = audio_mono[:drop_sample]
    audio_after = audio_mono[drop_sample:]

    # Compute spectra
    freqs_full, spectrum_full = compute_spectrum(audio_mono, sample_rate)
    freqs_before, spectrum_before = compute_spectrum(audio_before, sample_rate)
    freqs_after, spectrum_after = compute_spectrum(audio_after, sample_rate)

    # Frequency bands
    bands = {
        'Sub-bass': (20, 60),
        'Bass': (60, 250),
        'Low-mids': (250, 500),
        'Mids': (500, 2000),
        'High-mids': (2000, 4000),
        'Highs': (4000, 10000),
        'Air': (10000, 20000)
    }

    print("="*80)
    print("1. СПЕКТРАЛЬНЫЙ АНАЛИЗ - ПОЛНЫЙ ТРЕК")
    print("="*80)
    print()

    for band_name, (low, high) in bands.items():
        analysis = analyze_frequency_band(spectrum_full, freqs_full, low, high)
        print(f"{band_name:12} ({low:5}-{high:5} Hz):")
        print(f"  Средний уровень: {analysis['avg_db']:6.2f} dB")
        print(f"  Пиковый уровень: {analysis['peak_db']:6.2f} dB @ {analysis['peak_freq']:.1f} Hz")
        print(f"  RMS уровень:     {analysis['rms_db']:6.2f} dB")
        print()

    print("="*80)
    print("2. ПРОБЛЕМНЫЕ ЧАСТОТЫ")
    print("="*80)
    print()

    # Find resonances
    print("РЕЗОНАНСЫ (избыточные частоты):")
    print("-" * 80)
    resonances = find_resonances(spectrum_full, freqs_full, threshold_db=3)

    if resonances:
        for i, res in enumerate(resonances[:10], 1):
            print(f"{i:2}. {res['freq']:7.1f} Hz - Уровень: {res['db']:6.2f} dB "
                  f"(+{res['prominence']:5.2f} dB над средним)")
    else:
        print("Критических резонансов не обнаружено")
    print()

    # Find dips
    print("ПРОВАЛЫ (недостаточные частоты):")
    print("-" * 80)
    dips = find_dips(spectrum_full, freqs_full, threshold_db=-4)

    if dips:
        for i, dip in enumerate(dips[:10], 1):
            print(f"{i:2}. {dip['freq']:7.1f} Hz - Уровень: {dip['db']:6.2f} dB "
                  f"(-{dip['depth']:5.2f} dB ниже среднего)")
    else:
        print("Критических провалов не обнаружено")
    print()

    print("="*80)
    print(f"3. СРАВНЕНИЕ ДО и ПОСЛЕ DROP (DROP @ {drop_time}s)")
    print("="*80)
    print()

    print(f"{'Диапазон':12} | {'ДО DROP':>12} | {'ПОСЛЕ DROP':>12} | {'Разница':>12}")
    print("-" * 80)

    for band_name, (low, high) in bands.items():
        before = analyze_frequency_band(spectrum_before, freqs_before, low, high)
        after = analyze_frequency_band(spectrum_after, freqs_after, low, high)
        diff = after['avg_db'] - before['avg_db']

        print(f"{band_name:12} | {before['avg_db']:10.2f} dB | {after['avg_db']:10.2f} dB | "
              f"{diff:+10.2f} dB {'▲' if diff > 1 else '▼' if diff < -1 else '='}")

    print()

    print("="*80)
    print("4. EQ РЕКОМЕНДАЦИИ")
    print("="*80)
    print()

    recommendations = []

    # Analyze and generate recommendations

    # Check sub-bass
    sub_bass = analyze_frequency_band(spectrum_full, freqs_full, 20, 60)
    bass = analyze_frequency_band(spectrum_full, freqs_full, 60, 250)
    low_mids = analyze_frequency_band(spectrum_full, freqs_full, 250, 500)
    mids = analyze_frequency_band(spectrum_full, freqs_full, 500, 2000)
    high_mids = analyze_frequency_band(spectrum_full, freqs_full, 2000, 4000)
    highs = analyze_frequency_band(spectrum_full, freqs_full, 4000, 10000)
    air = analyze_frequency_band(spectrum_full, freqs_full, 10000, 20000)

    # Sub-bass recommendations
    if sub_bass['avg_db'] < bass['avg_db'] - 15:
        recommendations.append({
            'freq': 40,
            'gain': 2.5,
            'q': 0.7,
            'reason': 'Усиление фундамента - недостаточный sub-bass'
        })
    elif sub_bass['avg_db'] > bass['avg_db'] - 5:
        recommendations.append({
            'freq': 35,
            'gain': -2.0,
            'q': 0.8,
            'reason': 'Очистка низов - избыточный rumble'
        })

    # Bass recommendations
    if bass['peak_freq'] > 120:
        recommendations.append({
            'freq': int(bass['peak_freq']),
            'gain': -1.5,
            'q': 2.0,
            'reason': f'Резонанс баса на {bass["peak_freq"]:.0f} Hz'
        })

    # Low-mids (often problematic in modern mixes)
    if low_mids['avg_db'] > mids['avg_db'] + 3:
        recommendations.append({
            'freq': 350,
            'gain': -2.5,
            'q': 1.5,
            'reason': 'Грязь в low-mids - частота "картонности"'
        })

    # Add resonance-based recommendations
    for res in resonances[:5]:
        if res['prominence'] > 8:
            recommendations.append({
                'freq': int(res['freq']),
                'gain': -min(res['prominence'] / 2, 4.0),
                'q': 3.0,
                'reason': f'Критический резонанс - {res["prominence"]:.1f} dB над средним'
            })

    # Add dip-based recommendations
    for dip in dips[:3]:
        if dip['depth'] > 8 and dip['freq'] > 100:
            recommendations.append({
                'freq': int(dip['freq']),
                'gain': min(dip['depth'] / 2, 3.0),
                'q': 2.0,
                'reason': f'Заполнение провала - {dip["depth"]:.1f} dB ниже среднего'
            })

    # High-mids presence
    if high_mids['avg_db'] < mids['avg_db'] - 8:
        recommendations.append({
            'freq': 3000,
            'gain': 2.0,
            'q': 1.2,
            'reason': 'Недостаток presence - вокал/мелодия теряются'
        })
    elif high_mids['avg_db'] > mids['avg_db'] + 3:
        recommendations.append({
            'freq': 2500,
            'gain': -2.5,
            'q': 1.5,
            'reason': 'Избыток high-mids - резкость и усталость'
        })

    # Air band
    if air['avg_db'] < highs['avg_db'] - 15:
        recommendations.append({
            'freq': 12000,
            'gain': 3.0,
            'q': 0.7,
            'reason': 'Открытие air band - недостаток "воздуха"'
        })

    # Print recommendations
    print(f"{'#':3} | {'Частота (Hz)':>12} | {'Gain (dB)':>10} | {'Q-фактор':>10} | Причина")
    print("-" * 100)

    for i, rec in enumerate(recommendations, 1):
        print(f"{i:3} | {rec['freq']:12} Hz | {rec['gain']:+9.1f} dB | {rec['q']:10.2f} | {rec['reason']}")

    print()
    print("="*80)
    print("ДОПОЛНИТЕЛЬНЫЕ РЕКОМЕНДАЦИИ")
    print("="*80)
    print()

    # Dynamic processing recommendations
    print("DYNAMIC PROCESSING:")
    print("-" * 80)

    # Check dynamic range
    dynamic_range = np.max(spectrum_full) - np.min(spectrum_full[freqs_full > 20])
    print(f"Динамический диапазон спектра: {dynamic_range:.1f} dB")

    if dynamic_range > 80:
        print("• Рекомендуется multiband compression для контроля динамики")
        print(f"  - Bass (60-250 Hz): Ratio 3:1, Threshold -15dB")
        print(f"  - Mids (250-2000 Hz): Ratio 2:1, Threshold -12dB")
        print(f"  - Highs (2000+ Hz): Ratio 2.5:1, Threshold -10dB")

    print()

    # Overall tonal balance
    print("ТОНАЛЬНЫЙ БАЛАНС:")
    print("-" * 80)
    low_energy = (sub_bass['rms_db'] + bass['rms_db']) / 2
    mid_energy = (low_mids['rms_db'] + mids['rms_db']) / 2
    high_energy = (high_mids['rms_db'] + highs['rms_db'] + air['rms_db']) / 3

    print(f"Низкие частоты:   {low_energy:6.2f} dB")
    print(f"Средние частоты:  {mid_energy:6.2f} dB")
    print(f"Высокие частоты:  {high_energy:6.2f} dB")
    print()

    if abs(low_energy - mid_energy) > 10:
        print(f"⚠ ВНИМАНИЕ: Дисбаланс между низами и серединой ({abs(low_energy - mid_energy):.1f} dB)")
    if abs(mid_energy - high_energy) > 8:
        print(f"⚠ ВНИМАНИЕ: Дисбаланс между серединой и верхами ({abs(mid_energy - high_energy):.1f} dB)")

    print()
    print("="*80)
    print("Анализ завершен!")
    print("="*80)

if __name__ == "__main__":
    audio_file = "/home/user/look-at-me/СМОТРЕЛА_teaser.wav"
    analyze_audio(audio_file, drop_time=17.163)
