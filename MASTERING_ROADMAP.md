# MASTERING ROADMAP: SmotrelaА.wav
## Professional Dynamics & Loudness Strategy

---

## 📊 CURRENT STATE ANALYSIS

**File:** SmotrelaА.wav
**Duration:** 84.72 seconds (1:25)
**Sample Rate:** 48kHz

### Critical Metrics:
- **Current RMS:** -22.14 dB (Very quiet - needs +8 dB gain)
- **Current LUFS:** -24.95 LUFS (Target: -14 LUFS)
- **Peak Level:** 0.00 dB (Already normalized to ceiling)
- **Headroom:** 0 dB (No headroom - track is at 0dBFS)
- **Crest Factor:** 22.14 dB (Very dynamic)
- **Dynamic Range:** 22.3 dB (Wide dynamics)
- **Transient Density:** 3.64 transients/second

### ⚠️ CRITICAL ISSUE:
Track is already normalized to 0dBFS but RMS is extremely low at -22dB. This indicates:
1. The mix has very wide dynamics
2. Peak limiting is needed before further processing
3. Gain must be applied carefully with compression/limiting

---

## 🎵 TRACK STRUCTURE

| Section | Time Range | Duration | RMS Level | Energy | Priority |
|---------|-----------|----------|-----------|--------|----------|
| **Intro** | 0:00 - 0:17 | 17.0s | -26.08 dB | Low 📉 | Preserve dynamics |
| **Verse 1** | 0:17 - 0:28 | 10.7s | -18.53 dB | HIGH ⚡ | Maximum impact |
| **Pre-Chorus 1** | 0:28 - 0:38 | 10.4s | -20.14 dB | HIGH ⚡ | Build energy |
| **Chorus 1** | 0:38 - 0:42 | 4.1s | -20.83 dB | Above Average 📈 | Peak loudness |
| **Verse 2** | 0:42 - 0:47 | 4.5s | -22.59 dB | Average 📊 | Contrast |
| **Pre-Chorus 2** | 0:47 - 0:51 | 4.6s | -22.00 dB | Above Average 📈 | Build tension |
| **Chorus 2** | 0:51 - 0:55 | 4.0s | -22.76 dB | Average 📊 | Peak loudness |
| **Bridge** | 0:55 - 1:02 | 6.4s | -21.48 dB | Above Average 📈 | Dynamic variation |
| **Chorus 3** | 1:02 - 1:22 | 19.9s | -24.62 dB | Low 📉 | Extended resolution |
| **Outro** | 1:22 - 1:25 | 3.1s | -33.86 dB | Low 📉 | Fade out |

### 🔍 Key Observations:
1. **Verse 1 is the loudest section** (-18.53 dB) - energy peak early in track
2. **Outro is extremely quiet** (-33.86 dB) - intentional fade
3. **Unusual structure:** Energy decreases after first verse (non-standard for pop/dance)
4. **Short chorus sections** (4 seconds) - quick impact moments
5. **Long Chorus 3** (20 seconds) - extended finale

---

## 🎚️ MASTERING PROCESSING CHAIN

### CHAIN ORDER (Critical - Follow Exactly):

```
INPUT → [1] Surgical EQ → [2] Multiband Compression → [3] Parallel Compression →
[4] Sidechain Compression → [5] Transient Shaping → [6] Saturation →
[7] Creative EQ → [8] Stereo Enhancement → [9] Final Limiting → OUTPUT
```

---

## 1️⃣ SURGICAL EQ (Corrective)

**Plugin:** FabFilter Pro-Q 3 / iZotope Ozone EQ

**Settings:**
```
High-pass filter: 30 Hz, 12 dB/octave (clean up subsonic rumble)
Cut 1: 200-300 Hz, -2 to -3 dB, Q=1.5 (reduce mud)
Cut 2: 2-3 kHz, -1 to -2 dB, Q=2.0 (reduce harshness if present)
Boost: 8-10 kHz, +1 to +2 dB, shelf (add air)
```

**Purpose:** Remove problematic frequencies before compression

---

## 2️⃣ MULTIBAND COMPRESSION (Dynamic Control)

**Plugin:** FabFilter Pro-MB / Waves C6 / iZotope Ozone Dynamics

### INTRO (0:00-0:17) - Gentle Dynamic Control
```
LOW (20-120 Hz):
  Ratio: 2:1 | Threshold: -18 dB | Attack: 30ms | Release: 200ms

MID (120-2000 Hz):
  Ratio: 1.5:1 | Threshold: -15 dB | Attack: 15ms | Release: 100ms

HIGH (2k-20k Hz):
  Ratio: 1.3:1 | Threshold: -12 dB | Attack: 5ms | Release: 50ms
```

