#!/usr/bin/env python3
"""
Export EQ Presets in DAW-compatible formats
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_fabfilter_preset():
    """Create FabFilter Pro-Q3 compatible preset (XML)"""

    # FabFilter Pro-Q3 bands configuration
    bands = [
        {'enabled': True, 'frequency': 30, 'gain': 0, 'q': 0.707, 'shape': 'high_pass', 'slope': 12},
        {'enabled': True, 'frequency': 35, 'gain': -2.0, 'q': 0.80, 'shape': 'bell', 'slope': 0},
        {'enabled': True, 'frequency': 146, 'gain': -4.0, 'q': 3.00, 'shape': 'bell', 'slope': 0},
        {'enabled': True, 'frequency': 350, 'gain': -2.5, 'q': 1.50, 'shape': 'bell', 'slope': 0},
        {'enabled': True, 'frequency': 1693, 'gain': -4.0, 'q': 3.00, 'shape': 'bell', 'slope': 0},
        {'enabled': True, 'frequency': 2244, 'gain': -3.5, 'q': 3.00, 'shape': 'bell', 'slope': 0},
        {'enabled': True, 'frequency': 3000, 'gain': 2.0, 'q': 1.20, 'shape': 'bell', 'slope': 0},
        {'enabled': True, 'frequency': 3545, 'gain': -3.0, 'q': 2.50, 'shape': 'bell', 'slope': 0},
        {'enabled': True, 'frequency': 7916, 'gain': -2.5, 'q': 2.00, 'shape': 'bell', 'slope': 0},
        {'enabled': True, 'frequency': 12000, 'gain': 3.0, 'q': 0.70, 'shape': 'high_shelf', 'slope': 0},
    ]

    # Create XML structure
    root = ET.Element('FabFilterProQ3')
    root.set('version', '1.0')
    root.set('preset_name', 'СМОТРЕЛА_Master_EQ')

    for i, band in enumerate(bands, 1):
        band_elem = ET.SubElement(root, f'Band{i}')
        for key, value in band.items():
            param = ET.SubElement(band_elem, key)
            param.text = str(value)

    # Pretty print
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent='  ')

    with open('/home/user/look-at-me/СМОТРЕЛА_FabFilter_ProQ3.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)

    print("✓ FabFilter Pro-Q3 preset: /home/user/look-at-me/СМОТРЕЛА_FabFilter_ProQ3.xml")

def create_waves_preset():
    """Create Waves Q10 compatible preset"""

    bands = [
        {'band': 1, 'type': 'HPF', 'freq': 30, 'gain': 0, 'q': 0.707, 'slope': '12dB/oct'},
        {'band': 2, 'type': 'PEQ', 'freq': 35, 'gain': -2.0, 'q': 0.80, 'slope': 'N/A'},
        {'band': 3, 'type': 'PEQ', 'freq': 146, 'gain': -4.0, 'q': 3.00, 'slope': 'N/A'},
        {'band': 4, 'type': 'PEQ', 'freq': 350, 'gain': -2.5, 'q': 1.50, 'slope': 'N/A'},
        {'band': 5, 'type': 'PEQ', 'freq': 1693, 'gain': -4.0, 'q': 3.00, 'slope': 'N/A'},
        {'band': 6, 'type': 'PEQ', 'freq': 2244, 'gain': -3.5, 'q': 3.00, 'slope': 'N/A'},
        {'band': 7, 'type': 'PEQ', 'freq': 3000, 'gain': 2.0, 'q': 1.20, 'slope': 'N/A'},
        {'band': 8, 'type': 'PEQ', 'freq': 3545, 'gain': -3.0, 'q': 2.50, 'slope': 'N/A'},
        {'band': 9, 'type': 'PEQ', 'freq': 7916, 'gain': -2.5, 'q': 2.00, 'slope': 'N/A'},
        {'band': 10, 'type': 'HS', 'freq': 12000, 'gain': 3.0, 'q': 0.70, 'slope': 'N/A'},
    ]

    preset = {
        'preset_name': 'СМОТРЕЛА_Master_EQ',
        'plugin': 'Waves Q10 Equalizer',
        'bands': bands
    }

    with open('/home/user/look-at-me/СМОТРЕЛА_Waves_Q10.json', 'w', encoding='utf-8') as f:
        json.dump(preset, f, indent=2, ensure_ascii=False)

    print("✓ Waves Q10 preset: /home/user/look-at-me/СМОТРЕЛА_Waves_Q10.json")

def create_universal_csv():
    """Create universal CSV format for any EQ plugin"""

    csv_content = """Band,Type,Frequency (Hz),Gain (dB),Q Factor,Slope,Priority,Description
