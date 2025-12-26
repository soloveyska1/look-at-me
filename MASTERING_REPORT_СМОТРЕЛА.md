# PROFESSIONAL MASTERING REPORT
## Track: "СМОТРЕЛА" by Саймурр

**Engineer Level:** Sterling Sound / Abbey Road Standards
**Date:** 2025-12-26
**File:** `/home/user/look-at-me/СМОТРЕЛА_teaser.wav`

---

## EXECUTIVE SUMMARY

This 37-second teaser requires **moderate mastering** to reach professional streaming standards. The mix has excellent headroom (0.45 dB) and good dynamics (16 dB DR), but needs loudness optimization (+7.6 dB gain), stereo balance correction (0.83 dB L/R imbalance), and careful enhancement of the DROP moment at 17.163s.

**Overall Grade:** B+ (Good mix, ready for mastering)

---

## 1. HEADROOM ANALYSIS ✅

### Current Status
- **Headroom:** 0.45 dB (both channels)
- **Peak Level:** -0.45 dBFS (L/R)
- **True Peak:** -0.21 dBTP

### Verdict
**EXCELLENT** - This is the sweet spot for mastering. DO NOT reduce levels further.

### Why This Matters
- 0.4-0.5 dB headroom prevents accidental clipping during processing
- Gives limiter proper range to work without distortion
- Allows for safe intersample peak control

### Action Required
✅ **NONE** - Proceed directly to mastering chain

---

## 2. STEREO BALANCE CORRECTION ⚠️

### Current Status
- **Left Channel RMS:** -14.52 dBFS
- **Right Channel RMS:** -15.35 dBFS
- **Imbalance:** 0.83 dB (RIGHT channel quieter)
- **Stereo Correlation:** 0.58 (good stereo width)
- **Stereo Width Ratio:** 0.52 (moderate width)

### Problem
0.83 dB imbalance is **noticeable** on headphones and will cause image shift to the left.

### Solution - THREE OPTIONS:

#### Option A: Balance Plugin (Recommended)
```
Plugin: iZotope Ozone Imager / Waves S1 / Goodhertz MiddleEQ
Action: Boost RIGHT channel by +0.42 dB
       (or reduce LEFT by -0.42 dB)
```

#### Option B: Stereo Width Adjustment
```
Plugin: Mid/Side EQ
Action: Reduce SIDE channel by -1.5 dB
       This will center the image naturally
```

#### Option C: Pre-mastering Bounce Correction
```
DAW: Adjust pan/balance before bounce
Action: Pan entire track 2% right
       OR use channel strip L/R gain offset
```

### Verification
After correction, check with:
- Correlation meter (should remain 0.55-0.65)
- Mono compatibility test (no phase cancellation)
- Headphone listening (center image)

---

## 3. LOUDNESS TARGETS (LUFS) 🎚️

### Current Measurements
- **Integrated LUFS:** -15.6 LUFS
- **Crest Factor:** 14.5 dB (very dynamic)
- **Dynamic Range:** 16.0 dB (excellent preservation)

### Target Analysis

| Platform | Target LUFS | Current Delta | Streaming Behavior |
|----------|-------------|---------------|-------------------|
| Spotify | -14 LUFS | -1.6 dB quiet | Will turn UP (ideal!) |
| YouTube | -13 LUFS | -2.6 dB quiet | Will turn UP |
| Apple Music | -16 LUFS | +0.4 dB loud | Will turn DOWN slightly |
| Tidal/Qobuz | -14 LUFS | -1.6 dB quiet | Will turn UP |
| **EDM/Club Master** | **-8 LUFS** | **-7.6 dB quiet** | **Needs serious limiting** |

### Recommended Strategy

#### For STREAMING Platforms (Conservative Master)
```
Target: -14 LUFS integrated
True Peak Ceiling: -1.0 dBTP
Gain Required: +1.6 dB (very gentle limiting)

Why: Streaming platforms normalize anyway
     Preserves dynamics
     Prevents distortion on compression codecs
```

#### For ELECTRONIC/EDM/CLUB Play (Aggressive Master)
```
Target: -8 LUFS integrated
True Peak Ceiling: -0.5 dBTP
Gain Required: +7.6 dB (heavy limiting)

Why: Competitive loudness for genre
     Maximum impact on club systems
     Maintains punch against other EDM tracks
```

### RECOMMENDATION: Dual Master Approach
**Create TWO versions:**
1. **Streaming Master:** -14 LUFS (gentle, dynamic)
2. **Download/Promo Master:** -8 LUFS (loud, competitive)

This gives you options for different platforms.

---

## 4. EQ RECOMMENDATIONS (Surgical + Enhancement) 🎛️

### Spectral Analysis Results

| Frequency Band | Current Peak | Current Avg | Status |
|----------------|--------------|-------------|--------|
| Sub-Bass (20-60 Hz) | -38.2 dB | -71.7 dB | ⚠️ Weak |
| Bass (60-250 Hz) | -47.2 dB | -66.6 dB | ⚠️ Weak |
| Low-Mids (250-500 Hz) | -46.1 dB | -70.7 dB | ⚠️ Weak |
| Mids (500-2k Hz) | -50.5 dB | -79.5 dB | ⚠️ Weak |
| High-Mids (2-4k Hz) | -67.3 dB | -87.4 dB | ⚠️ Very Weak |
| Presence (4-6k Hz) | -78.5 dB | -91.6 dB | ⚠️ Very Weak |
| Brilliance (6-20k Hz) | -71.7 dB | -104.3 dB | ⚠️ Very Weak |

**Interpretation:** This spectrum shows a LOW-FREQUENCY DOMINANT mix, typical of dramatic/cinematic electronic music. The high end is significantly rolled off.

### EQ Strategy: 3-Stage Process

#### STAGE 1: Linear Phase EQ (Surgical - Corrective)
**Plugin:** FabFilter Pro-Q3 (Linear Phase Zero-Latency)

