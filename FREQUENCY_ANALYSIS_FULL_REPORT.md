# 🎵 СМОТРЕЛА - Professional Frequency Analysis Report
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