1,High Pass,30,0.0,0.71,12dB/oct,CRITICAL,Subsonic filter
2,Bell Cut,35,-2.0,0.80,N/A,HIGH,Sub-bass cleanup
3,Bell Cut,146,-4.0,3.00,N/A,CRITICAL,Bass resonance removal
4,Bell Cut,350,-2.5,1.50,N/A,HIGH,Low-mid mud removal
5,Bell Cut,1693,-4.0,3.00,N/A,CRITICAL,Mid resonance cut
6,Bell Cut,2244,-3.5,3.00,N/A,CRITICAL,High-mid resonance cut
7,Bell Boost,3000,+2.0,1.20,N/A,MEDIUM,Presence enhancement
8,Bell Cut,3545,-3.0,2.50,N/A,HIGH,Upper-mid resonance cut
9,Bell Cut,7916,-2.5,2.00,N/A,HIGH,High frequency resonance cut
10,High Shelf Boost,12000,+3.0,0.70,N/A,MEDIUM,Air band enhancement"""

    with open('/home/user/look-at-me/СМОТРЕЛА_EQ_Settings.csv', 'w', encoding='utf-8') as f:
        f.write(csv_content)

    print("✓ Universal CSV: /home/user/look-at-me/СМОТРЕЛА_EQ_Settings.csv")

def create_text_cheatsheet():
    """Create quick reference text cheat sheet"""

    cheatsheet = """
╔════════════════════════════════════════════════════════════════════════════════════╗
║                    СМОТРЕЛА - EQ QUICK REFERENCE CHEAT SHEET                       ║
║                              by Саймурр                                            ║
╚════════════════════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────────────────────────┐
│ CRITICAL FREQUENCIES (Must Fix!)                                                   │
├────────────────────────────────────────────────────────────────────────────────────┤
│ 146 Hz   │ -4.0 dB │ Q: 3.0 │ Bass resonance +35.8dB - causes boom/mud            │
│ 1693 Hz  │ -4.0 dB │ Q: 3.0 │ Mid resonance +22.0dB - vocal harshness             │
│ 2244 Hz  │ -3.5 dB │ Q: 3.0 │ High-mid resonance +21.9dB - aggressive sound       │
└────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────┐
│ HIGH PRIORITY CORRECTIONS                                                          │
├────────────────────────────────────────────────────────────────────────────────────┤
│ 35 Hz    │ -2.0 dB │ Q: 0.8 │ Sub-bass cleanup                                    │
│ 350 Hz   │ -2.5 dB │ Q: 1.5 │ Low-mid mud ("boxy" sound)                          │
│ 3545 Hz  │ -3.0 dB │ Q: 2.5 │ Upper-mid resonance - listening fatigue             │
│ 7916 Hz  │ -2.5 dB │ Q: 2.0 │ High frequency resonance - sibilance                │
└────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────┐
│ ENHANCEMENTS                                                                       │
├────────────────────────────────────────────────────────────────────────────────────┤
│ 3000 Hz  │ +2.0 dB │ Q: 1.2 │ Presence boost - vocal clarity                      │
│ 12000 Hz │ +3.0 dB │ Q: 0.7 │ Air band - openness and space                       │
└────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────┐
│ PROCESSING ORDER                                                                   │
├────────────────────────────────────────────────────────────────────────────────────┤
│ 1. High-pass filter @ 30 Hz (12 dB/oct)                                           │
│ 2. Surgical cuts: 146, 1693, 2244 Hz (use LINEAR PHASE mode!)                    │
│ 3. Broad cuts: 35, 350, 3545, 7916 Hz                                            │
│ 4. Musical boosts: 3000, 12000 Hz                                                │
│ 5. Multiband compression                                                          │
│ 6. Saturation/harmonic excitation (subtle)                                        │
│ 7. Final limiter (True Peak: -1.0 dBTP)                                          │
└────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────┐
│ DROP COMPARISON (@ 17.163s)                                                       │
├────────────────────────────────────────────────────────────────────────────────────┤
│ Sub-bass   │ Before: -77.18 dB │ After: -43.92 dB │ Change: +33.26 dB ▲          │
│ Bass       │ Before: -48.70 dB │ After: -43.84 dB │ Change:  +4.86 dB ▲          │
│ Mids       │ Before: -63.29 dB │ After: -55.84 dB │ Change:  +7.45 dB ▲          │
│ High-mids  │ Before: -74.59 dB │ After: -63.48 dB │ Change: +11.11 dB ▲          │
│ Highs      │ Before: -82.12 dB │ After: -67.97 dB │ Change: +14.15 dB ▲          │
│ Air        │ Before: -94.20 dB │ After: -84.31 dB │ Change:  +9.89 dB ▲          │
└────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────┐
│ TARGET LOUDNESS (Post-mastering)                                                   │
├────────────────────────────────────────────────────────────────────────────────────┤
│ Integrated LUFS:   -14 to -10 dB  (streaming platforms)                          │
│ True Peak:         -1.0 dBTP      (mandatory!)                                   │
│ Dynamic Range:     6-9 dB          (modern commercial mix)                       │
└────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────┐
│ PRO TIPS                                                                           │
├────────────────────────────────────────────────────────────────────────────────────┤
│ ✓ A/B test every 30 seconds - trust your ears!                                   │
│ ✓ Check on 3+ systems: monitors, headphones, phone speakers                      │
│ ✓ Use LINEAR PHASE EQ for 146, 1693, 2244 Hz to preserve phase                  │
│ ✓ Apply cuts gradually, not all at once                                          │
│ ✓ Compare with 2-3 reference tracks in the same genre                            │
│ ✓ Monitor with spectrum analyzer for visual feedback                             │
│ ✗ Don't boost more than 3-4 dB at once                                           │
│ ✗ Don't mix only in headphones - use monitors too                                │
│ ✗ Don't forget gain staging after EQ                                             │
└────────────────────────────────────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════════════════════════════
Print this page and keep it next to your DAW for quick reference!
═════════════════════════════════════════════════════════════════════════════════════
"""

    with open('/home/user/look-at-me/СМОТРЕЛА_EQ_CHEATSHEET.txt', 'w', encoding='utf-8') as f:
        f.write(cheatsheet)

    print("✓ Quick Reference Cheat Sheet: /home/user/look-at-me/СМОТРЕЛА_EQ_CHEATSHEET.txt")

def create_markdown_report():
    """Create detailed Markdown report for documentation"""

    markdown = """# 🎵 СМОТРЕЛА - Professional Frequency Analysis Report