```
1. High-Pass Filter
   Frequency: 25 Hz
   Slope: 24 dB/oct (Brick Wall)
   Purpose: Remove subsonic rumble, protect bass speakers

2. Sub-Bass Clean-Up
   Frequency: 35-40 Hz
   Type: Bell
   Gain: -1.0 dB
   Q: 3.0 (narrow)
   Purpose: Remove problematic low-end resonance

3. Mud Reduction
   Frequency: 180 Hz
   Type: Bell
   Gain: -0.8 dB
   Q: 1.2 (moderate)
   Purpose: Clean up muddy low-mids

4. Boxiness Reduction
   Frequency: 350 Hz
   Type: Bell
   Gain: -0.5 dB
   Q: 1.5
   Purpose: Reduce boxy, hollow tone

5. Nasal Frequency Check
   Frequency: 800-1200 Hz
   Type: Bell
   Gain: 0 dB (SWEEP to find problem)
   Q: 4.0 (very narrow)
   Purpose: Find and remove harsh nasal tones
   Action: Sweep, identify, cut by -1 to -3 dB
```

#### STAGE 2: Standard EQ (Enhancement - Creative)
**Plugin:** Waves SSL G-Master Buss Compressor / FabFilter Pro-Q3 (Natural Phase)

```
1. Sub-Bass Shelf (DRAMA)
   Frequency: 40 Hz
   Type: Low Shelf
   Gain: +1.2 dB
   Q: 0.7 (gentle slope)
   Purpose: Add weight and power for DROP

2. Warmth/Body
   Frequency: 120 Hz
   Type: Bell
   Gain: +0.5 dB
   Q: 1.0 (wide)
   Purpose: Add warmth to bass elements

3. Clarity/Presence
   Frequency: 2.5 kHz
   Type: Bell
   Gain: +1.0 dB
   Q: 2.0 (moderate)
   Purpose: Bring forward vocals/leads, add clarity

4. Sizzle/Definition
   Frequency: 6.5 kHz
   Type: Bell
   Gain: +0.7 dB
   Q: 1.5
   Purpose: Add shimmer and edge to synths

5. Air/Brilliance Shelf
   Frequency: 10 kHz
   Type: High Shelf
   Gain: +1.5 dB
   Q: 0.7 (gentle slope)
   Purpose: Add air, openness, professional sheen

6. Ultra-High Cleanup (Optional)
   Frequency: 18 kHz
   Type: Low-Pass
   Slope: 6 dB/oct (very gentle)
   Purpose: Remove harsh digital artifacts
```

#### STAGE 3: Dynamic EQ (Optional - Advanced)
**Plugin:** FabFilter Pro-Q3 (Dynamic Mode) / Waves F6

```
1. De-Essing (if needed)
   Frequency: 6-8 kHz
   Type: Dynamic Bell (compress)
   Threshold: -20 dB
   Range: -3 dB max
   Attack: 5 ms / Release: 50 ms
   Purpose: Tame harsh sibilance or hi-hat peaks

2. Bass Control
   Frequency: 80-100 Hz
   Type: Dynamic Bell (compress)
   Threshold: -15 dB
   Range: -2 dB max
   Attack: 30 ms / Release: 100 ms
   Purpose: Control boomy bass transients
```

### Total EQ Gain Budget
- Maximum boost: +1.5 dB (air shelf)
- Maximum cut: -1.0 dB (mud reduction)
- **Net result:** Transparent enhancement, not obvious EQ

---

## 5. COMPRESSION/LIMITING STRATEGY ⚡

### Current Dynamic Profile
- **Crest Factor:** 14.5 dB (very dynamic)
- **Dynamic Range:** 16.0 dB (DR14 equivalent)
- **Peak-to-Average:** High variation

This is a DYNAMIC mix. We need to preserve transients while achieving loudness.

### 3-Stage Compression Chain

#### STAGE 1: Multiband Compression (Subtle Control)
**Plugin:** FabFilter Pro-MB / Waves C6 / iZotope Ozone 11 Dynamics

**Purpose:** Control frequency-specific dynamics without squashing overall mix

```
BAND 1: SUB-BASS (20-120 Hz)
├─ Threshold: -18 dBFS
├─ Ratio: 2.0:1
├─ Attack: 30 ms (preserve kick punch)
├─ Release: 100 ms (auto-release ON)
├─ Knee: 3 dB (soft)
├─ Gain Reduction: 1-2 dB max
└─ Purpose: Tighten low end, prevent woofer damage

BAND 2: BASS/LOW-MIDS (120-500 Hz)
├─ Threshold: -16 dBFS
├─ Ratio: 2.0:1
├─ Attack: 20 ms
├─ Release: 80 ms (auto-release ON)
├─ Knee: 3 dB (soft)
├─ Gain Reduction: 1-3 dB max
└─ Purpose: Control muddy buildup

BAND 3: MIDRANGE (500-5000 Hz)
├─ Threshold: -14 dBFS
├─ Ratio: 1.5:1 (gentle!)
├─ Attack: 10 ms
├─ Release: 50 ms (auto-release ON)
├─ Knee: 5 dB (very soft)
├─ Gain Reduction: 0.5-2 dB max
└─ Purpose: Glue midrange, add cohesion

BAND 4: HIGH-END (5000-20000 Hz)
├─ Threshold: -12 dBFS
├─ Ratio: 2.0:1
├─ Attack: 5 ms (fast transient control)
├─ Release: 40 ms (auto-release ON)
├─ Knee: 3 dB (soft)
├─ Gain Reduction: 1-2 dB max
└─ Purpose: Tame harsh transients, add polish
```

**Important Settings:**
- **Lookahead:** 5 ms (all bands)
- **Output Gain:** 0 dB (transparent, no makeup)
- **Solo Bands:** Check for artifacts
- **A/B Compare:** Should be subtle, not obvious

**Expected Result:**
- Total GR: 2-4 dB across all bands
- More controlled, tighter sound
- Preserved transients and punch

---

#### STAGE 2: Glue Compressor (Optional - Character)
**Plugin:** Waves SSL G-Master / Cytomic The Glue / Slate VBC

**Purpose:** Add analog character, gentle glue

```
Settings:
├─ Threshold: -10 dBFS (gentle)
├─ Ratio: 2:1
├─ Attack: 30 ms (slow, preserve transients)
├─ Release: Auto (or 300 ms)
├─ Makeup Gain: +1 to +2 dB
├─ Mix (Parallel): 50% (blend)
└─ Gain Reduction: 1-2 dB max

Character Settings (SSL G-Master):
├─ 4K Button: ON (adds high-end sparkle)
└─ Analog: ON (subtle saturation)
```