### VERSE 1, 2 (0:17-0:28, 0:42-0:47) - Balanced Compression
```
LOW (20-120 Hz):
  Ratio: 3:1 | Threshold: -20 dB | Attack: 20ms | Release: 180ms

MID (120-2000 Hz):
  Ratio: 2.5:1 | Threshold: -16 dB | Attack: 10ms | Release: 90ms

HIGH (2k-20k Hz):
  Ratio: 2:1 | Threshold: -14 dB | Attack: 3ms | Release: 50ms
```

### PRE-CHORUS & CHORUS (0:28-0:42, 0:47-0:55) - Aggressive Control
```
LOW (20-120 Hz):
  Ratio: 4:1 | Threshold: -20 dB | Attack: 10ms | Release: 150ms

MID (120-2000 Hz):
  Ratio: 3:1 | Threshold: -16 dB | Attack: 5ms | Release: 80ms

HIGH (2k-20k Hz):
  Ratio: 2.5:1 | Threshold: -14 dB | Attack: 1ms | Release: 40ms
```

**Automate:** Switch between these presets based on section changes

---

## 3️⃣ PARALLEL COMPRESSION (New York Style)

**Plugin:** Waves SSL Comp / UAD 1176 / FabFilter Pro-C 2

### Settings by Section:

**For High Energy Sections (Verse 1, Pre-Chorus, Chorus):**
```
Ratio: 8:1 to 10:1 (heavy!)
Threshold: -35 to -40 dB (catches everything)
Attack: 1-3ms (fast - catch transients)
Release: 50-100ms (medium-fast)
Makeup Gain: +10 to +15 dB
Mix: 20-30% wet blend
```

**For Low Energy Sections (Intro, Verse 2, Bridge, Outro):**
```
Ratio: 4:1 to 6:1 (moderate)
Threshold: -30 dB
Attack: 5-10ms
Release: 100-150ms
Makeup Gain: +8 to +12 dB
Mix: 15-25% wet blend
```

**Purpose:** Add thickness and glue without squashing dynamics

---

## 4️⃣ SIDECHAIN COMPRESSION (Ducking)

**Plugin:** FabFilter Pro-C 2 / Waves C1 (sidechain enabled)

### Kick-to-Bass Ducking:
```
Trigger: Kick drum frequency (50-100 Hz bandpass)
Ratio: 6:1
Threshold: Adjust to taste (-6 to -10 dB)
Attack: 0.1ms (instant)
Release: 150ms (medium)
Gain Reduction: 4-6 dB
```

### Kick-to-Synths/Pads Ducking:
```
Trigger: Kick drum
Ratio: 3:1
Threshold: -8 dB
Attack: 0.1ms
Release: 50ms (fast)
Gain Reduction: 2-3 dB
```

**Apply to:** Verse 1, Pre-Chorus, Chorus sections (where kick is prominent)

---

## 5️⃣ TRANSIENT SHAPING (Punch Enhancement)

**Plugin:** SPL Transient Designer / Waves Trans-X / iZotope Ozone Dynamics

### Verse 1 & Chorus Sections:
```
DRUMS:
  Attack: +3 to +6 dB (enhance punch)
  Sustain: -2 dB (reduce tail)

BASS:
  Attack: +2 dB (add definition)
  Sustain: 0 dB (preserve tone)

SYNTHS:
  Attack: +1 to +3 dB (add clarity)
  Sustain: -1 dB
```

### Other Sections:
```
DRUMS:
  Attack: +1 to +3 dB (moderate)
  Sustain: -1 dB

BASS:
  Attack: +1 dB
  Sustain: 0 dB
```

**Purpose:** Make kicks/snares cut through without raising overall level

---

## 6️⃣ SATURATION (Harmonic Enhancement)

**Plugin:** FabFilter Saturn 2 / Decapitator / Waves J37

```
Type: Tape or Tube (warm character)
Drive: 10-20% (subtle)
Mix: 30-50%
Output: Compensate -1 to -2 dB
```

**Multiband Saturation (Advanced):**
```
LOW (20-200 Hz): Tape saturation, 15% drive
MID (200-2k Hz): Tube saturation, 10% drive
HIGH (2k-20k Hz): Clean/minimal, 5% drive
```

**Gain:** Expect +1 to +2 dB from harmonic content

---

## 7️⃣ CREATIVE EQ (Character)

**Plugin:** Pultec EQP-1A / API 550 / SSL EQ

```
Low shelf (100 Hz): +1 to +2 dB (warmth)
Presence (3-4 kHz): +1 dB (clarity)
High shelf (10 kHz): +1.5 to +2 dB (air)
```

**Purpose:** Add character and final tonal shaping

---