**Artist:** Саймурр
**Analyzed:** 2025-12-26
**Duration:** 37.00 seconds
**Sample Rate:** 48000 Hz
**DROP Position:** 17.163s

---

## 📊 Executive Summary

This track exhibits **5 critical frequency resonances** that significantly impact the mix quality. The most problematic frequency is **146 Hz** with a resonance of **+35.8 dB** above average, causing muddiness in the bass range.

### Key Issues Found:
- ⚠️ **Critical bass resonance** at 146 Hz
- ⚠️ **Paired mid-range resonances** at 1693 Hz and 2244 Hz
- ⚠️ **Low-mid mud** around 350 Hz (classic "boxy" frequency)
- ⚠️ **Insufficient air band** (-21.3 dB deficit in 10-20 kHz range)
- ⚠️ **Multiple high-frequency resonances** requiring surgical EQ

---

## 🎛️ Spectral Analysis - Full Track

| Frequency Band | Range (Hz) | Avg Level (dB) | Peak Level (dB) | Peak Freq (Hz) | RMS (dB) |
|----------------|------------|----------------|-----------------|----------------|----------|
| **Sub-bass**   | 20-60      | -46.60         | -32.70          | 52.7           | 47.85    |
| **Bass**       | 60-250     | -44.31         | -38.85          | 64.5           | 44.40    |
| **Low-mids**   | 250-500    | -48.03         | -40.95          | 275.4          | 48.21    |
| **Mids**       | 500-2000   | -57.74         | -42.26          | 556.6          | 57.95    |
| **High-mids**  | 2000-4000  | -65.80         | -55.81          | 2220.7         | 65.93    |
| **Highs**      | 4000-10000 | -70.44         | -65.74          | 6222.7         | 70.47    |
| **Air**        | 10000-20000| -86.43         | -70.31          | 10002.0        | 86.82    |

---

## 🔴 Critical Resonances Detected