**When to Use:**
- If mix feels "loose" or disconnected
- For analog warmth/glue
- EDM/electronic can benefit from SSL character

**When to SKIP:**
- If multiband compression already provides cohesion
- If mix already feels "glued"

---

#### STAGE 3: Final Limiter (Maximum Loudness)
**Plugin:** FabFilter Pro-L2 / Waves L2 / iZotope Ozone Maximizer

**Purpose:** Achieve target loudness without distortion

### TWO CONFIGURATIONS:

#### CONFIG A: Streaming Master (-14 LUFS)
```
FabFilter Pro-L2 Settings:
├─ Ceiling: -1.0 dBTP (true peak)
├─ Gain: +1.5 to +2.0 dB (target -14 LUFS)
├─ Attack: 1.0 ms
├─ Release: 100 ms (auto-release ON)
├─ Lookahead: 10 ms
├─ Style: Transparent / Modern
├─ Oversampling: 4x
├─ True Peak Limiting: ON
├─ Channel Linking: Stereo (linked)
└─ Expected GR: 2-3 dB on peaks

Result:
- Natural, dynamic master
- Preserves punch and transients
- Streaming-friendly
```

#### CONFIG B: Aggressive Master (-8 LUFS EDM)
```
FabFilter Pro-L2 Settings:
├─ Ceiling: -0.5 dBTP (true peak)
├─ Gain: +7.5 to +8.0 dB (target -8 LUFS)
├─ Attack: 0.5 ms (FAST for EDM punch)
├─ Release: 50 ms (auto-release ON, fast recovery)
├─ Lookahead: 5 ms (shorter for more aggression)
├─ Style: Modern / Aggressive
├─ Oversampling: 4x
├─ True Peak Limiting: ON
├─ Channel Linking: Stereo (linked)
└─ Expected GR: 5-8 dB on peaks

Result:
- Loud, competitive loudness
- Some dynamic sacrifice (acceptable for genre)
- Maximum impact on club systems
```

### Critical Limiter Parameters Explained

**Attack Time:**
- Fast (0.5-1 ms): Catches transients, more "crushed" sound (EDM)
- Slow (5-10 ms): Preserves transients, more natural (acoustic)

**Release Time:**
- Fast (10-50 ms): Quick recovery, more pumping (EDM energy)
- Slow (100-500 ms): Smooth, transparent, less pumping (natural)

**Lookahead:**
- More (10-15 ms): Cleaner limiting, less distortion
- Less (2-5 ms): More aggressive, can add "punch"

**Style/Algorithm:**
- Transparent: Cleanest, least coloration
- Modern: Balanced, popular choice
- Aggressive: Maximum loudness, some saturation

### Limiter Monitoring

**Watch These Meters:**
1. **Gain Reduction:** Should not exceed 8 dB sustained
2. **True Peak:** MUST stay below ceiling (-1.0 or -0.5 dBTP)
3. **LUFS:** Check integrated loudness matches target
4. **Correlation:** Should stay >0.5 (good stereo)

**Listen For:**
- Pumping (too fast release)
- Distortion (too much gain reduction)
- Loss of transients (too fast attack)
- Stereo collapse (too much limiting)

---

## 6. DROP ENHANCEMENT (17.163s) 🎯

### Special Techniques for Maximum Impact

The DROP at 17.163 seconds is the **key moment** - this must hit HARD.

### Pre-DROP Build (15.0s - 17.16s)

#### Technique 1: Volume Automation (Subtle Energy Pull)
```
Timeline:
15.0s - 16.5s: 0 dB (normal level)
16.5s - 17.1s: -1.5 dB (gradual reduction, builds tension)
17.163s: SNAP back to 0 dB (instant release)

Plugin: DAW automation (pre-mastering chain)
Purpose: Creates contrast, makes drop feel LOUDER
```

#### Technique 2: High-Pass Filter Sweep (Dramatic Build)
```
Timeline:
15.0s - 16.0s: No filter (full frequency)
16.0s - 17.0s: Sweep high-pass from 100 Hz → 800 Hz
17.163s: INSTANT removal (full bass return)

Plugin: FabFilter Pro-Q3 (automate HP frequency)
Purpose: Removes bass during build, explosive return at drop
Critical: Use ZERO-LATENCY mode for precise timing!
```

#### Technique 3: Reverb Build (Cinematic Rise)
```
Plugin: Valhalla VintageVerb / Soundtoys Little Plate

Settings:
├─ Pre-Delay: 0 ms
├─ Decay: 2.5-4.0 seconds (long tail)
├─ Size: Large Hall
├─ Mix: Start 0% → End 30% (automated rise)
├─ High Cut: 8 kHz (keep reverb warm)
└─ Timeline: Increase mix from 0% to 30% over 15-17s

Purpose: Creates sense of space expanding, then collapsing at drop
```

---

### AT DROP (17.163s) - Make It HIT

#### Technique 4: Transient Enhancement
```
Plugin: Waves Trans-X / SPL Transient Designer / Schaack Transient Shaper

Settings:
├─ Attack: +2 to +4 dB (boost initial hit)
├─ Sustain: +1 dB (maintain energy)
├─ Release: 0 dB (natural decay)
├─ Frequency Focus: 60-100 Hz + 2-6 kHz
└─ Apply: Only to DROP section (17.163s onward)

Purpose: Makes kick/bass hit harder, instant impact
```

#### Technique 5: Stereo Width Enhancement (Highs Only!)
```
Plugin: iZotope Ozone Imager / Waves S1 Stereo Imager

Settings:
├─ Low Frequency (<150 Hz): 0% width (MONO - critical!)
├─ Mid Frequency (150-2000 Hz): 100% width (no change)
├─ High Frequency (>2000 Hz): 120-140% width (widen)
├─ Stereoize Amount: 10-15%
└─ Apply: DROP section only

Purpose: Widens stereo field, creates "explosion" effect
Warning: NEVER widen bass - causes phase issues, weak mono
```