## 8️⃣ STEREO ENHANCEMENT (Optional)

**Plugin:** iZotope Ozone Imager / Waves S1

```
LOW (below 200 Hz): 0% stereo (keep mono)
MID (200-2k Hz): 100-120% width
HIGH (2k-20k Hz): 120-140% width
```

**⚠️ WARNING:** Check mono compatibility! Many streaming services convert to mono.

---

## 9️⃣ FINAL LIMITING (Loudness Maximization)

**Plugin:** FabFilter Pro-L 2 / iZotope Ozone Maximizer / Waves L2

### Target Settings:
```
Algorithm: Modern (Pro-L 2) / IRC IV (Ozone)
Ceiling: -0.5 dB True Peak (streaming safety)
Lookahead: 5ms
Oversampling: 4x or 8x (prevents aliasing)
Release: Auto (or 50-100ms)
```

### Target LUFS by Section (Use Automation):

| Section | Target LUFS | Threshold | Expected GR |
|---------|-------------|-----------|-------------|
| Intro | -16.0 LUFS | -8 dB | 3-4 dB |
| Verse 1 | -15.0 LUFS | -6 dB | 4-5 dB |
| Pre-Chorus | -14.0 LUFS | -5 dB | 5-6 dB |
| **Chorus** | **-13.0 LUFS** | **-4 dB** | **6-8 dB** |
| Verse 2 | -15.0 LUFS | -6 dB | 4-5 dB |
| Bridge | -14.0 LUFS | -5 dB | 5-6 dB |
| Chorus 3 | -14.0 LUFS | -5 dB | 5-6 dB |
| Outro | -16.0 LUFS | -8 dB | 2-3 dB |

### Overall Target:
```
Integrated LUFS: -14.0 LUFS (Spotify/YouTube standard)
True Peak: -0.5 dB
Dynamic Range: 6-8 dB (competitive but not over-compressed)
```

---

## 🎼 AUTOMATION RECOMMENDATIONS

### Volume Automation (Pre-Limiter):

```
0:00 - 0:04 (Intro fade-in):
  Start: -6 dB → End: 0 dB (smooth curve)

0:17 - 0:28 (Verse 1 - LOUDEST SECTION):
  Reduce by -0.5 to -1 dB (prevent over-limiting)

0:28 - 0:38 (Pre-Chorus 1):
  Boost by +0.5 dB (build energy)

0:38 - 0:42 (Chorus 1):
  Boost by +1 to +2 dB (peak impact)

0:42 - 0:47 (Verse 2):
  Reduce by -1 dB (contrast)

0:47 - 0:51 (Pre-Chorus 2):
  Boost by +0.5 dB

0:51 - 0:55 (Chorus 2):
  Boost by +1 to +2 dB

0:55 - 1:02 (Bridge):
  Reduce by -1 to -2 dB (create tension/dynamics)

1:02 - 1:22 (Chorus 3):
  Gradual boost from 0 dB to +1 dB (build to climax)

1:22 - 1:25 (Outro):
  Fade: 0 dB → -12 dB (smooth ending)
```

### Limiter Drive Automation:
```
Chorus sections: +1 dB drive increase
Bridge: -1 dB drive decrease
```

---

## 📈 GAIN STAGING STRATEGY

### Total Gain Budget: +8.1 dB

Distributed as follows:

| Stage | Gain | Cumulative |
|-------|------|------------|
| 1. Initial Clean Gain | +0 dB | +0 dB |
| 2. Multiband Compression | +2.0 dB (makeup) | +2.0 dB |
| 3. Parallel Compression | +2.0 dB (blend) | +4.0 dB |
| 4. Saturation | +1.5 dB | +5.5 dB |
| 5. Creative EQ | +0.5 dB | +6.0 dB |
| 6. Final Limiting | +2.0 to +4.0 dB | +8-10 dB |

**⚠️ CRITICAL:** Do NOT add clean gain at the start! Track is already at 0dBFS.
Start with compression to control peaks, then add gain.

---

## ✅ QUALITY CONTROL CHECKLIST

### Before Export:
- [ ] Check True Peak meter: Must be ≤ -0.5 dB
- [ ] Integrated LUFS: -14.0 ± 0.5 LUFS
- [ ] No digital clipping (red lights)
- [ ] Mono compatibility check (sum to mono, listen for phase issues)
- [ ] Low-end focus: Check bass clarity in mono
- [ ] A/B against reference tracks (same genre)
- [ ] Listen on multiple systems:
  - [ ] Studio monitors
  - [ ] Headphones
  - [ ] Phone speaker
  - [ ] Car stereo
  - [ ] Laptop speakers