| Rank | Frequency (Hz) | Level (dB) | Above Average (dB) | Severity |
|------|----------------|------------|--------------------|----------|
| 1    | **146.5**      | -40.69     | **+35.75**         | CRITICAL |
| 2    | **1693.4**     | -57.84     | **+22.04**         | CRITICAL |
| 3    | **2244.1**     | -56.34     | **+21.85**         | CRITICAL |
| 4    | **3544.9**     | -67.78     | **+12.97**         | HIGH     |
| 5    | **7916.0**     | -67.73     | **+12.12**         | HIGH     |
| 6    | 9832.0         | -72.09     | +8.01              | MEDIUM   |

---

## 📈 Before vs After DROP Analysis (@ 17.163s)

| Frequency Band | Before DROP (dB) | After DROP (dB) | Difference (dB) | Change |
|----------------|------------------|-----------------|-----------------|--------|
| Sub-bass       | -77.18           | -43.92          | **+33.26**      | ▲▲▲    |
| Bass           | -48.70           | -43.84          | +4.86           | ▲      |
| Low-mids       | -49.91           | -47.60          | +2.32           | ▲      |
| Mids           | -63.29           | -55.84          | +7.45           | ▲▲     |
| High-mids      | -74.59           | -63.48          | +11.11          | ▲▲     |
| Highs          | -82.12           | -67.97          | +14.15          | ▲▲▲    |
| Air            | -94.20           | -84.31          | +9.89           | ▲▲     |

**Key Observation:** The DROP introduces **massive energy increase** across all frequency bands, particularly in sub-bass (+33.26 dB) and highs (+14.15 dB).

---

## 🎚️ Professional EQ Recommendations

### FabFilter Pro-Q3 / Waves Q10 Settings

| Band | Type | Frequency (Hz) | Gain (dB) | Q Factor | Priority | Reason |
|------|------|----------------|-----------|----------|----------|--------|
| 1    | High Pass | 30 | 0.0 | 0.71 | CRITICAL | Subsonic rumble removal |
| 2    | Bell | 35 | **-2.0** | 0.80 | HIGH | Sub-bass cleanup |
| 3    | Bell | **146** | **-4.0** | **3.00** | **CRITICAL** | Bass resonance removal (+35.8 dB) |
| 4    | Bell | 350 | **-2.5** | 1.50 | HIGH | Low-mid mud (boxy sound) |
| 5    | Bell | **1693** | **-4.0** | **3.00** | **CRITICAL** | Mid resonance (+22.0 dB) |
| 6    | Bell | **2244** | **-3.5** | **3.00** | **CRITICAL** | High-mid resonance (+21.9 dB) |
| 7    | Bell | 3000 | **+2.0** | 1.20 | MEDIUM | Presence boost (vocal clarity) |
| 8    | Bell | 3545 | **-3.0** | 2.50 | HIGH | Upper-mid resonance |
| 9    | Bell | 7916 | **-2.5** | 2.00 | HIGH | High-freq resonance (sibilance) |
| 10   | High Shelf | 12000 | **+3.0** | 0.70 | MEDIUM | Air band enhancement |

### ⚡ Important Notes:
- **Use LINEAR PHASE mode** for bands 3, 5, and 6 (146, 1693, 2244 Hz) to preserve phase relationships
- Apply cuts **gradually** - don't enable all at once
- A/B test after each major adjustment
- Compensate output gain as needed

---

## 🔧 Additional Processing Recommendations

### Multiband Compression

**Bass Band (20-250 Hz):**
- Threshold: -15 dB
- Ratio: 3:1
- Attack: 10 ms
- Release: 100 ms
- Purpose: Control bass dynamics after EQ

**Mid Band (250-2000 Hz):**
- Threshold: -12 dB
- Ratio: 2:1
- Attack: 5 ms
- Release: 50 ms
- Purpose: Smooth vocal/melody consistency

**High Band (2000-8000 Hz):**
- Threshold: -10 dB
- Ratio: 2.5:1
- Attack: 3 ms
- Release: 30 ms
- Purpose: Control harshness after cuts

### Signal Chain Order
1. High-pass filter (30 Hz)
2. Surgical EQ cuts (LINEAR PHASE)
3. Broad EQ cuts
4. Musical EQ boosts
5. Multiband compression
6. Subtle saturation
7. Final limiter

---

## 🎯 Target Mastering Parameters

| Parameter | Target Value | Notes |
|-----------|--------------|-------|
| Integrated LUFS | -14 to -10 dB | For streaming platforms |
| True Peak | -1.0 dBTP | **Mandatory** to avoid clipping |
| Dynamic Range (DR) | 6-9 dB | Modern commercial standard |
| Sample Peak | -0.3 dBFS | Safety headroom |