#### Technique 6: Sub-Bass Emphasis (Check & Boost)
```
Plugin: Waves Renaissance Bass / MaxxBass / RBass

Settings:
├─ Frequency: 40-50 Hz (fundamental)
├─ Intensity: 20-40% (subtle)
├─ Type: Generate harmonics (2nd order)
└─ Apply: DROP bass elements only

Purpose: Ensures powerful sub-bass presence
Why: Adds perceived low-end on smaller speakers
```

#### Technique 7: Sidechain Compression (Clarity)
```
Plugin: FabFilter Pro-MB (sidechain mode) / Waves C6

Setup:
├─ Key Input: Kick drum (trigger)
├─ Target: Bass/Sub-bass (ducked)
├─ Threshold: -20 dB
├─ Ratio: 4:1
├─ Attack: 10 ms (fast duck)
├─ Release: 100 ms (quick recovery)
└─ Gain Reduction: 3-6 dB on kick hits

Purpose: Creates "pumping" rhythm, keeps kick clear
Result: Kick punches through bass, adds energy
```

---

### Post-DROP (17.163s - 37.0s)

#### Technique 8: Sustain Energy
```
Strategy:
1. NO additional volume automation drops
2. Maintain limiting settings from DROP
3. Ensure consistent loudness throughout
4. Check for any dips in energy - compensate with automation

Purpose: Keep listener engaged after the impact
```

#### Technique 9: Final Moments (35s-37s)
```
Fade-out (if applicable):
├─ Start: 35.0s
├─ End: 37.0s
├─ Curve: Linear or S-curve
└─ Target: -inf dB or natural musical end

OR Natural End:
├─ Reverb Tail: Allow 1-2 seconds
├─ No abrupt cuts
└─ Let final chord/note breathe
```

---

### DROP Enhancement: Complete Signal Chain
```
PRE-MASTERING (in DAW, before bounce):
1. Volume Automation (-1.5 dB dip before drop)
2. High-Pass Filter Sweep (100 → 800 Hz)
3. Reverb Build Automation (0% → 30% mix)

MASTERING CHAIN (at 17.163s):
1. Transient Shaper (+3 dB attack boost) → ON for drop section
2. Stereo Imager (120% width >2kHz) → ON for drop section
3. Sub-Bass Enhancer (40 Hz, 30% intensity) → ON for drop section
4. [Continue with normal mastering chain: EQ, Multiband, Limiter]

Result: DROP will feel like it EXPLODES out of the speakers
```

---

## 7. COMPLETE MASTERING SIGNAL FLOW 🔧

### CHAIN ORDER (Critical - Do Not Reorder!)

