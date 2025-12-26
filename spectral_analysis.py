#!/usr/bin/env python3
"""
Professional Spectral Analysis Tool
Abbey Road Studios methodology
"""

import numpy as np
import scipy.io.wavfile as wavfile
from scipy import signal
from scipy.fft import rfft, rfftfreq
import json
from pathlib import Path

class SpectralAnalyzer:
    """Professional spectral analyzer for audio mastering"""

    # Frequency bands (Hz)
    BANDS = {
        'Sub': (20, 60),
        'Bass': (60, 250),
        'Low-mids': (250, 500),
        'Mids': (500, 2000),
        'High-mids': (2000, 6000),
        'Highs': (6000, 12000),
        'Air': (12000, 20000)
    }

    def __init__(self, filepath):
        self.filepath = filepath
        self.sample_rate, self.audio_data = wavfile.read(filepath)

        # Convert to mono if stereo
        if len(self.audio_data.shape) > 1:
            self.audio_mono = np.mean(self.audio_data, axis=1)
        else:
            self.audio_mono = self.audio_data

        # Normalize to float
        if self.audio_data.dtype == np.int16:
            self.audio_mono = self.audio_mono.astype(np.float32) / 32768.0
        elif self.audio_data.dtype == np.int32:
            self.audio_mono = self.audio_mono.astype(np.float32) / 2147483648.0

        self.duration = len(self.audio_mono) / self.sample_rate

        print(f"\n{'='*80}")
        print(f"ABBEY ROAD STUDIOS - SPECTRAL ANALYSIS REPORT")
        print(f"{'='*80}")
        print(f"File: {Path(filepath).name}")
        print(f"Sample Rate: {self.sample_rate} Hz")
        print(f"Duration: {self.duration:.2f} seconds")
        print(f"Channels: {'Stereo' if len(self.audio_data.shape) > 1 else 'Mono'}")
        print(f"{'='*80}\n")

    def analyze_full_spectrum(self):
        """FFT analysis of the entire track"""
        print("1. FULL SPECTRUM FFT ANALYSIS")
        print("-" * 80)

        # Use larger window for better frequency resolution
        n_fft = 8192

        # Calculate spectrogram for entire track
        f, t, Sxx = signal.spectrogram(
            self.audio_mono,
            self.sample_rate,
            window='hann',
            nperseg=n_fft,
            noverlap=n_fft//2,
            scaling='density'
        )

        # Average across time to get overall spectrum
        spectrum_avg = np.mean(Sxx, axis=1)
        spectrum_db = 10 * np.log10(spectrum_avg + 1e-10)

        # Analyze each frequency band
        for band_name, (low_freq, high_freq) in self.BANDS.items():
            # Find indices for this band
            band_mask = (f >= low_freq) & (f <= high_freq)
            band_spectrum = spectrum_db[band_mask]
            band_freqs = f[band_mask]

            if len(band_spectrum) > 0:
                avg_level = np.mean(band_spectrum)
                max_level = np.max(band_spectrum)
                min_level = np.min(band_spectrum)
                peak_freq = band_freqs[np.argmax(band_spectrum)]

                print(f"\n{band_name} ({low_freq}-{high_freq} Hz):")
                print(f"  Average Level: {avg_level:.2f} dB")
                print(f"  Peak Level: {max_level:.2f} dB at {peak_freq:.1f} Hz")
                print(f"  Dynamic Range: {max_level - min_level:.2f} dB")

        return f, spectrum_db

    def find_problematic_frequencies(self, freqs, spectrum_db):
        """Identify resonances, dips, and masking issues"""
        print("\n\n2. PROBLEMATIC FREQUENCIES DETECTION")
        print("-" * 80)

        # Find peaks (resonances)
        # Use scipy's find_peaks with appropriate parameters
        peak_indices, peak_properties = signal.find_peaks(
            spectrum_db,
            prominence=6,  # At least 6dB above surrounding
            distance=20    # Minimum distance between peaks
        )

        print("\n🔴 RESONANCES (Problematic Peaks):")
        resonances = []
        for idx in peak_indices:
            freq = freqs[idx]
            level = spectrum_db[idx]
            prominence = peak_properties['prominences'][list(peak_indices).index(idx)]

            # Only report significant resonances in audible range
            if 40 < freq < 16000 and prominence > 6:
                resonances.append({
                    'frequency': freq,
                    'level': level,
                    'prominence': prominence
                })
                print(f"  {freq:.1f} Hz - Level: {level:.2f} dB - Prominence: {prominence:.2f} dB")

        # Find dips (notches)
        inverted_spectrum = -spectrum_db
        dip_indices, dip_properties = signal.find_peaks(
            inverted_spectrum,
            prominence=6,
            distance=20
        )

        print("\n🔵 FREQUENCY DIPS (Notches/Holes):")
        dips = []
        for idx in dip_indices:
            freq = freqs[idx]
            level = spectrum_db[idx]
            prominence = dip_properties['prominences'][list(dip_indices).index(idx)]

            if 40 < freq < 16000 and prominence > 6:
                dips.append({
                    'frequency': freq,
                    'level': level,
                    'depth': prominence
                })
                print(f"  {freq:.1f} Hz - Level: {level:.2f} dB - Depth: {prominence:.2f} dB")

        # Analyze masking issues
        print("\n⚠️  MASKING ANALYSIS:")
        self.analyze_masking(freqs, spectrum_db)

        return resonances, dips

    def analyze_masking(self, freqs, spectrum_db):
        """Analyze frequency masking issues"""

        # Check if bass is masking low-mids
        bass_range = (freqs >= 60) & (freqs <= 250)
        lowmid_range = (freqs >= 250) & (freqs <= 500)

        bass_avg = np.mean(spectrum_db[bass_range])
        lowmid_avg = np.mean(spectrum_db[lowmid_range])

        if bass_avg - lowmid_avg > 10:
            print(f"  Bass masking Low-mids: {bass_avg - lowmid_avg:.1f} dB difference")
            print(f"    → Low-mids likely buried under bass")

        # Check if low-mids are masking mids
        mid_range = (freqs >= 500) & (freqs <= 2000)
        mid_avg = np.mean(spectrum_db[mid_range])

        if lowmid_avg - mid_avg > 8:
            print(f"  Low-mids masking Mids: {lowmid_avg - mid_avg:.1f} dB difference")
            print(f"    → Vocals/lead instruments may lack clarity")

        # Check high-frequency balance
        highmid_range = (freqs >= 2000) & (freqs <= 6000)
        highs_range = (freqs >= 6000) & (freqs <= 12000)

        highmid_avg = np.mean(spectrum_db[highmid_range])
        highs_avg = np.mean(spectrum_db[highs_range])

        if highmid_avg - highs_avg > 15:
            print(f"  Lacking high frequency extension: {highmid_avg - highs_avg:.1f} dB roll-off")
            print(f"    → Track may sound dull/dark")
        elif highs_avg - highmid_avg > 10:
            print(f"  Excessive high frequencies: {highs_avg - highmid_avg:.1f} dB boost")
            print(f"    → Track may sound harsh/brittle")

    def sectional_analysis(self):
        """Analyze different sections of the track"""
        print("\n\n3. SECTIONAL ANALYSIS")
        print("-" * 80)

        # Divide track into 5 sections
        section_names = ['Intro', 'Verse/Build', 'Chorus/Drop', 'Bridge/Middle', 'Outro']
        n_sections = 5
        section_length = len(self.audio_mono) // n_sections

        sections_data = []

        for i, section_name in enumerate(section_names):
            start = i * section_length
            end = (i + 1) * section_length if i < n_sections - 1 else len(self.audio_mono)

            section_audio = self.audio_mono[start:end]

            # Calculate spectrum for this section
            n_fft = 4096
            f, Sxx = signal.welch(
                section_audio,
                self.sample_rate,
                window='hann',
                nperseg=n_fft,
                scaling='density'
            )

            spectrum_db = 10 * np.log10(Sxx + 1e-10)

            # Calculate RMS for overall level
            rms = np.sqrt(np.mean(section_audio**2))
            rms_db = 20 * np.log10(rms + 1e-10)

            print(f"\n{section_name} ({start/self.sample_rate:.1f}s - {end/self.sample_rate:.1f}s):")
            print(f"  RMS Level: {rms_db:.2f} dB")

            # Analyze band levels for this section
            for band_name, (low_freq, high_freq) in self.BANDS.items():
                band_mask = (f >= low_freq) & (f <= high_freq)
                if np.any(band_mask):
                    band_avg = np.mean(spectrum_db[band_mask])
                    print(f"  {band_name}: {band_avg:.2f} dB")

            sections_data.append({
                'name': section_name,
                'rms_db': rms_db,
                'time_range': (start/self.sample_rate, end/self.sample_rate)
            })

        return sections_data

    def generate_eq_recommendations(self, resonances, dips, freqs, spectrum_db):
        """Generate professional EQ recommendations"""
        print("\n\n4. PROFESSIONAL EQ RECOMMENDATIONS")
        print("=" * 80)

        recommendations = []

        # Analyze overall balance first
        print("\n📊 OVERALL TONAL BALANCE:")

        for band_name, (low_freq, high_freq) in self.BANDS.items():
            band_mask = (freqs >= low_freq) & (freqs <= high_freq)
            if np.any(band_mask):
                band_avg = np.mean(spectrum_db[band_mask])

                # Reference levels (based on professional mixing standards)
                reference_levels = {
                    'Sub': -35,
                    'Bass': -30,
                    'Low-mids': -28,
                    'Mids': -25,
                    'High-mids': -28,
                    'Highs': -32,
                    'Air': -38
                }

                diff = band_avg - reference_levels.get(band_name, -30)

                if abs(diff) > 5:
                    status = "TOO HOT" if diff > 0 else "TOO WEAK"
                    print(f"  {band_name}: {band_avg:.1f} dB ({diff:+.1f} dB from reference) - {status}")

        print("\n\n🎚️  DETAILED EQ SETTINGS:")
        print("-" * 80)

        eq_num = 1

        # Handle resonances
        for res in resonances[:8]:  # Top 8 resonances
            freq = res['frequency']
            prominence = res['prominence']

            # Calculate appropriate Q based on prominence
            if prominence > 12:
                q = 4.0  # Narrow cut for sharp resonances
                gain = -min(prominence * 0.6, 8.0)
            elif prominence > 8:
                q = 2.5
                gain = -min(prominence * 0.5, 6.0)
            else:
                q = 1.5
                gain = -min(prominence * 0.4, 4.0)

            # Determine the issue
            if freq < 100:
                issue = "Sub-bass resonance / rumble"
            elif freq < 250:
                issue = "Bass buildup / muddiness"
            elif freq < 500:
                issue = "Low-mid boxiness"
            elif freq < 2000:
                issue = "Mid-range honk / harshness"
            elif freq < 6000:
                issue = "Upper-mid harshness / sibilance"
            else:
                issue = "High-frequency harshness"

            print(f"\nEQ #{eq_num} - CUT RESONANCE:")
            print(f"  Frequency: {freq:.1f} Hz")
            print(f"  Gain: {gain:.1f} dB")
            print(f"  Q: {q:.1f}")
            print(f"  Filter Type: Parametric Bell")
            print(f"  Reason: {issue} - {prominence:.1f} dB prominence")

            recommendations.append({
                'eq_num': eq_num,
                'frequency': freq,
                'gain': gain,
                'q': q,
                'filter_type': 'Bell',
                'reason': issue
            })

            eq_num += 1

        # Handle dips (boost conservatively)
        for dip in dips[:4]:  # Top 4 dips
            freq = dip['frequency']
            depth = dip['depth']

            # Be conservative with boosts
            if depth > 10:
                q = 2.0
                gain = min(depth * 0.4, 5.0)
            else:
                q = 1.5
                gain = min(depth * 0.3, 3.0)

            if freq < 250:
                issue = "Bass deficiency"
            elif freq < 2000:
                issue = "Mid-range hole / lack of body"
            elif freq < 6000:
                issue = "Lack of presence / clarity"
            else:
                issue = "Lack of air / brightness"

            print(f"\nEQ #{eq_num} - FILL DIP:")
            print(f"  Frequency: {freq:.1f} Hz")
            print(f"  Gain: +{gain:.1f} dB")
            print(f"  Q: {q:.1f}")
            print(f"  Filter Type: Parametric Bell")
            print(f"  Reason: {issue} - {depth:.1f} dB deficiency")

            recommendations.append({
                'eq_num': eq_num,
                'frequency': freq,
                'gain': gain,
                'q': q,
                'filter_type': 'Bell',
                'reason': issue
            })

            eq_num += 1

        # Overall tonal shaping recommendations
        bass_range = (freqs >= 60) & (freqs <= 250)
        air_range = (freqs >= 12000) & (freqs <= 20000)

        bass_avg = np.mean(spectrum_db[bass_range])
        air_avg = np.mean(spectrum_db[air_range])

        # High-pass filter recommendation
        print(f"\nEQ #{eq_num} - HIGH-PASS FILTER:")
        print(f"  Frequency: 30.0 Hz")
        print(f"  Slope: 12 dB/octave")
        print(f"  Filter Type: High-Pass")
        print(f"  Reason: Remove sub-sonic rumble and save headroom")

        recommendations.append({
            'eq_num': eq_num,
            'frequency': 30,
            'gain': 0,
            'q': 0.7,
            'filter_type': 'HPF 12dB',
            'reason': 'Sub-sonic rumble removal'
        })

        eq_num += 1

        # Air boost if needed
        if air_avg < -38:
            print(f"\nEQ #{eq_num} - AIR SHELF:")
            print(f"  Frequency: 12000.0 Hz")
            print(f"  Gain: +2.5 dB")
            print(f"  Filter Type: High Shelf")
            print(f"  Reason: Add air and sparkle (currently {air_avg:.1f} dB)")

            recommendations.append({
                'eq_num': eq_num,
                'frequency': 12000,
                'gain': 2.5,
                'q': 0.7,
                'filter_type': 'High Shelf',
                'reason': 'Add air and openness'
            })

        print("\n" + "=" * 80)
        print("END OF ANALYSIS REPORT")
        print("=" * 80)

        return recommendations

    def run_full_analysis(self):
        """Execute complete analysis pipeline"""
        # 1. Full spectrum analysis
        freqs, spectrum_db = self.analyze_full_spectrum()

        # 2. Find problematic frequencies
        resonances, dips = self.find_problematic_frequencies(freqs, spectrum_db)

        # 3. Sectional analysis
        sections = self.sectional_analysis()

        # 4. Generate EQ recommendations
        recommendations = self.generate_eq_recommendations(resonances, dips, freqs, spectrum_db)

        # Save detailed report
        report = {
            'file': str(self.filepath),
            'sample_rate': int(self.sample_rate),
            'duration': float(self.duration),
            'resonances': [
                {
                    'frequency': float(r['frequency']),
                    'level': float(r['level']),
                    'prominence': float(r['prominence'])
                } for r in resonances
            ],
            'dips': [
                {
                    'frequency': float(d['frequency']),
                    'level': float(d['level']),
                    'depth': float(d['depth'])
                } for d in dips
            ],
            'eq_recommendations': recommendations
        }

        report_path = Path(self.filepath).with_suffix('.spectral_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Detailed report saved to: {report_path}")

        return report


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python spectral_analysis.py <audio_file.wav>")
        sys.exit(1)

    audio_file = sys.argv[1]

    try:
        analyzer = SpectralAnalyzer(audio_file)
        analyzer.run_full_analysis()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