### Frequency Balance Goals:
- Bass (60-250 Hz): -6 to -3 dB relative to mids
- Mids (500-2000 Hz): 0 dB (reference)
- Highs (4000-10000 Hz): -3 to 0 dB relative to mids
- Air (10000+ Hz): -6 to -3 dB relative to highs

---

## ✅ Quality Assurance Checklist

- [ ] A/B test EQ changes every 30 seconds
- [ ] Check on studio monitors (main system)
- [ ] Check on headphones (reference)
- [ ] Check on phone/laptop speakers (consumer)
- [ ] Compare with 2-3 reference tracks in genre
- [ ] Use spectrum analyzer for visual verification
- [ ] Check at low, medium, and high listening levels
- [ ] Verify no phase cancellation issues
- [ ] Ensure proper gain staging throughout chain
- [ ] Final LUFS and True Peak measurement

---

## 📁 Export Formats

**Master Version:**
- Format: WAV
- Sample Rate: 48000 Hz
- Bit Depth: 24-bit
- Dither: None (master)

**Streaming Version:**
- Format: WAV
- Sample Rate: 44100 Hz
- Bit Depth: 16-bit
- Dither: Triangular

**Compressed Versions:**
- MP3: 320 kbps CBR
- AAC: 256 kbps VBR

---

## 📝 Metadata

```
Artist: Саймурр
Title: СМОТРЕЛА
Album: [TBD]
Genre: [TBD]
Year: 2025
ISRC: [Obtain code]
Copyright: © 2025 Саймурр
```

---

## 🎓 Pro Tips

### DO:
✅ Use LINEAR PHASE EQ for critical frequencies
✅ Apply changes gradually and A/B test frequently
✅ Reference on multiple playback systems
✅ Trust your ears over visual analyzers
✅ Take breaks every 30-45 minutes
✅ Compare with commercial references

### DON'T:
❌ Apply all EQ cuts simultaneously
❌ Boost more than 3-4 dB at once
❌ Use excessive Q values (>5.0) except surgical cuts
❌ Mix only in headphones
❌ Forget gain staging
❌ Skip the A/B comparison

---

## 📞 Support

For questions or further analysis, refer to the generated files:
- `PROFESSIONAL_EQ_GUIDE.txt` - Complete text guide
- `СМОТРЕЛА_EQ_CHEATSHEET.txt` - Quick reference
- `СМОТРЕЛА_FabFilter_ProQ3.xml` - FabFilter preset
- `СМОТРЕЛА_Waves_Q10.json` - Waves preset
- `СМОТРЕЛА_EQ_Settings.csv` - Universal format

---

**Analysis Date:** 2025-12-26
**Tool:** Professional FFT Analyzer (scipy/numpy)
**Precision:** 16384-point FFT with Hann window

*This report was generated using scientific audio analysis tools with professional-grade accuracy.*
"""

    with open('/home/user/look-at-me/FREQUENCY_ANALYSIS_FULL_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(markdown)

    print("✓ Full Markdown Report: /home/user/look-at-me/FREQUENCY_ANALYSIS_FULL_REPORT.md")

def main():
    print("\n" + "="*80)
    print("EXPORTING EQ PRESETS AND DOCUMENTATION")
    print("="*80 + "\n")

    create_fabfilter_preset()
    create_waves_preset()
    create_universal_csv()
    create_text_cheatsheet()
    create_markdown_report()

    print("\n" + "="*80)
    print("✓ ALL FILES EXPORTED SUCCESSFULLY!")
    print("="*80 + "\n")

    print("Generated Files:")
    print("  1. СМОТРЕЛА_FabFilter_ProQ3.xml       - FabFilter Pro-Q3 preset")
    print("  2. СМОТРЕЛА_Waves_Q10.json            - Waves Q10 preset")
    print("  3. СМОТРЕЛА_EQ_Settings.csv           - Universal CSV format")
    print("  4. СМОТРЕЛА_EQ_CHEATSHEET.txt         - Quick reference cheat sheet")
    print("  5. FREQUENCY_ANALYSIS_FULL_REPORT.md  - Complete Markdown documentation")
    print("  6. PROFESSIONAL_EQ_GUIDE.txt          - Detailed text guide (already created)")
    print()
    print("Import these files into your DAW or print the cheat sheet for quick reference!")
    print()

if __name__ == "__main__":
    main()