```
INPUT: СМОТРЕЛА_teaser.wav (48kHz/float32, -15.6 LUFS)
  │
  ↓
┌─────────────────────────────────────────────────────────────┐
│ 1. SPECTRAL REPAIR (if needed)                              │
│    Plugin: iZotope RX 11 / Accusonus ERA Bundle             │
│    Purpose: Remove clicks, pops, noise                      │
│    Settings: Visual inspection mode, surgical removal       │
└─────────────────────────────────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. STEREO BALANCE CORRECTION ⚠️ CRITICAL                     │
│    Plugin: iZotope Ozone Imager / Waves S1                  │
│    Action: Boost RIGHT channel +0.42 dB                     │
│            (Fix 0.83 dB L/R imbalance)                      │
│    Verify: Check correlation meter (target 0.55-0.65)       │
└─────────────────────────────────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. LINEAR PHASE EQ (Surgical/Corrective)                    │
│    Plugin: FabFilter Pro-Q3 (Linear Phase Zero-Latency)     │
│    Purpose: Remove problem frequencies, clean up mix        │
│                                                              │
│    Band 1: HP Filter @ 25 Hz, 24 dB/oct                     │
│    Band 2: Bell -1.0 dB @ 40 Hz, Q=3.0 (sub cleanup)        │
│    Band 3: Bell -0.8 dB @ 180 Hz, Q=1.2 (mud reduction)     │
│    Band 4: Bell -0.5 dB @ 350 Hz, Q=1.5 (boxiness)          │
│    Band 5: Dynamic -2 dB @ 800-1200 Hz (sweep/find nasal)   │
└─────────────────────────────────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. MULTIBAND COMPRESSION (Dynamics Control)                 │
│    Plugin: FabFilter Pro-MB / Waves C6                       │
│    Purpose: Control frequency-specific dynamics              │
│                                                              │
│    Band 1 (20-120 Hz): 2:1, -18dB, Atk 30ms, Rel 100ms      │
│    Band 2 (120-500 Hz): 2:1, -16dB, Atk 20ms, Rel 80ms      │
│    Band 3 (500-5k Hz): 1.5:1, -14dB, Atk 10ms, Rel 50ms     │
│    Band 4 (5k-20k Hz): 2:1, -12dB, Atk 5ms, Rel 40ms        │
│                                                              │
│    Lookahead: 5ms | Auto-Release: ON | GR: 2-4dB total      │
└─────────────────────────────────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. MASTERING EQ (Enhancement/Color)                          │
│    Plugin: Waves SSL G-Master / FabFilter Pro-Q3 (Natural)  │
│    Purpose: Add character, enhance tone                     │
│                                                              │
│    Band 1: Low Shelf +1.2 dB @ 40 Hz, Q=0.7 (power)         │
│    Band 2: Bell +0.5 dB @ 120 Hz, Q=1.0 (warmth)            │
│    Band 3: Bell +1.0 dB @ 2.5 kHz, Q=2.0 (presence)         │
│    Band 4: Bell +0.7 dB @ 6.5 kHz, Q=1.5 (sizzle)           │
│    Band 5: High Shelf +1.5 dB @ 10 kHz, Q=0.7 (air)         │
│    Band 6: LP Filter @ 18 kHz, 6 dB/oct (optional cleanup)  │
└─────────────────────────────────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. STEREO ENHANCEMENT (Width for Drop Impact)               │
│    Plugin: iZotope Ozone Imager / Waves S1                  │
│    Purpose: Widen highs for spacious feel                   │
│                                                              │
│    Low (<150 Hz): 0% width → MONO (critical!)               │
│    Mid (150-2k Hz): 100% width → NO CHANGE                  │
│    High (>2k Hz): 120-130% width → WIDEN                    │
│    Stereoize: 10-15% (subtle)                               │
│                                                              │
│    ⚠️ Automation: Increase to 140% width at DROP (17.163s)   │
│    ⚠️ Check: Mono compatibility - no phase cancellation      │
└─────────────────────────────────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. HARMONIC EXCITER (optional - subtle saturation)          │
│    Plugin: Waves Aphex Aural Exciter / Ozone Exciter        │
│    Purpose: Add warmth, harmonics, analog feel              │
│                                                              │
│    Type: Tape or Tube (warm character)                      │
│    Amount: 5-15% mix (very subtle!)                         │
│    Frequency: Multiband (separate low/high)                 │
│    - Low (50-500 Hz): 2nd harmonic, 10% mix                 │
│    - High (2k-20k Hz): 3rd harmonic, 5% mix                 │
│                                                              │
│    Skip if: Mix already sounds "warm" or you want clean     │
└─────────────────────────────────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. GLUE COMPRESSOR (optional - analog character)            │
│    Plugin: Waves SSL G-Master / Cytomic The Glue            │
│    Purpose: Final glue, analog warmth                       │
│                                                              │
│    Threshold: -10 dBFS                                       │
│    Ratio: 2:1                                                │
│    Attack: 30 ms (slow, preserve transients)                │
│    Release: Auto (or 300 ms)                                │
│    Makeup: +1 to +2 dB                                       │
│    Mix: 50% (parallel blend)                                │
│    GR: 1-2 dB max                                            │
│                                                              │
│    SSL Settings: 4K Button ON, Analog ON                    │
│    Skip if: Already feels cohesive                          │
└─────────────────────────────────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────────────────────────────────┐
│ 9A. FINAL LIMITER - STREAMING VERSION (-14 LUFS) ✅          │
│     Plugin: FabFilter Pro-L2 / Waves L2                     │
│                                                              │
│     Ceiling: -1.0 dBTP (true peak)                          │
│     Gain: +1.5 to +2.0 dB                                    │
│     Attack: 1.0 ms                                           │
│     Release: 100 ms (auto ON)                               │
│     Lookahead: 10 ms                                         │
│     Style: Transparent / Modern                             │
│     Oversampling: 4x                                         │
│     True Peak Limiting: ON                                   │
│     Channel Linking: Stereo                                  │
│     Expected GR: 2-3 dB                                      │
│                                                              │
│     Result: -14 LUFS, dynamic, streaming-optimized          │
└─────────────────────────────────────────────────────────────┘
  │
  ↓ (OR - choose one limiter config)
  │
┌─────────────────────────────────────────────────────────────┐
│ 9B. FINAL LIMITER - AGGRESSIVE VERSION (-8 LUFS) 🔥          │
│     Plugin: FabFilter Pro-L2 / Waves L2                     │
│                                                              │
│     Ceiling: -0.5 dBTP (true peak)                          │
│     Gain: +7.5 to +8.0 dB                                    │
│     Attack: 0.5 ms (FAST)                                    │
│     Release: 50 ms (auto ON, fast recovery)                 │
│     Lookahead: 5 ms                                          │
│     Style: Modern / Aggressive                              │
│     Oversampling: 4x                                         │
│     True Peak Limiting: ON                                   │
│     Channel Linking: Stereo                                  │
│     Expected GR: 5-8 dB                                      │
│                                                              │
│     Result: -8 LUFS, loud, EDM-competitive                  │
└─────────────────────────────────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────────────────────────────────┐
│ 10. METERING / VERIFICATION                                 │
│     Plugin: iZotope Insight 2 / Waves WLM Plus              │
│                                                              │
│     Check:                                                   │
│     ✓ Integrated LUFS: -14 or -8 (±0.5 tolerance)           │
│     ✓ True Peak: Below ceiling (-1.0 or -0.5 dBTP)          │
│     ✓ Stereo Correlation: >0.5 (good stereo)                │
│     ✓ Dynamic Range: >8 dB (streaming) / >6 dB (aggressive) │
│     ✓ Spectral Balance: Visual check for frequency holes    │
│     ✓ Phase: No major phase issues visible                  │
└─────────────────────────────────────────────────────────────┘
  │
  ↓
OUTPUT: СМОТРЕЛА_MASTERED.wav
```

---

### Critical Chain Notes

**DO NOT REORDER** - This sequence is optimized:
1. **Fix first** (stereo balance, problems)
2. **Control dynamics** (multiband, glue)
3. **Enhance tone** (EQ, saturation, width)
4. **Maximize loudness** (limiter)
5. **Verify** (metering)

**Bypass Test:** A/B compare with each plugin bypassed to ensure it's helping, not hurting.

**Gain Staging:** Watch meters between each plugin - avoid internal clipping.

**Processing Budget:**
- Total latency: <50 ms (acceptable for mastering)
- CPU usage: Monitor for real-time processing
- If system struggles: Render/bounce in stages

---

## 8. A/B REFERENCE COMPARISON 📊

### Reference Track Selection

For "СМОТРЕЛА" (dramatic electronic/cinematic), reference against:

**Genre-Matched Tracks (Electronic/Dramatic):**
1. **ODESZA** - "A Moment Apart" (similar emotional electronic)
2. **deadmau5** - "Strobe" (progressive build/drop structure)
3. **Porter Robinson** - "Shelter" (dramatic, emotional)
4. **REZZ** - Any track (dark, heavy electronic)
5. **Flume** - "Never Be Like You" (modern electronic production)

**Mastering Quality References:**
- Any track mastered by Sterling Sound
- Spotify/Tidal "Master Quality" releases
- Beatport #1 tracks in similar genre

### A/B Comparison Method

#### Plugin: ADPTR Audio Metric AB / Magic AB / REFERENCE
```
Setup:
1. Load reference track at same loudness (-14 or -8 LUFS)
2. Level-match with gain offset (critical!)
3. Compare sections: intro, build, drop, outro

What to Listen For:
├─ Overall Tonal Balance (too bright? too dark?)
├─ Bass Weight (is yours too light/heavy?)
├─ Stereo Width (is yours too narrow/wide?)
├─ Loudness (does yours feel competitive?)
├─ Clarity (can you hear all elements clearly?)
└─ Punch (do transients hit as hard?)

Visual Comparison (Spectrum Analyzer):
├─ Low-end rolloff point (should match)
├─ Midrange presence (2-5 kHz critical)
├─ High-end extension (air frequencies)
└─ Overall spectral curve shape
```