### Measurement Tools:
- [ ] iZotope Insight / Youlean Loudness Meter (LUFS)
- [ ] True Peak meter
- [ ] Spectrum analyzer (check for holes/excessive buildup)
- [ ] Phase correlation meter (stereo field)

---

## 🎯 COMPETITIVE LOUDNESS TARGETS

### Streaming Platforms:

| Platform | Target LUFS | Notes |
|----------|-------------|-------|
| **Spotify** | -14 LUFS | Will turn down if louder |
| **Apple Music** | -16 LUFS | More dynamic preferred |
| **YouTube** | -14 LUFS | Standard target |
| **Tidal** | -14 LUFS | HiFi platform |
| **SoundCloud** | -14 LUFS | Recommended |
| **CD/Download** | -9 to -11 LUFS | Can be louder (optional) |

**Recommendation:** Master to -14 LUFS for universal compatibility.

---

## ⚠️ CRITICAL WARNINGS

### DO NOT:
1. ❌ Apply clean gain before compression (track is already at 0dBFS)
2. ❌ Over-limit to achieve loudness (aim for 3-6 dB GR max, up to 8 dB in chorus)
3. ❌ Boost low-end excessively (check in mono - bass should be clear)
4. ❌ Widen stereo below 200 Hz (causes phase issues)
5. ❌ Skip reference track comparison
6. ❌ Export without checking True Peak

### DO:
1. ✅ Use automation for dynamic variation
2. ✅ Maintain 0.3-0.5 dB True Peak headroom
3. ✅ Check mix on phone speaker (most people listen there)
4. ✅ Take listening breaks every 30-45 minutes
5. ✅ Save multiple versions with different LUFS targets
6. ✅ Use high-quality dithering when exporting to 16-bit

---

## 📁 EXPORT SETTINGS

### Streaming Master:
```
Format: WAV
Bit Depth: 24-bit (or 16-bit with dither)
Sample Rate: 48 kHz (match source)
Dither: POW-r #2 or Apogee UV22HR (if 16-bit)
True Peak Limiting: -0.5 dB
Target LUFS: -14.0
```

### High-Quality Archive:
```
Format: WAV
Bit Depth: 24-bit or 32-bit float
Sample Rate: 48 kHz
No limiting/processing
```

### Optional Loud Master (CD):
```
Same as streaming but:
Target LUFS: -9 to -11
True Peak: -0.3 dB
```

---

## 🔧 RECOMMENDED PLUGINS

### Essential:
- **EQ:** FabFilter Pro-Q 3, iZotope Ozone EQ
- **Multiband Comp:** FabFilter Pro-MB, Waves C6
- **Compressor:** FabFilter Pro-C 2, SSL G-Master Bus Comp
- **Limiter:** FabFilter Pro-L 2, iZotope Ozone Maximizer
- **Metering:** Youlean Loudness Meter, iZotope Insight

### Optional (Character):
- **Saturation:** Decapitator, FabFilter Saturn 2
- **Transient:** SPL Transient Designer, Waves Trans-X
- **Vintage:** UAD Neve/SSL/API emulations

---

## 📊 EXPECTED RESULTS

### Before Mastering:
- RMS: -22.14 dB
- LUFS: -24.95 LUFS
- Peak: 0.00 dB
- Dynamic Range: 22.3 dB

### After Mastering:
- RMS: -14.0 dB (+8 dB increase)
- LUFS: -14.0 LUFS (+11 LUFS increase)
- Peak: -0.5 dB True Peak
- Dynamic Range: 6-8 dB (competitive)
- Clarity: Enhanced
- Punch: Significantly improved
- Commercial viability: High

---

## 🎓 FINAL NOTES

1. **This is a dynamic track** with wide variation in energy. Preserve some of that character - don't over-compress.

2. **Verse 1 is the loudest section** at -18.53 dB. This is unusual. Consider if this is intentional or if automation is needed to balance sections.

3. **The outro fade** is extreme (-33 dB). Ensure this is intentional. May need to extend fade time.

4. **Short chorus sections** (4 seconds) mean transitions are critical. Use smooth automation curves.

5. **Reference tracks:** Find 3-5 professionally mastered tracks in the same genre and match their tonal balance and loudness.

6. **Mastering is iterative:** Don't expect perfection on first pass. Compare versions, sleep on it, return with fresh ears.

---

## 📞 NEXT STEPS

1. Load track into DAW
2. Set up processing chain (save as template)
3. Configure section markers based on structure table
4. Apply settings section by section with automation
5. Fine-tune based on listening tests
6. Export and verify with loudness meter
7. Test on multiple playback systems
8. Deliver final master

---

**Mastering Engineer:** Follow this roadmap as a guide, but trust your ears above all measurements.

**Good luck! 🎵**
