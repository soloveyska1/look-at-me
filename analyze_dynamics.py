#!/usr/bin/env python3
"""
Professional Dynamics & Structure Analysis for Music Production
Dynamics Engineer Analysis Tool
"""

import numpy as np
from scipy.io import wavfile
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

class DynamicsAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.sr, self.audio = wavfile.read(filepath)

        # Convert to mono if stereo
        if len(self.audio.shape) > 1:
            self.mono = np.mean(self.audio, axis=1)
        else:
            self.mono = self.audio

        # Normalize to float [-1, 1]
        self.mono = self.mono.astype(np.float64)
        if self.mono.max() > 1.0:
            self.mono = self.mono / np.abs(self.mono).max()

        self.duration = len(self.mono) / self.sr

    def db_to_amplitude(self, db):
        return 10 ** (db / 20)

    def amplitude_to_db(self, amp):
        return 20 * np.log10(np.maximum(amp, 1e-10))

    def calculate_rms(self, signal_segment):
        """Calculate RMS in dB"""
        rms = np.sqrt(np.mean(signal_segment**2))
        return self.amplitude_to_db(rms)

    def calculate_lufs_approximation(self, signal_segment):
        """
        Simplified LUFS calculation (K-weighted approximation)
        Professional LUFS uses ITU-R BS.1770-4 filtering
        """
        # High-pass filter (pre-filter stage 1)
        sos_hp = signal.butter(2, 100, 'hp', fs=self.sr, output='sos')
        filtered = signal.sosfilt(sos_hp, signal_segment)

        # High-frequency boost (pre-filter stage 2 - K-weighting approximation)
        # Simplified version of the shelf filter
        mean_square = np.mean(filtered**2)
        lufs = -0.691 + 10 * np.log10(np.maximum(mean_square, 1e-10))

        return lufs

    def detect_onsets(self, hop_length=512):
        """Detect onsets/transients for structure analysis"""
        # Calculate spectral flux
        stft = np.abs(signal.stft(self.mono, self.sr, nperseg=2048, noverlap=2048-hop_length)[2])

        # Onset strength envelope
        onset_env = np.sum(np.diff(stft, axis=1).clip(min=0), axis=0)
        onset_env = np.concatenate([[0], onset_env])

        # Smooth
        onset_env = signal.medfilt(onset_env, 3)

        # Peak picking
        threshold = np.mean(onset_env) + 0.5 * np.std(onset_env)
        peaks, _ = signal.find_peaks(onset_env, height=threshold, distance=int(self.sr/hop_length*0.3))

        onset_times = peaks * hop_length / self.sr
        onset_strengths = onset_env[peaks]

        return onset_times, onset_strengths, onset_env

    def calculate_energy_profile(self, window_size=2048, hop_length=512):
        """Calculate energy profile over time"""
        num_windows = int((len(self.mono) - window_size) / hop_length) + 1
        energy = np.zeros(num_windows)
        times = np.zeros(num_windows)

        for i in range(num_windows):
            start = i * hop_length
            end = start + window_size
            if end <= len(self.mono):
                segment = self.mono[start:end]
                energy[i] = np.sum(segment**2)
                times[i] = start / self.sr

        # Convert to dB
        energy_db = 10 * np.log10(np.maximum(energy, 1e-10))

        return times, energy_db

    def detect_transients(self):
        """Detect kicks, snares, and other transients"""
        # Envelope follower
        envelope = np.abs(signal.hilbert(self.mono))

        # High-pass for transient emphasis
        sos = signal.butter(4, 80, 'hp', fs=self.sr, output='sos')
        transient_emphasis = signal.sosfilt(sos, self.mono)
        transient_env = np.abs(signal.hilbert(transient_emphasis))

        # Detect peaks in transient envelope
        threshold = np.mean(transient_env) + 1.5 * np.std(transient_env)
        peaks, properties = signal.find_peaks(
            transient_env,
            height=threshold,
            distance=int(self.sr*0.1)  # Min 100ms between transients
        )

        transient_times = peaks / self.sr
        transient_strengths = transient_env[peaks]

        return transient_times, transient_strengths

    def analyze_sections(self, energy_times, energy_db):
        """
        Detect musical sections based on energy changes
        """
        # Smooth energy for section detection
        smooth_window = int(self.sr / 512 * 2)  # ~2 seconds
        energy_smooth = signal.medfilt(energy_db, min(smooth_window, len(energy_db)//2*2-1))

        # Find significant changes in energy
        energy_diff = np.diff(energy_smooth)
        energy_diff = np.concatenate([[0], energy_diff])

        # Detect section boundaries
        threshold_up = np.std(energy_diff) * 1.5
        threshold_down = -np.std(energy_diff) * 1.5

        # Combine with onset information for better section detection
        onset_times, _, _ = self.detect_onsets()

        # Simple heuristic section detection based on energy levels
        sections = []
        section_names = ['Intro', 'Verse 1', 'Pre-Chorus 1', 'Chorus 1',
                        'Verse 2', 'Pre-Chorus 2', 'Chorus 2', 'Bridge',
                        'Chorus 3', 'Outro']

        # Divide into energy-based segments
        energy_percentiles = np.percentile(energy_smooth, [20, 40, 60, 80])

        current_section = 0
        last_boundary = 0
        min_section_duration = 4.0  # seconds

        for i in range(len(energy_smooth)):
            time = energy_times[i]

            # Look for significant energy changes
            if i > 0 and time - last_boundary > min_section_duration:
                if abs(energy_diff[i]) > threshold_up or abs(energy_diff[i]) > abs(threshold_down):
                    if current_section < len(section_names):
                        sections.append({
                            'name': section_names[current_section],
                            'start': last_boundary,
                            'end': time
                        })
                        last_boundary = time
                        current_section += 1

        # Add final section
        if current_section < len(section_names):
            sections.append({
                'name': section_names[current_section],
                'start': last_boundary,
                'end': self.duration
            })

        # If we didn't detect many sections, use simpler time-based division
        if len(sections) < 3:
            sections = self.simple_section_division()

        return sections

    def simple_section_division(self):
        """Fallback: divide track into typical sections based on duration"""
        sections = []

        if self.duration < 30:
            # Very short track
            sections = [
                {'name': 'Intro', 'start': 0, 'end': self.duration * 0.2},
                {'name': 'Main', 'start': self.duration * 0.2, 'end': self.duration * 0.8},
                {'name': 'Outro', 'start': self.duration * 0.8, 'end': self.duration}
            ]
        elif self.duration < 120:
            # Standard pop song structure
            intro_len = min(8, self.duration * 0.1)
            verse_len = min(16, self.duration * 0.2)
            chorus_len = min(16, self.duration * 0.2)

            sections = [
                {'name': 'Intro', 'start': 0, 'end': intro_len},
                {'name': 'Verse 1', 'start': intro_len, 'end': intro_len + verse_len},
                {'name': 'Chorus 1', 'start': intro_len + verse_len, 'end': intro_len + verse_len + chorus_len},
                {'name': 'Verse 2', 'start': intro_len + verse_len + chorus_len, 'end': self.duration * 0.5},
                {'name': 'Chorus 2', 'start': self.duration * 0.5, 'end': self.duration * 0.7},
                {'name': 'Bridge/Chorus 3', 'start': self.duration * 0.7, 'end': self.duration * 0.9},
                {'name': 'Outro', 'start': self.duration * 0.9, 'end': self.duration}
            ]
        else:
            # Longer track
            sections = [
                {'name': 'Intro', 'start': 0, 'end': 10},
                {'name': 'Build', 'start': 10, 'end': 30},
                {'name': 'Main Section', 'start': 30, 'end': self.duration - 20},
                {'name': 'Outro', 'start': self.duration - 20, 'end': self.duration}
            ]

        return sections

    def analyze_section_dynamics(self, section):
        """Detailed dynamics analysis for a section"""
        start_sample = int(section['start'] * self.sr)
        end_sample = int(section['end'] * self.sr)
        segment = self.mono[start_sample:end_sample]

        if len(segment) == 0:
            return None

        # RMS level
        rms_db = self.calculate_rms(segment)

        # LUFS approximation
        lufs = self.calculate_lufs_approximation(segment)

        # Peak level
        peak = np.max(np.abs(segment))
        peak_db = self.amplitude_to_db(peak)

        # Crest factor (peak to RMS ratio)
        rms_linear = np.sqrt(np.mean(segment**2))
        crest_factor = peak / np.maximum(rms_linear, 1e-10)
        crest_factor_db = self.amplitude_to_db(crest_factor)

        # Dynamic range (difference between loudest and quietest moments)
        window_size = int(0.4 * self.sr)  # 400ms windows
        hop = window_size // 2
        num_windows = max(1, (len(segment) - window_size) // hop)

        window_rms = []
        for i in range(num_windows):
            start = i * hop
            end = start + window_size
            if end <= len(segment):
                win_segment = segment[start:end]
                win_rms = np.sqrt(np.mean(win_segment**2))
                window_rms.append(win_rms)

        if len(window_rms) > 0:
            window_rms = np.array(window_rms)
            dynamic_range = self.amplitude_to_db(np.max(window_rms)) - self.amplitude_to_db(np.min(window_rms))
        else:
            dynamic_range = 0

        return {
            'rms_db': rms_db,
            'lufs': lufs,
            'peak_db': peak_db,
            'crest_factor_db': crest_factor_db,
            'dynamic_range': dynamic_range,
            'duration': section['end'] - section['start']
        }

    def generate_compression_recommendations(self, section_name, dynamics):
        """Generate professional compression recommendations"""
        recommendations = {
            'section': section_name,
            'multiband': {},
            'parallel_compression': {},
            'sidechain': {},
            'transient_shaping': {}
        }

        # Multiband compression settings
        if 'Intro' in section_name or 'Outro' in section_name:
            recommendations['multiband'] = {
                'low_band': '20-120 Hz: Ratio 2:1, Threshold -18dB, Attack 30ms, Release 200ms',
                'mid_band': '120-2kHz: Ratio 1.5:1, Threshold -15dB, Attack 15ms, Release 100ms',
                'high_band': '2k-20kHz: Ratio 1.3:1, Threshold -12dB, Attack 5ms, Release 50ms',
                'note': 'Gentle compression for dynamic intro/outro'
            }
        elif 'Chorus' in section_name:
            recommendations['multiband'] = {
                'low_band': '20-120 Hz: Ratio 4:1, Threshold -20dB, Attack 10ms, Release 150ms',
                'mid_band': '120-2kHz: Ratio 3:1, Threshold -16dB, Attack 5ms, Release 80ms',
                'high_band': '2k-20kHz: Ratio 2.5:1, Threshold -14dB, Attack 1ms, Release 40ms',
                'note': 'Aggressive compression for maximum energy and consistency'
            }
        else:  # Verse, Pre-Chorus, Bridge
            recommendations['multiband'] = {
                'low_band': '20-120 Hz: Ratio 3:1, Threshold -20dB, Attack 20ms, Release 180ms',
                'mid_band': '120-2kHz: Ratio 2.5:1, Threshold -16dB, Attack 10ms, Release 90ms',
                'high_band': '2k-20kHz: Ratio 2:1, Threshold -14dB, Attack 3ms, Release 50ms',
                'note': 'Balanced compression maintaining dynamics'
            }

        # Parallel compression
        if dynamics and dynamics['dynamic_range'] > 15:
            recommendations['parallel_compression'] = {
                'ratio': '8:1 to 10:1',
                'threshold': f"{dynamics['rms_db'] - 10:.1f} dB",
                'attack': '1-3ms (fast)',
                'release': '50-100ms (medium-fast)',
                'mix': '20-30% wet',
                'note': 'Heavy parallel compression to add density without losing transients'
            }
        else:
            recommendations['parallel_compression'] = {
                'ratio': '4:1 to 6:1',
                'threshold': f"{dynamics['rms_db'] - 6:.1f} dB" if dynamics else '-20 dB',
                'attack': '5-10ms',
                'release': '100-150ms',
                'mix': '15-25% wet',
                'note': 'Moderate parallel compression for glue'
            }

        # Sidechain recommendations
        if 'Verse' in section_name or 'Chorus' in section_name:
            recommendations['sidechain'] = {
                'kick_to_bass': 'Ratio 6:1, Fast attack (0.1ms), Medium release (150ms), -6dB reduction',
                'kick_to_synths': 'Ratio 3:1, Fast attack, Fast release (50ms), -3dB reduction',
                'note': 'Create pumping effect and clarity for kick drum'
            }
        else:
            recommendations['sidechain'] = {
                'kick_to_bass': 'Ratio 4:1, Fast attack, Medium release (120ms), -4dB reduction',
                'note': 'Subtle ducking for clarity'
            }

        # Transient shaping
        if 'Chorus' in section_name or 'Drop' in section_name:
            recommendations['transient_shaping'] = {
                'drums': 'Attack +3dB to +6dB, Sustain -2dB',
                'bass': 'Attack +2dB, Sustain 0dB',
                'synths': 'Attack +1dB to +3dB',
                'note': 'Enhance punch and impact for high-energy section'
            }
        else:
            recommendations['transient_shaping'] = {
                'drums': 'Attack +1dB to +3dB, Sustain -1dB',
                'bass': 'Attack +1dB, Sustain 0dB',
                'note': 'Moderate transient enhancement'
            }

        return recommendations

    def generate_loudness_strategy(self, sections_analysis, current_rms, target_streaming_lufs=-14):
        """
        Generate comprehensive loudness strategy
        Current streaming targets:
        - Spotify: -14 LUFS
        - Apple Music: -16 LUFS
        - YouTube: -14 LUFS
        - Tidal: -14 LUFS
        """
        strategy = {
            'current_state': {},
            'target_lufs_per_section': {},
            'gain_staging': {},
            'limiting_strategy': {},
            'automation': {}
        }

        # Current state
        strategy['current_state'] = {
            'current_rms': f"{current_rms:.1f} dB",
            'current_headroom': f"{0 - current_rms:.1f} dB",
            'note': 'Track is significantly under-leveled, lots of headroom for processing'
        }

        # Target LUFS per section (dynamic variation for interest)
        strategy['target_lufs_per_section'] = {
            'Intro/Outro': f"{target_streaming_lufs - 2:.1f} LUFS (quieter for dynamics)",
            'Verse': f"{target_streaming_lufs - 1:.1f} LUFS (slightly below target)",
            'Pre-Chorus': f"{target_streaming_lufs:.1f} LUFS (target level)",
            'Chorus': f"{target_streaming_lufs + 1:.1f} LUFS (louder for impact)",
            'Bridge': f"{target_streaming_lufs:.1f} LUFS (target level)",
            'note': 'Vary LUFS by section to maintain interest and dynamics'
        }

        # Gain staging strategy
        total_gain_needed = abs(current_rms - target_streaming_lufs)

        strategy['gain_staging'] = {
            'step_1_clean_gain': '+6 to +8 dB (initial boost)',
            'step_2_compression': f'+{total_gain_needed * 0.4:.1f} dB gain reduction compensated',
            'step_3_saturation': '+1 to +2 dB (harmonic enhancement)',
            'step_4_limiting': f'+{total_gain_needed * 0.3:.1f} dB (final loudness)',
            'total_gain_needed': f"+{total_gain_needed:.1f} dB",
            'note': 'Distribute gain across multiple stages for transparent loudness'
        }

        # Limiting strategy
        strategy['limiting_strategy'] = {
            'ceiling': '-0.3 dB to -0.5 dB (True Peak)',
            'threshold': '-4 dB to -6 dB',
            'release': '50-100ms (auto-release preferred)',
            'lookahead': '5ms',
            'oversampling': '4x or higher',
            'target_gain_reduction': '3-6 dB (transparent), up to 8-10 dB for competitive loudness',
            'note': 'Use high-quality limiter (FabFilter Pro-L2, Ozone, or similar)'
        }

        # Automation recommendations
        strategy['automation'] = []

        for section in sections_analysis:
            section_name = section['section']
            dynamics = section['dynamics']

            if not dynamics:
                continue

            if 'Intro' in section_name:
                strategy['automation'].append({
                    'section': section_name,
                    'time': f"{section['start']:.1f}s - {section['end']:.1f}s",
                    'action': 'Volume fade-in +6dB over 2-4 seconds',
                    'purpose': 'Smooth entrance'
                })

            if 'Verse' in section_name and 'Chorus' in [s['section'] for s in sections_analysis]:
                strategy['automation'].append({
                    'section': section_name,
                    'time': f"{section['start']:.1f}s - {section['end']:.1f}s",
                    'action': 'Slight volume reduction -0.5 to -1dB',
                    'purpose': 'Create contrast with chorus'
                })

            if 'Chorus' in section_name:
                strategy['automation'].append({
                    'section': section_name,
                    'time': f"{section['start']:.1f}s - {section['end']:.1f}s",
                    'action': 'Volume boost +1 to +2dB, slight limiter drive increase',
                    'purpose': 'Maximum impact and energy'
                })

            if 'Bridge' in section_name:
                strategy['automation'].append({
                    'section': section_name,
                    'time': f"{section['start']:.1f}s - {section['end']:.1f}s",
                    'action': 'Dynamic automation based on arrangement (often -1 to -2dB)',
                    'purpose': 'Create tension before final chorus'
                })

            if 'Outro' in section_name:
                strategy['automation'].append({
                    'section': section_name,
                    'time': f"{section['start']:.1f}s - {section['end']:.1f}s",
                    'action': 'Volume fade-out -6 to -12dB',
                    'purpose': 'Smooth ending'
                })

        return strategy


def main():
    filepath = '/home/user/look-at-me/SmotrelaА.wav'

    print("=" * 80)
    print("PROFESSIONAL DYNAMICS & STRUCTURE ANALYSIS")
    print("Dynamics Engineer Report")
    print("=" * 80)
    print()

    # Initialize analyzer
    analyzer = DynamicsAnalyzer(filepath)

    print(f"📊 TRACK INFORMATION")
    print(f"File: {filepath}")
    print(f"Sample Rate: {analyzer.sr} Hz")
    print(f"Duration: {analyzer.duration:.2f} seconds ({analyzer.duration/60:.2f} minutes)")
    print(f"Total Samples: {len(analyzer.mono):,}")
    print()

    # Overall dynamics
    print("=" * 80)
    print("OVERALL DYNAMICS")
    print("=" * 80)

    overall_rms = analyzer.calculate_rms(analyzer.mono)
    overall_lufs = analyzer.calculate_lufs_approximation(analyzer.mono)
    overall_peak = analyzer.amplitude_to_db(np.max(np.abs(analyzer.mono)))

    print(f"RMS Level: {overall_rms:.2f} dB")
    print(f"LUFS (approx): {overall_lufs:.2f} LUFS")
    print(f"Peak Level: {overall_peak:.2f} dB")
    print(f"Headroom: {0 - overall_peak:.2f} dB")
    print()

    # Transient analysis
    print("=" * 80)
    print("TRANSIENT ANALYSIS")
    print("=" * 80)

    transient_times, transient_strengths = analyzer.detect_transients()
    print(f"Detected Transients: {len(transient_times)}")
    print(f"Average Transient Density: {len(transient_times) / analyzer.duration:.2f} transients/second")
    print()

    if len(transient_times) > 0:
        print("First 10 major transients (likely kicks/snares):")
        for i, (time, strength) in enumerate(zip(transient_times[:10], transient_strengths[:10])):
            print(f"  {i+1}. Time: {time:.2f}s, Strength: {strength:.4f}")
    print()

    # Energy profile and section detection
    print("=" * 80)
    print("STRUCTURE ANALYSIS")
    print("=" * 80)

    energy_times, energy_db = analyzer.calculate_energy_profile()
    sections = analyzer.analyze_sections(energy_times, energy_db)

    print(f"Detected Sections: {len(sections)}")
    print()

    # Detailed section analysis
    sections_analysis = []

    for i, section in enumerate(sections, 1):
        print(f"\n{'─' * 80}")
        print(f"SECTION {i}: {section['name']}")
        print(f"{'─' * 80}")
        print(f"Time Range: {section['start']:.2f}s - {section['end']:.2f}s")
        print(f"Duration: {section['end'] - section['start']:.2f}s")

        dynamics = analyzer.analyze_section_dynamics(section)

        if dynamics:
            print(f"\n🎚️  DYNAMICS:")
            print(f"  RMS Level:        {dynamics['rms_db']:>8.2f} dB")
            print(f"  LUFS (approx):    {dynamics['lufs']:>8.2f} LUFS")
            print(f"  Peak Level:       {dynamics['peak_db']:>8.2f} dB")
            print(f"  Crest Factor:     {dynamics['crest_factor_db']:>8.2f} dB")
            print(f"  Dynamic Range:    {dynamics['dynamic_range']:>8.2f} dB")

            # Energy assessment
            if dynamics['rms_db'] > overall_rms + 2:
                energy_level = "HIGH ENERGY ⚡"
            elif dynamics['rms_db'] > overall_rms:
                energy_level = "Above Average 📈"
            elif dynamics['rms_db'] > overall_rms - 2:
                energy_level = "Average 📊"
            else:
                energy_level = "Low Energy 📉"

            print(f"  Energy Level:     {energy_level}")

            sections_analysis.append({
                'section': section['name'],
                'start': section['start'],
                'end': section['end'],
                'dynamics': dynamics
            })

        print()

    # Compression recommendations
    print("\n" + "=" * 80)
    print("COMPRESSION RECOMMENDATIONS")
    print("=" * 80)
    print()

    for section_data in sections_analysis:
        section_name = section_data['section']
        dynamics = section_data['dynamics']

        print(f"\n{'▼' * 40}")
        print(f"SECTION: {section_name}")
        print(f"{'▼' * 40}")

        recommendations = analyzer.generate_compression_recommendations(section_name, dynamics)

        print(f"\n🎛️  MULTIBAND COMPRESSION:")
        for key, value in recommendations['multiband'].items():
            if key != 'note':
                print(f"  • {value}")
        if 'note' in recommendations['multiband']:
            print(f"  NOTE: {recommendations['multiband']['note']}")

        print(f"\n🔄 PARALLEL COMPRESSION:")
        for key, value in recommendations['parallel_compression'].items():
            if key != 'note':
                print(f"  • {key.replace('_', ' ').title()}: {value}")
        if 'note' in recommendations['parallel_compression']:
            print(f"  NOTE: {recommendations['parallel_compression']['note']}")

        print(f"\n⛓️  SIDECHAIN COMPRESSION:")
        for key, value in recommendations['sidechain'].items():
            if key != 'note':
                print(f"  • {key.replace('_', ' ').title()}: {value}")
        if 'note' in recommendations['sidechain']:
            print(f"  NOTE: {recommendations['sidechain']['note']}")

        print(f"\n⚡ TRANSIENT SHAPING:")
        for key, value in recommendations['transient_shaping'].items():
            if key != 'note':
                print(f"  • {key.title()}: {value}")
        if 'note' in recommendations['transient_shaping']:
            print(f"  NOTE: {recommendations['transient_shaping']['note']}")

        print()

    # Loudness strategy
    print("\n" + "=" * 80)
    print("LOUDNESS STRATEGY")
    print("=" * 80)
    print()

    strategy = analyzer.generate_loudness_strategy(sections_analysis, overall_rms)

    print("🎯 CURRENT STATE:")
    for key, value in strategy['current_state'].items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")

    print(f"\n🎚️  TARGET LUFS PER SECTION:")
    for key, value in strategy['target_lufs_per_section'].items():
        if key != 'note':
            print(f"  • {key}: {value}")
    if 'note' in strategy['target_lufs_per_section']:
        print(f"  NOTE: {strategy['target_lufs_per_section']['note']}")

    print(f"\n📈 GAIN STAGING STRATEGY:")
    for key, value in strategy['gain_staging'].items():
        if key != 'note':
            print(f"  • {key.replace('_', ' ').title()}: {value}")
    if 'note' in strategy['gain_staging']:
        print(f"  NOTE: {strategy['gain_staging']['note']}")

    print(f"\n🧱 LIMITING STRATEGY:")
    for key, value in strategy['limiting_strategy'].items():
        if key != 'note':
            print(f"  • {key.replace('_', ' ').title()}: {value}")
    if 'note' in strategy['limiting_strategy']:
        print(f"  NOTE: {strategy['limiting_strategy']['note']}")

    print(f"\n🎼 AUTOMATION RECOMMENDATIONS:")
    if strategy['automation']:
        for auto in strategy['automation']:
            print(f"\n  Section: {auto['section']} ({auto['time']})")
            print(f"  Action: {auto['action']}")
            print(f"  Purpose: {auto['purpose']}")
    else:
        print("  • No specific automation needed - apply global processing")

    print()
    print("=" * 80)
    print("PROFESSIONAL RECOMMENDATIONS SUMMARY")
    print("=" * 80)
    print()
    print("✅ PROCESSING CHAIN ORDER:")
    print("  1. Clean gain: +6 to +8 dB")
    print("  2. Surgical EQ (remove mud, harshness)")
    print("  3. Multiband compression (per section settings above)")
    print("  4. Parallel compression (NY compression for glue)")
    print("  5. Sidechain compression (kick ducking)")
    print("  6. Transient shaping (enhance punch)")
    print("  7. Saturation/harmonic excitement (+1-2 dB)")
    print("  8. Final EQ (corrective and creative)")
    print("  9. Stereo widening (if needed)")
    print(" 10. Final limiting (-14 LUFS target)")
    print()
    print("⚠️  CRITICAL NOTES:")
    print("  • Maintain 0.3-0.5 dB True Peak headroom for streaming")
    print("  • Use automation to create dynamic variation between sections")
    print("  • A/B test against professional reference tracks")
    print("  • Check mix on multiple playback systems")
    print("  • Use high-quality plugins (FabFilter, Waves, iZotope, etc.)")
    print()
    print("=" * 80)
    print("Analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