### Specific Checks

**Bass Balance:**
- Play reference track - note sub-bass level
- Play your master - should feel similar weight
- If yours is lighter: boost 40 Hz shelf by +0.5-1 dB
- If yours is heavier: reduce 40 Hz or add high-pass

**High-End Balance:**
- Reference track high-end should sound similar
- Too bright: reduce 10 kHz shelf by -0.5 dB
- Too dull: boost 10 kHz shelf by +0.5 dB

**Stereo Width:**
- Reference should have similar spaciousness
- Too narrow: increase stereo enhancement
- Too wide: reduce or check mono compatibility

**Loudness:**
- Should feel equally "loud" when level-matched
- If yours feels quieter: increase limiter gain
- If yours feels louder but worse: reduce limiting

---

## 9. FINAL DELIVERABLES & EXPORT ✅

### Export Settings

#### MASTER 1: Streaming Master (Conservative)
```
Format: WAV
Sample Rate: 44.1 kHz (standard for streaming)
Bit Depth: 16-bit (streaming platforms use this)
Dither: TPDF or POW-r 1 (noise-shaped)
Target LUFS: -14 LUFS integrated
True Peak: -1.0 dBTP

File Naming:
СМОТРЕЛА_MASTER_STREAMING_44k16bit.wav

Destinations:
- Spotify
- YouTube
- Apple Music
- Amazon Music
- Deezer
```

#### MASTER 2: High-Resolution Master (Archival/Promo)
```
Format: WAV or FLAC (lossless)
Sample Rate: 48 kHz (keep original)
Bit Depth: 24-bit (maximum quality)
Dither: NONE (stay in 24-bit domain)
Target LUFS: -8 LUFS integrated (aggressive)
True Peak: -0.5 dBTP

File Naming:
СМОТРЕЛА_MASTER_HD_48k24bit.wav

Destinations:
- Tidal (Master Quality)
- Qobuz (Hi-Res)
- Bandcamp (lossless download)
- Beatport (DJ/club play)
- Personal archive
```

#### MASTER 3: MP3 (Lossy Distribution)
```
Format: MP3
Encoder: LAME 3.100 (best quality)
Bitrate: 320 kbps CBR (constant bitrate)
Sample Rate: 44.1 kHz
Source: From STREAMING master (44.1k/16bit)

File Naming:
СМОТРЕЛА_MASTER_320kbps.mp3

Destinations:
- SoundCloud
- DJ promo pools
- Email/social media sharing
```

---

### Pre-Export Checklist

**Before rendering final master:**

☑️ **1. Loudness Verification**
- [ ] Integrated LUFS matches target (±0.3 LU)
- [ ] True peak stays below ceiling throughout
- [ ] No limiter over-compression (GR <10 dB)

☑️ **2. Sonic Quality**
- [ ] No distortion audible (listen on monitors + headphones)
- [ ] Transients preserved (kick/snare have punch)
- [ ] Bass translates on small speakers (laptop test)
- [ ] High-end not harsh or fatiguing
- [ ] Stereo field sounds natural

☑️ **3. Technical Verification**
- [ ] No DC offset (should be 0.00)
- [ ] No clipping (peak <0 dBFS)
- [ ] Fade-in/out smooth (if applicable)
- [ ] No clicks at start/end of file
- [ ] Metadata embedded (artist, title, ISRC if available)

☑️ **4. Mono Compatibility**
- [ ] Check in mono (phone speaker simulation)
- [ ] No major phase cancellation
- [ ] Bass still present in mono
- [ ] Overall balance sounds good

☑️ **5. Reference Comparison**
- [ ] Level-matched A/B with reference track
- [ ] Competitive loudness
- [ ] Similar tonal balance
- [ ] Matches genre standards

☑️ **6. Client Approval (if applicable)**
- [ ] Send pre-master for feedback
- [ ] Address any revision requests
- [ ] Get final sign-off

---

### Sample Rate Conversion (44.1k for Streaming)

**Best Practice: SRC (Sample Rate Conversion)**

```
Plugin: iZotope RX / SoX / Saracon / r8brain

Settings for 48k → 44.1k:
├─ Algorithm: Linear phase, high quality
├─ Anti-Alias Filter: Sharp (brick-wall)
├─ Dither: TPDF with noise shaping
├─ Bit Depth: 48k/24bit → 44.1k/16bit
└─ Quality: Maximum (slowest, best)

Why this matters:
- Streaming platforms want 44.1 kHz
- Poor SRC can cause aliasing, artifacts
- Professional SRC preserves quality
```

**Alternative:** Export at 48 kHz and let platform convert
- Spotify accepts 48 kHz (they convert internally)
- Quality: Slightly worse than manual SRC
- Convenience: Easier workflow

**Recommendation for this track:**
Export both versions:
1. 48 kHz/24-bit (HD master, archival)
2. 44.1 kHz/16-bit (streaming, converted with iZotope RX)

---

## 10. PLATFORM-SPECIFIC CONSIDERATIONS 🌐

### Spotify
```
Recommended Delivery:
- Format: 44.1 kHz / 16-bit WAV or OGG
- Loudness: -14 LUFS integrated (they normalize to this)
- True Peak: -1.0 dBTP
- If louder: They turn down (lose dynamic range benefit)
- If quieter: They turn up (can introduce noise/artifacts)

Spotify Normalization:
- Standard: -14 LUFS (default)
- Loud: -11 LUFS (user setting, less common)

Strategy:
✅ Master to -14 LUFS exactly
✅ Preserves dynamics
✅ Sounds best on "Normalize Audio" ON setting
```

### YouTube
```
Recommended Delivery:
- Format: 44.1 kHz / 16-bit WAV
- Loudness: -13 to -15 LUFS integrated (they normalize to -14)
- True Peak: -1.0 dBTP
- Video Encoding: H.264, AAC 320 kbps

YouTube Normalization:
- Target: -14 LUFS (similar to Spotify)
- Less consistent (varies by content type)

Strategy:
✅ Master to -14 LUFS
✅ Leave headroom for video compression artifacts
```

### Apple Music
```
Recommended Delivery:
- Format: 44.1 kHz / 16-bit WAV (they transcode to ALAC)
- Loudness: -16 LUFS integrated (their target)
- True Peak: -1.0 dBTP
- Sound Check: ON (normalization)

Apple Music Normalization:
- Target: -16 LUFS (more conservative)
- Sound Check reduces louder tracks

Strategy:
⚠️ Dilemma: Master to -14 LUFS (Spotify) or -16 (Apple)?
✅ Solution: Master to -14 LUFS
   - Apple will play it slightly louder than target (acceptable)
   - OR create separate Apple-optimized master at -16 LUFS
```

### Tidal / Qobuz (Hi-Res)
```
Recommended Delivery:
- Format: 48 kHz / 24-bit FLAC or WAV
- Loudness: -14 LUFS OR -8 LUFS (aggressive, no normalization)
- True Peak: -1.0 dBTP (conservative) or -0.5 dBTP (aggressive)

Tidal/Qobuz Behavior:
- Master Quality (MQA on Tidal, Hi-Res on Qobuz)
- NO normalization (they respect your loudness)
- Audiophile listeners (expect quality over loudness)

Strategy:
🎯 TWO OPTIONS:
1. Conservative: -14 LUFS, preserve dynamics for critical listeners
2. Competitive: -8 LUFS, match other EDM tracks on platform

Recommendation: -14 LUFS for Hi-Res platforms (dynamics valued)
```

### Beatport (DJ/Club)
```
Recommended Delivery:
- Format: 44.1 kHz / 16-bit WAV (some accept 24-bit)
- Loudness: -8 to -9 LUFS integrated (LOUD, competitive)
- True Peak: -0.3 to -0.5 dBTP (aggressive)

Beatport/DJ Culture:
- Loudness war ACTIVE (DJs want loud tracks)
- Compete with other EDM tracks
- Club systems (expect aggressive limiting)

Strategy:
🔥 Master AGGRESSIVELY:
   - Target: -8 LUFS
   - Ceiling: -0.5 dBTP
   - Maximize impact for DJ mixing
```

### SoundCloud
```
Recommended Delivery:
- Format: 320 kbps MP3 or WAV
- Loudness: -14 LUFS (they normalize)
- True Peak: -1.0 dBTP
- Lossy Compression: Assume heavy compression

SoundCloud Normalization:
- Target: -14 LUFS (Spotify-like)
- Transcodes to 128 kbps Opus (lossy!)

Strategy:
✅ Master to -14 LUFS
⚠️ Upload WAV (not MP3) - let SoundCloud encode
⚠️ Expect quality loss from lossy encoding
```

---

### Platform Decision Matrix

| Platform | Target LUFS | True Peak | Sample Rate | Strategy |
|----------|-------------|-----------|-------------|----------|
| **Spotify** | -14 | -1.0 dBTP | 44.1k/16bit | Conservative, dynamic |
| **YouTube** | -14 | -1.0 dBTP | 44.1k/16bit | Conservative, dynamic |
| **Apple Music** | -16 | -1.0 dBTP | 44.1k/16bit | Most conservative |
| **Tidal/Qobuz** | -14 or -8 | -1.0 dBTP | 48k/24bit | Hi-res, quality focus |
| **Beatport** | -8 | -0.5 dBTP | 44.1k/16bit | Aggressive, loud |
| **SoundCloud** | -14 | -1.0 dBTP | WAV/MP3 | Conservative, lossy-aware |

### Recommendation for "СМОТРЕЛА"
```
Create TWO masters:

MASTER A: Streaming (Spotify/YouTube/Apple)
- 44.1 kHz / 16-bit WAV
- -14 LUFS integrated
- -1.0 dBTP true peak
- Conservative limiting
- File: СМОТРЕЛА_MASTER_STREAMING.wav

MASTER B: Promo/DJ (Beatport/Downloads)
- 48 kHz / 24-bit WAV
- -8 LUFS integrated
- -0.5 dBTP true peak
- Aggressive limiting
- File: СМОТРЕЛА_MASTER_PROMO.wav

This covers all platforms optimally!
```

---

## 11. QUALITY CONTROL CHECKLIST ✓

### Final QC Before Delivery

#### LISTEN on Multiple Systems:
- [ ] **Studio Monitors** (Yamaha HS, KRK, etc.) - critical listening
- [ ] **Headphones** (open-back: Sennheiser HD, closed: Sony MDR) - detail check
- [ ] **Earbuds** (Apple AirPods, cheap earbuds) - consumer experience
- [ ] **Phone Speaker** (mono, worst-case scenario)
- [ ] **Car Stereo** (bass-heavy, consumer environment)
- [ ] **Laptop Speakers** (weak bass, midrange-focused)

#### What to Check on Each System:
- **Bass**: Present but not boomy? Translates on small speakers?
- **Clarity**: Can you hear all instruments clearly?
- **Harshness**: Any fatiguing high frequencies?
- **Balance**: Left/right image centered?
- **Loudness**: Feels competitive with commercial tracks?

---

#### TECHNICAL CHECKS (Metering):
- [ ] **Integrated LUFS:** Matches target (±0.3 LU)
- [ ] **True Peak:** Never exceeds ceiling
- [ ] **Stereo Correlation:** >0.5 (good stereo)
- [ ] **Dynamic Range:** >8 dB (streaming) / >6 dB (aggressive)
- [ ] **DC Offset:** 0.00 (no offset)
- [ ] **Clipping:** None visible on waveform
- [ ] **Spectral Balance:** No major holes/peaks in spectrum

---

#### FILE CHECKS:
- [ ] **File Format:** WAV (not MP3 for master source)
- [ ] **Sample Rate:** Correct (44.1k or 48k)
- [ ] **Bit Depth:** Correct (16-bit or 24-bit)
- [ ] **File Size:** Reasonable (37s × 48k × 24bit × 2ch ≈ 17 MB)
- [ ] **Metadata:** Artist, title, album, ISRC embedded
- [ ] **File Name:** Clear, descriptive, version labeled

---

#### SONIC QUALITY (Critical Listening):
- [ ] **Intro (0-5s):** Clean start, no clicks, proper fade-in?
- [ ] **Build (5-17s):** Energy increases, automation smooth?
- [ ] **DROP (17.163s):** Maximum impact, hits hard?
- [ ] **Body (17-35s):** Sustained energy, no dips?
- [ ] **Outro (35-37s):** Clean end, proper fade-out?
- [ ] **Overall:** No distortion, pumping, or artifacts?

---

#### MONO COMPATIBILITY:
- [ ] **Mono Sum:** Check on phone speaker, mono button
- [ ] **Bass Present:** Low-end still audible in mono?
- [ ] **Phase Issues:** No major cancellation?
- [ ] **Overall Balance:** Sounds good in mono?

---

#### A/B COMPARISON:
- [ ] **Reference Track:** Level-matched, compared
- [ ] **Tonal Balance:** Matches reference's frequency balance?
- [ ] **Loudness:** Competitive with reference?
- [ ] **Stereo Width:** Similar spaciousness?
- [ ] **Quality:** Feels "finished" and professional?

---

#### MASTERING ENGINEER SIGN-OFF:
- [ ] **Personal Approval:** I would put my name on this
- [ ] **Commercial Ready:** Ready for public release
- [ ] **Technical Standards:** Meets all specs
- [ ] **Client Approval:** Client/artist satisfied (if applicable)

**IF ANY ITEM FAILS:** Go back and address the issue. Do not compromise on quality.

---

## 12. ADDITIONAL RESOURCES & TOOLS 🛠️

### Recommended Plugins (Professional Standard)

#### EQ:
- **FabFilter Pro-Q3** - Industry standard, best transparency
- **Waves SSL G-EQ** - Analog color, musical
- **iZotope Ozone EQ** - All-in-one mastering
- **DMG Audio Equilibrium** - Surgical precision

#### Compression:
- **FabFilter Pro-MB** - Best multiband, flexibility
- **Waves C6** - Classic multiband workhorse
- **Cytomic The Glue** - SSL bus comp emulation
- **Slate Digital VBC** - Multiple analog comp models

#### Limiting:
- **FabFilter Pro-L2** - Best modern limiter, transparent
- **Waves L2/L3** - Classic, aggressive when needed
- **iZotope Ozone Maximizer** - Intelligent, AI-assisted
- **Sonnox Oxford Limiter** - Clean, transparent

#### Stereo Imaging:
- **iZotope Ozone Imager** - Free, effective
- **Waves S1** - Professional standard
- **Goodhertz Midside Matrix** - Advanced M/S control

#### Metering:
- **iZotope Insight 2** - Complete metering suite
- **Waves WLM Plus** - LUFS, true peak, compliance
- **Plugin Alliance ADPTR Metric AB** - A/B comparison
- **Youlean Loudness Meter** - Free, excellent LUFS meter

#### Restoration/Repair:
- **iZotope RX 11** - Industry standard, best spectral repair
- **Accusonus ERA Bundle** - Fast, AI-based cleanup

---

### Learning Resources

#### Books:
- **"Mastering Audio" by Bob Katz** - Bible of mastering
- **"The Loudness War" by Earl Vickers** - Understanding loudness
- **"Mixing Secrets" by Mike Senior** - Practical techniques

#### Websites:
- **iZotope Learning Hub** - Free mastering education
- **Sound on Sound** - Technical articles, reviews
- **Gearspace** - Community, discussions, advice

#### YouTube Channels:
- **MixBusTV** - Professional mastering workflows
- **iZotope** - Plugin tutorials, tips
- **FabFilter** - Expert techniques

---

## 13. FINAL RECOMMENDATIONS SUMMARY 📝

### Critical Actions (MUST DO):

1. **Fix Stereo Imbalance**
   - Boost RIGHT channel by +0.42 dB
   - Current 0.83 dB difference is audible
   - Use iZotope Ozone Imager or balance plugin

2. **Achieve Target Loudness**
   - Streaming: -14 LUFS (add +1.6 dB)
   - Promo/DJ: -8 LUFS (add +7.6 dB)
   - Use FabFilter Pro-L2 or similar limiter

3. **Enhance DROP Impact (17.163s)**
   - Pre-drop: Volume automation dip (-1.5 dB)
   - Pre-drop: High-pass filter sweep (100→800 Hz)
   - At drop: Transient enhancement (+3 dB attack)
   - At drop: Stereo width increase (140% highs)

4. **Apply Mastering EQ**
   - Sub-bass boost: +1.2 dB @ 40 Hz
   - Presence boost: +1.0 dB @ 2.5 kHz
   - Air boost: +1.5 dB @ 10 kHz shelf

5. **Multiband Compression**
   - Control dynamics across 4 bands
   - Gentle 1-3 dB gain reduction per band
   - Preserve transients and punch

### Optional Enhancements:

- Harmonic exciter (subtle warmth)
- Glue compressor (analog character)
- Stereo width enhancement (>2 kHz only)

### Delivery:

**Create TWO masters:**
1. Streaming: 44.1k/16bit, -14 LUFS, -1.0 dBTP
2. Promo/HD: 48k/24bit, -8 LUFS, -0.5 dBTP

---

## CONCLUSION

This track has **excellent potential** with proper mastering. The mix is clean, dynamic, and well-balanced spectrally. Key priorities:

1. **Stereo balance correction** (most important fix)
2. **Loudness optimization** (competitive levels)
3. **DROP enhancement** (maximum impact at 17.163s)
4. **Tonal shaping** (EQ for polish and character)

With these treatments, "СМОТРЕЛА" will achieve **professional streaming quality** and compete with commercial releases in the electronic/dramatic genre.

**Estimated Time Investment:**
- Setup chain: 30 minutes
- Tweaking/optimization: 1-2 hours
- A/B comparison: 30 minutes
- Export/QC: 30 minutes
- **Total: 3-4 hours** for full professional master

**Result:** Radio-ready, streaming-optimized, commercially competitive master.

---

**Report prepared by:** AI Mastering Engineer (Sterling Sound/Abbey Road standards)
**Date:** 2025-12-26
**Track:** СМОТРЕЛА by Саймурр
**Version:** Final Mastering Report v1.0

---

*Good luck with the master! This track has serious potential.* 🎚️🎵
