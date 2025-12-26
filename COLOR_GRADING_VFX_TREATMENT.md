# COLOR GRADING & VFX TREATMENT: "СМОТРЕЛА" TEASER

## ADVANCED VISUAL TREATMENT SPECIFICATION

**Colorist Notes:** This is a 37-second emotional journey from mystery to catharsis. Every grade serves the narrative arc. The green eyes are not just a color accent—they're the emotional anchor, the memory that haunts.

---

## 1. COLOR GRADING EVOLUTION

### MASTER LOOK FOUNDATION

**Base LUT Stack:**
1. **Primary:** ARRI LogC to Rec.709 conversion
2. **Creative:** Custom B&W conversion (NOT simple desaturation)
3. **Final:** Film emulation layer

**Custom B&W Formula (NOT simple desaturation):**
```
Red Channel:    40%
Green Channel:  40%
Blue Channel:   20%
```
*Rationale: Maximizes skin tone contrast and eye luminosity*

**Global Settings (All Sections):**
- Color Space: Rec.709 / sRGB
- Gamma: 2.4
- Black Point: Pure 0,0,0 RGB
- White Point: 235,235,235 RGB (broadcast safe)

---

### SECTION-BY-SECTION GRADING BREAKDOWN

#### **INTRO (0.000s - 4.320s): "The Void"**

**Mood:** Liminal, mysterious, almost dream-like

**Primary Corrections:**
- Lift (Shadows): -0.15 (crushed blacks for mystery)
- Gamma (Midtones): 0.95 (slightly darker, somber)
- Gain (Highlights): +0.08 (gentle glow on practical lights)
- Contrast: 1.25

**Curves:**
- **Luma Curve:** S-curve with toe crush
  - Shadows (0-25%): Hard black point at 0, lift to 15% at input 25%
  - Highlights (75-100%): Soft rolloff, max out at 92%
- **RGB Parade Target:** Deep blacks (0-10%), compressed mids (35-60%), gentle highs (80-92%)

**HSL Secondary (Skin Tones):**
- Hue: 15-35° (orange-red range)
- Saturation: 0% (kill all color)
- Luminance: +5% (skin should be slightly luminous in B&W)

**Vignette:**
- Amount: 35%
- Feather: 85%
- Roundness: 0.3 (subtle oval)

**Special Treatment:**
- **Empty Chair Shot (0.352s):** Add subtle bloom on spotlight
  - Threshold: 85%
  - Intensity: 15%
  - Radius: 25px

**Emotional Intent:** Cold, isolated, searching. The viewer should feel the absence.

---

#### **BUILD-UP (4.320s - 10.016s): "The Search"**

**Mood:** Agitation, increasing energy, fragmentation

**Primary Corrections:**
- Lift: -0.10 (slightly less crushed than intro)
- Gamma: 1.00 (neutral midtones for clarity)
- Gain: +0.12 (brighter highlights, more energy)
- Contrast: 1.35 (increased separation)

**Curves:**
- **Luma:** Steeper S-curve
  - Increased contrast in mids (40-70% range)
  - Highlights can reach 95%

**Dynamic Adjustment (CRITICAL):**
- **Crowd Shots:** Contrast +10% (chaos, fragmentation)
- **Hand/Piano Shots:** Contrast baseline (focus, control)

**Grain Introduction:**
- Size: 0.8 (fine grain)
- Intensity: 12%
- Type: Kodak 5219 emulation
- **Animation:** Static (no temporal variation yet)

**Vignette:**
- Amount: 25% (reduced from intro)
- Feather: 90%

**HSL Treatment:**
- **Practical lights in crowd:** Keep crushed, no detail
- **Skin in motion:** +8% luminance (hands should pop)

**Emotional Intent:** Fragmented reality, searching through memories, increasing urgency.

---

#### **PRE-DROP (10.016s - 17.163s): "The Breath Before"**

**Mood:** Suspended, intimate, time slowing down

**Primary Corrections:**
- Lift: -0.08 (bringing blacks up slightly)
- Gamma: 1.05 (brighter, clearer)
- Gain: +0.15 (luminous highlights)
- Contrast: 1.15 (REDUCED contrast for dreamlike quality)

**Curves:**
- **Luma:** Softer S-curve
  - Shadow rolloff (gentler blacks)
  - Highlight expansion (more detail in bright areas)
- **Target:** Milky blacks (5-12%), expanded mids (30-75%)

**Special Slow-Motion Grade:**
- Frame interpolation: Optical Flow (NOT frame blending)
- Motion blur: 180° shutter angle simulation
- **Temporal grain:** Grain follows motion vectors

**Focus on Empty Chair & Eye Close-ups:**
- **Selective sharpening:** +15% on focal plane
- **Gaussian blur:** 2px on background (simulated shallow DOF)
- **Highlight rolloff:** Softer, more "filmic" (reduce digital harshness)

**Vignette:**
- Amount: 15% (minimal, open feel)
- Feather: 95%

**Black Screen (16.500s - 17.163s):**
- Pure black: 0,0,0 RGB
- Duration: 663ms
- **Transition:** Hard cut to black at 16.500s
- **Audio:** Continue (visual silence only)

**Emotional Intent:** Intimacy before revelation. Time suspended. The moment before everything changes.

---

#### **DROP (17.163s - 25.003s): "The Recognition" 💥**

**Mood:** EXPLOSION, recognition, maximum visual energy

**Primary Corrections:**
- Lift: -0.20 (MAXIMUM black crush for impact)
- Gamma: 0.98 (punch in mids)
- Gain: +0.20 (MAXIMUM highlight extension)
- Contrast: 1.50 (MAXIMUM separation)

**Curves:**
- **Aggressive S-Curve:**
  - Blacks: Hard crush at 0-8%
  - Mids: Strong contrast 30-80% (steep slope)
  - Highlights: Hard clip at 98% (near-white)

**RGB Parade:** High dynamic range look
- Blacks: 0-5%
- Mids: Sharp peak at 45-55%
- Highlights: Extended to 95-98%

**Grain:**
- Intensity: 25% (INCREASED)
- **Temporal variation:** Active (grain dances with cuts)
- **On beat hits:** Momentary intensity spike to 35%

**Vignette:**
- Amount: 45% (HEAVY)
- Feather: 75% (sharper edge)
- **Pulsing:** Vignette intensity modulates ±5% on bass hits

**Flash Frames (White):**
- Timing: 19.891s - 20.021s (130ms)
- RGB: 255,255,255 (pure white)
- **Transition:** Instant cut (no fade)
- **Recovery:** 2-frame fade back (60ms @ 30fps)

**Emotional Intent:** The moment of recognition. Memory flooding back. Maximum visual assault synchronized with the DROP.

---

#### **CLIMAX (21.451s - 22.880s): "The Gaze Holds" 🔥**

**SPECIAL TREATMENT FOR HERO SHOT (V6 @ 14.2s - Direct eye contact)**

This is the emotional peak. 1.429 seconds of sustained eye contact.

**Primary Corrections:**
- Lift: -0.18
- Gamma: 1.02 (slight lift for clarity)
- Gain: +0.18
- Contrast: 1.45

**Selective Face Enhancement:**
- **Eyes:**
  - Sharpness: +25% (MAXIMUM clarity on iris)
  - Luminance: +12% (eyes should be most luminous element)
  - Micro-contrast: +8% (detail in iris structure)
- **Skin:**
  - Softening: Subtle 1px blur (separate eyes)
  - Luminance: +6%
  - Texture: Preserve (don't over-smooth)

**Slow Zoom Specification:**
- Start scale: 100%
- End scale: 105%
- Easing: Exponential ease-out
- Duration: 1.429s
- **Anchor point:** Between the eyes

**Vignette (Dynamic):**
- Start: 40%
- End: 50%
- **Gradient direction:** Radial from eyes
- Feather: 80%

**Grain:**
- Intensity: 20%
- **Freeze grain:** Lock grain pattern (no temporal variation)
- Rationale: Stability = emotional truth

**Emotional Intent:** Time stops. This is the moment. Direct confrontation with memory/loss/longing. The viewer cannot look away.

---

#### **PEAK (25.003s - 34.293s): "The Catharsis"**

**Mood:** Acceptance, bittersweet, gradual resolution

**Primary Corrections (Gradual transition):**

**@ 25s (Start of section):**
- Lift: -0.15
- Gamma: 1.00
- Gain: +0.15
- Contrast: 1.40

**@ 30s (Midpoint):**
- Lift: -0.12
- Gamma: 1.02
- Gain: +0.12
- Contrast: 1.30

**@ 34s (End of section):**
- Lift: -0.08
- Gamma: 1.05
- Gain: +0.08
- Contrast: 1.20

**Automated Keyframe Interpolation:**
- Type: Bezier smooth
- **Effect:** Gentle softening through the section

**Vignette (Gradual reduction):**
- @ 25s: 40%
- @ 34s: 20%
- Transition: Linear

**Grain (Gradual reduction):**
- @ 25s: 22%
- @ 34s: 15%
- Transition: Linear

**Emotional Intent:** Energy dissipating. Acceptance of the absence. Softening from the intensity.

---

#### **OUTRO (34.293s - 37.000s): "The Memory Remains"**

**Mood:** Fading, ethereal, final breath

**Primary Corrections:**
- Lift: -0.05 (gentle blacks)
- Gamma: 1.08 (lifted, luminous)
- Gain: +0.05 (soft highlights)
- Contrast: 1.10 (minimal contrast, dreamlike)

**Fade Specification:**

**Last Eye Shot (35.723s - 36.500s):**
- Opacity: 100% → 30%
- Duration: 777ms
- Curve: Exponential ease-in

**Final Black (36.500s - 37.000s):**
- Pure black: 0,0,0 RGB
- Title card: "СМОТРЕЛА"
  - Font: Futura Bold Condensed
  - Size: 72pt
  - Color: 255,255,255 RGB
  - Tracking: +50
  - Position: Center, lower third
  - Opacity fade-in: 250ms
  - Hold: 250ms (until track ends)

**Grain:**
- Intensity: 8% (minimal)
- **On black:** 5% (barely visible texture)

**Emotional Intent:** The dissolution. The memory fades but never disappears entirely. Quiet ending.

---

## 2. SELECTIVE COLOR STRATEGY: THE GREEN EYES

### EXACT HSV SPECIFICATION

**Isolation Method:** HSL Keyer + Luminance Qualification

**Step 1: HSL Key Parameters**
```
Hue Center:        160° (cyan-green, emerald)
Hue Range:         ±15° (145° - 175°)
Saturation Min:    20%
Saturation Max:    100%
Luminance Min:     15%
Luminance Max:     85%
```

**Step 2: Refinement**
- **Feather:** 8% (soft edge to blend naturally)
- **Edge blur:** 3px (avoid hard keying artifacts)
- **Matte cleanup:**
  - Erode: 1px
  - Blur: 2px
  - Expand: 1px
  - (Creates smooth, natural edge)

**Step 3: Color Application**

**Base Eye Color (All sections except variations below):**
```
Hue:          160° (emerald green)
Saturation:   75%
Luminance:    +15%
```

**RGB Values:** Approximately (20, 180, 120) in highlighted areas

---

### DYNAMIC GREEN INTENSITY (Music Energy Response)

**Energy-Based Modulation:**

| Section | Saturation | Luminance | Glow | Rationale |
|---------|------------|-----------|------|-----------|
| **INTRO** | 65% | +10% | None | Subtle, mysterious reveal |
| **BUILD-UP** | 70% | +12% | Minimal | Growing intensity |
| **PRE-DROP** | 75% | +15% | 5% | Anticipation |
| **DROP (17.163s flash)** | 95% | +25% | 25% | MAXIMUM IMPACT |
| **DROP (sustained)** | 85% | +20% | 15% | High energy |
| **CLIMAX (21.451s)** | 90% | +22% | 20% | Peak emotional moment |
| **PEAK** | 80% | +18% | 12% | Sustained intensity |
| **OUTRO** | 60% | +8% | None | Fading memory |

**Glow Specification:**
- **Plugin:** Sapphire S_Glow or native soft glow
- **Threshold:** 70% (only affects bright eye highlights)
- **Spread:** Variable (see table)
- **Color:** Match green (160° hue)
- **Blending:** Screen mode, 50% opacity

---

### BEAT-SYNCHRONIZED GREEN PULSING

**DROP Section (17.163s - 25.003s):**

Apply subtle luminance pulsing on strong beats:

**Pulse Parameters:**
```
Beat hits: Every 0.352s (BPM 170 grid)
Pulse curve: Quick rise, slow fall
Rise time: 50ms
Fall time: 250ms
Luminance range: +15% → +22% → +15%
```

**Keyframe Pattern (example for first 3 beats):**
```
17.163s: +25% (DROP hit - maximum)
17.213s: +20% (decay start)
17.515s: +15% (baseline)
17.565s: +22% (beat hit)
17.815s: +15% (baseline)
17.867s: +22% (beat hit)
... (continue pattern)
```

**Implementation:** Use expression/automation rather than manual keyframes

---

### OTHER SELECTIVE COLOR MOMENTS

**1. Warm Practicals (Subtle Hint):**

*Rationale:* Pure B&W can feel sterile. Barely visible warmth on light sources adds subliminal richness.

**When:** INTRO & PRE-DROP sections only
**What:** Spotlight on empty chair, window light

**Parameters:**
```
Hue:           30° (warm amber)
Saturation:    8% (BARELY visible)
Luminance:     +5%
Application:   Highlight areas only (>75% luminance)
```

**Isolation:** Luminance key (75-100%) + manual vignette mask on light sources

**2. Cool Shadows (Teal undertone):**

**When:** BUILD-UP & DROP sections (for contrast with green)
**What:** Deep shadow areas

**Parameters:**
```
Hue:           190° (cool cyan)
Saturation:    5% (extremely subtle)
Luminance:     0%
Application:   Shadow areas only (<20% luminance)
```

**Effect:** Creates subtle color contrast (cool shadows vs. warm highlights) even in "B&W"

---

### DESATURATION TECHNIQUE

**Method:** Channel Mixer (NOT simple desaturation)

**Why:** Preserves luminance relationships for more cinematic B&W with better skin tones and eye contrast.

**Channel Mixer Settings:**

**Red Output:**
```
Red:    40%
Green:  40%
Blue:   20%
Total:  100%
```

**Green Output:**
```
Red:    40%
Green:  40%
Blue:   20%
Total:  100%
```

**Blue Output:**
```
Red:    40%
Green:  40%
Blue:   20%
Total:  100%
```

**Result:** All three channels receive the same weighted mix = desaturation, but with optimal contrast for faces and eyes.

**Alternative (for deeper blacks):**
```
Red:    35%
Green:  45%
Blue:   20%
```
(Emphasizes green channel data = better skin separation)

**Post-Mix Adjustment:**
- Apply selective green eye color AFTER channel mixer
- This ensures the eye color sits "on top" of the B&W base

---

## 3. VFX ELEMENTS

### FILM GRAIN

**Base Grain (All Sections):**
- **Plugin:** Dehancer, FilmConvert Nitrate, or native Film Grain
- **Film Stock Emulation:** Kodak Vision3 5219 500T (pushed 1 stop)
- **Scan Resolution:** 4K scan simulation
- **Grain Structure:** Organic, non-uniform

**Technical Parameters:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| Size | 0.8 | Fine grain (35mm look) |
| Intensity (Luma) | Variable | See dynamic table below |
| Intensity (Chroma) | 5% | Minimal color grain (it's B&W, but adds texture) |
| Highlights | 100% | Grain visible in bright areas |
| Midtones | 100% | Full grain in mids |
| Shadows | 85% | Slightly reduced in deep blacks |
| Temporal behavior | Variable | Static or animated depending on section |

**Dynamic Grain Intensity by Section:**

| Section | Intensity | Temporal | Rationale |
|---------|-----------|----------|-----------|
| INTRO | 15% | Static | Stable, contemplative |
| BUILD-UP | 18% | Animated (slow) | Growing energy |
| PRE-DROP | 12% | Static | Calm before storm |
| DROP | 28% | Animated (fast) | Maximum chaos/energy |
| CLIMAX (21.451s hero shot) | 18% | **FROZEN** | Stability = truth |
| PEAK | 22% | Animated (medium) | Sustained energy |
| OUTRO | 10% | Static (fading) | Dissolving |

**Beat-Reactive Grain (DROP section only):**
- On bass hits: +7% intensity spike
- Duration: 100ms
- Falloff: 200ms
- **Effect:** Grain "punches" with the music

**Grain Color Tint:**
- Highlights: Slightly warm (RGB: 255, 254, 250)
- Shadows: Slightly cool (RGB: 0, 0, 2)
- **Effect:** Subtle film stock color cross-talk

---

### LENS EFFECTS

#### **Chromatic Aberration**

**When:** Entire video
**Amount:** Subtle (0.15% - 0.3%)

**Technical Spec:**
```
Red Channel Shift:    +0.2% radial outward
Blue Channel Shift:   -0.2% radial inward
Green Channel:        No shift (reference)
Center Point:         Frame center
Falloff:              Quadratic (stronger at edges)
```

**Per-Section Variation:**

| Section | Amount | Notes |
|---------|--------|-------|
| INTRO | 0.15% | Minimal |
| BUILD-UP | 0.20% | Slightly increased |
| PRE-DROP | 0.12% | Reduced (cleaner) |
| DROP | 0.35% | MAXIMUM (adds chaos) |
| CLIMAX | 0.10% | Minimal (clarity) |
| PEAK | 0.25% | Medium-high |
| OUTRO | 0.15% | Return to subtle |

**Special Note for Eye Shots:**
- **Reduce CA to 0.05%** on close-up eye shots
- Rationale: Eyes should be sharp, clear, perfect

---

#### **Lens Distortion (Barrel/Pincushion)**

**When:** Selectively applied
**Type:** Barrel distortion (bulging)

**Applications:**

**1. Empty Chair Shots:**
- Amount: -0.5% (subtle pincushion)
- Effect: Slight compression toward center
- Emotional intent: Isolation, drawing in

**2. Close-up Eye Shots (Climax):**
- Amount: +0.3% (subtle barrel)
- Effect: Slight expansion
- Emotional intent: Intensity, presence

**3. Crowd/Chaos Shots:**
- Amount: +0.8% (noticeable barrel)
- Effect: Dynamic distortion
- Emotional intent: Disorientation

**Global Settings:**
- Center: Frame center
- Preserve aspect: Yes
- Edge behavior: Stretch (not crop)

---

### LIGHT LEAKS

**Philosophy:** Use sparingly. Light leaks should feel like happy accidents, not Instagram filters.

**When to Apply:**

**1. Transition to DROP (17.163s):**
- Type: White/cyan diagonal streak
- Position: Top right corner
- Opacity: 25%
- Blending: Screen
- Duration: 400ms (quick flash)
- Motion: Slight downward drift
- **Color:** Desaturated cyan (190°, 15% sat)

**2. CLIMAX Eye Contact (21.451s):**
- Type: Subtle golden edge leak
- Position: Left edge
- Opacity: 15%
- Blending: Add
- Duration: Full 1.429s hold
- Motion: Static
- **Color:** Warm amber (30°, 12% sat)
- **Effect:** Adds warmth to the moment

**3. OUTRO Fade (35.723s):**
- Type: Soft white bloom
- Position: Radial from center
- Opacity: 20% → 0%
- Blending: Screen
- Duration: 777ms (entire fade)
- **Effect:** "Overexposed" memory fading

**Creation Method:**
- Use real light leak overlays (practical film scans)
- **NOT** digital gradients
- Recommended: Film Looks library, Video Copilot Twitch

**Global Light Leak Settings:**
- Blur: 40% (soft, diffused)
- Edge feather: 90%
- Tracking: None (static overlays feel more organic)

---

### FLICKER EFFECTS

**Philosophy:** Simulate vintage film/projector instability. Should be subliminal.

**Global Flicker (All Sections):**

**Luminance Flicker:**
```
Amount:      ±2% (subtle)
Frequency:   24Hz (film projector rate)
Pattern:     Organic (not perfectly rhythmic)
Seed:        Random per frame
```

**Implementation:**
- Add noise to Gain parameter
- **Curve:** Slight randomization, biased toward darker
- Should not be consciously noticeable, only felt

**Beat-Synchronized Flicker (DROP section):**

On each beat hit (every 0.352s):
```
Luminance drop: -8%
Duration:       50ms (flash down)
Recovery:       150ms (fade back up)
Curve:          Fast drop, slow recovery
```

**Effect:** Image "punches" darker on beats, creating subliminal rhythm

**Special Flicker Events:**

**1. Pre-DROP Black Screen (16.500s - 17.163s):**
- Random luminance variation: ±5%
- **Effect:** Black isn't perfectly stable (tension)

**2. Flash to White (19.891s):**
- Flicker during recovery (20.021s - 20.100s)
- Rapid luminance variation: ±15%
- **Effect:** "Blown out film" recovery

---

### HALATION / BLOOM

**What:** Soft glow around bright highlights, simulating film halation

**When:** Entire video
**Amount:** Variable by section

**Technical Parameters:**

**Base Settings:**
```
Threshold:   75% (only bright areas)
Intensity:   Variable (see table)
Radius:      20-35px (depending on section)
Color:       Match source (white → white glow)
Falloff:     Gaussian
Blending:    Screen mode
```

**Per-Section Variation:**

| Section | Intensity | Radius | Notes |
|---------|-----------|--------|-------|
| INTRO | 12% | 20px | Gentle glow on spotlight |
| BUILD-UP | 8% | 15px | Minimal (clarity) |
| PRE-DROP | 15% | 25px | Soft, dreamlike |
| DROP | 30% | 35px | MAXIMUM (explosive) |
| CLIMAX | 25% | 30px | Strong but controlled |
| PEAK | 20% | 25px | Medium |
| OUTRO | 18% | 22px | Gentle fade |

**Special Applications:**

**1. Green Eyes (All Sections):**
- **Separate bloom layer** for eyes
- Threshold: 60% (catches eye highlights)
- Intensity: +10% above base
- Color: Green (160° hue)
- **Effect:** Eyes "glow" with their own light

**2. Spotlight on Empty Chair:**
- Intensity: 35%
- Radius: 40px
- **Effect:** Ethereal, heavenly quality

**3. Flash Frame (20.021s):**
- Intensity: 100% (maximum)
- Radius: 80px (huge spread)
- **Effect:** Complete blown-out bloom

---

### LETTERBOXING / ASPECT RATIO

**Letterbox Specification:**

**Format:** 2.39:1 (Anamorphic / Cinemascope)
**Base Resolution:** 1920x1080 (16:9)
**Letterbox Bars:** Top and bottom

**Calculations:**
```
Image height at 2.39:1: 803px
Bar height (each):      138.5px
Total bars:             277px
```

**Letterbox Color:** Pure black (0,0,0 RGB)

**Edge Treatment:**
- **Hard edge** (no feather)
- Rationale: Clean, cinematic

**Text Safe Area:**
- Keep title/credits within central 80% of visible area
- Avoid placement within 69px of letterbox edge

**Anamorphic Characteristics (Optional Enhancement):**

If adding anamorphic lens simulation:
1. **Horizontal lens flares:** Blue streak on practicals
2. **Bokeh shape:** Oval (2:1 ratio)
3. **Focus breathing:** Slight horizontal squeeze on focus pulls
4. **Edge distortion:** Minimal anamorphic mumps (0.05%)

**Recommendation:** Keep minimal. The B&W + green eyes is already a strong look. Don't over-stylize.

---

## 4. SPECIAL MOMENT TREATMENTS

### DROP FLASH EFFECT (17.163s) 💥

**This is THE moment. Must be perfect.**

**Sequence Breakdown (frame-by-frame @ 30fps):**

**Frame -1 (17.130s):**
- Pure black (end of pre-drop silence)

**Frame 0 (17.163s - DROP HIT):**
- **Instant white flash**
- RGB: 255, 255, 255
- Duration: 1 frame (33ms)

**Frame 1 (17.196s):**
- **Eye shot appears**
- Simultaneously:
  - Zoom from 120% → 100% (instant scale)
  - Chromatic aberration: 2% (extreme, then reduces)
  - Green saturation: 95%
  - Green luminance: +25%
  - Green glow: 25%
  - Vignette: 60% → 45% (quick reduction)
  - Grain spike: 35%
  - Halation: 40%

**Frames 2-3 (17.229s - 17.262s):**
- **Recovery animation:**
  - Chromatic aberration: 2% → 0.35% (fast reduction)
  - Vignette: 45% → 40% (settle)
  - Grain: 35% → 28% (settle)
  - Halation: 40% → 30% (settle)
- Easing: Exponential ease-out

**Frame 4+ (17.295s onward):**
- **Settled state:**
  - All parameters at DROP baseline
  - Continue with beat-synced pulsing

**Additional Elements:**

**1. Radial Blur (Impact):**
- Applied to Frame 0-1 only
- Center: Between eyes
- Amount: 15%
- Feather: 100%
- **Effect:** Explosive energy radiating from eyes

**2. Edge Glitch:**
- Applied to Frame 1 only
- RGB channel offset:
  - Red: +5px horizontal
  - Blue: -5px horizontal
- **Effect:** Digital "shock" impact

**3. Camera Shake:**
- Frames 0-5
- Amount: ±3px horizontal, ±2px vertical
- Pattern: Random but decreasing
- Easing: Exponential decay
- **Effect:** Physical impact feeling

**Audio-Visual Sync:**
- Flash must be EXACTLY on 17.163s
- Verify with waveform: Should hit on transient peak
- Tolerance: ±16ms (half frame @ 30fps)

---

### CLIMAX VISUAL PEAK (21.451s - 22.880s) 🔥

**The Sustained Gaze: 1.429 seconds of pure emotional connection**

**Shot:** V6 @ 14.2s (direct eye contact into camera)

**This is not a flash—it's a HOLD. Everything else disappears.**

**Grading:**
- Use "CLIMAX" grade from Section 1
- Freeze grain pattern (locked seed)
- Maximum eye enhancement

**Camera Movement (Slow Push-In):**
```
Start: 100% scale
End: 105% scale
Duration: 1.429s
Easing: Exponential ease-out (starts fast, ends slow)
Anchor: Center between eyes
```

**Purpose:** Gradually increasing intimacy

**Vignette Animation:**
```
Start (21.451s): 40% intensity
End (22.880s):   50% intensity
Transition:      Linear
```

**Effect:** World contracts around the eyes

**Green Eye Treatment (Special):**
- Saturation: 90%
- Luminance: +22%
- Glow: 20%
- **Micro-animation:** Subtle luminance pulse
  - Range: +22% → +24% → +22%
  - Duration: One cycle per second (2 cycles total)
  - Pattern: Sine wave (smooth)
  - **Effect:** "Breathing" quality, alive

**Subtle Elements:**

**1. Edge Light Leak:**
- Position: Left edge
- Color: Warm amber (30°, 12% sat)
- Opacity: 15%
- **Effect:** Subliminal warmth

**2. Minimal Chromatic Aberration:**
- Amount: 0.10%
- **Effect:** Maximum clarity (reduce distortion)

**3. Selective Sharpening:**
- Eyes: +25%
- Skin: -5% (slight blur for separation)
- **Method:** Luminance-based mask

**Audio-Visual Relationship:**
- This hold occurs during sustained musical energy
- **No cuts** during this moment
- Let it breathe, let the viewer sit with it

**Emotional Intent:**
Direct confrontation with the gaze. No escape. This is the face that haunts. The memory crystallized. Time stops.

---

### TRANSITION EFFECTS BETWEEN SECTIONS

**Philosophy:** Transitions should serve the narrative, not distract from it.

**1. INTRO → BUILD-UP (4.320s):**

**Type:** Hard cut
**On:** Strong beat
**Enhancement:**
- 2-frame fade (60ms) to soften slightly
- Grain increase on cut (15% → 18%)
- **Effect:** Abrupt shift from contemplation to search

---

**2. BUILD-UP → PRE-DROP (10.016s):**

**Type:** Match cut on movement
**Details:**
- Cut from hands in motion to hands on piano
- **Motion match:** Continue similar gesture across cut
- Time remap: 100% speed → 50% speed
- **Effect:** Sudden deceleration, time stretching

**Enhancement:**
- Contrast reduction (1.35 → 1.15)
- Vignette reduction (25% → 15%)
- **Sound design suggestion:** Reverb increase on audio

---

**3. PRE-DROP → DROP (17.163s):**

**Type:** Flash cut (detailed in DROP section above)

**The most important transition in the entire piece.**

**Recap:**
- Black screen @ 16.500s
- Silence (visual) for 663ms
- White flash @ 17.163s (1 frame)
- Eyes appear @ 17.196s

**Enhancement:**
- Maximum contrast shift (1.15 → 1.50)
- Maximum grain increase (12% → 28%)
- Maximum vignette increase (15% → 45%)
- **Effect:** EXPLOSION

---

**4. DROP → PEAK (25.003s):**

**Type:** Seamless continuation (no visible transition)

**Rationale:** Energy doesn't drop, just stabilizes

**Subtle shift:**
- Grain: 28% → 22% (gradual over 1 second)
- Vignette: 45% → 40% (gradual)
- **Effect:** Sustained but slightly softer

---

**5. PEAK → OUTRO (34.293s):**

**Type:** Cross dissolve
**Duration:** 1.0 second
**Details:**
- Outgoing: Piano hands
- Incoming: Empty chair
- **Overlap:** 500ms on each side

**Enhancement:**
- Contrast gradual reduction (1.30 → 1.10)
- Vignette gradual reduction (25% → 15%)
- Grain gradual reduction (18% → 10%)
- **Effect:** Energy dissipating, settling

---

**6. OUTRO → BLACK (36.500s):**

**Type:** Fade to black
**Duration:** 500ms
**Details:**
- Opacity: 100% → 0%
- Curve: Exponential ease-in (starts slow, accelerates)

**Enhancement:**
- Final eye shot dissolves
- Grain fades with image (10% → 0%)
- **Effect:** Dissolution of memory

---

## 5. ADVANCED TECHNIQUES

### SPEED RAMPING CURVES

**PRE-DROP Slow Motion (10.016s - 17.163s):**

**Method:** Time remapping with optical flow interpolation

**Sections within PRE-DROP:**

| Shot | Original Speed | Remap Speed | Duration | Interpolation |
|------|----------------|-------------|----------|---------------|
| Empty chair + pianist | 100% | 50% | 1.397s | Optical Flow |
| Profile side light | 100% | 60% | 1.366s | Optical Flow |
| Empty chair + curtain | 100% | 100% | 1.493s | None (hold) |
| Chair under spotlight | 100% | 40% | 1.547s | Optical Flow + Frame blend |
| Eye close-up | 100% | 30% | 0.681s | Optical Flow |

**Optical Flow Settings:**
```
Quality:        High
Motion blur:    Enabled
Shutter angle:  180°
Vector detail:  Fine (avoid warping artifacts)
Fallback:       Frame blend (if flow fails)
```

**Purpose:** Extreme slow motion (30-60% speed) creates suspended, dream-like quality

---

**DROP/PEAK Speed Variations:**

**Crowd Shots (selective):**
- Speed ramp: 100% → 150% (speed up)
- Duration: 200ms ramp
- **Effect:** Frenetic energy

**Eye Moments:**
- Speed: 100% or 80% (slight slow-mo)
- **Effect:** Emphasis, importance

---

### FRAME BLENDING FOR SMOOTHNESS

**When to Use:**
- Slow motion sections where optical flow creates artifacts
- Fast cuts to add motion blur
- Speed ramps

**Settings:**

**For Slow Motion:**
```
Blend mode:      Frame mix
Blend amount:    50%
Samples:         2 frames
```

**Effect:** Natural motion blur on slowed footage

**For Fast Cuts (BUILD-UP section):**
```
Blend:           1 frame overlap
Amount:          25%
```

**Effect:** Softens jarring cuts slightly, more cinematic

**Do NOT use on:**
- Static shots (no motion)
- CLIMAX hero shot (needs sharpness)
- Flash frames (needs hard cut)

---

### SHUTTER ANGLE SIMULATION

**Philosophy:** Most digital footage is shot at 180° shutter (natural motion blur). We can enhance or modify this.

**Applications:**

**1. Action/Crowd Shots (BUILD-UP, DROP):**
- Simulated shutter: 90° (reduced motion blur)
- **Method:** Frame sampling or ReelSmart Motion Blur with reduced amount
- **Effect:** Sharper, more staccato motion (Private Ryan-style)

**2. Dreamy Moments (PRE-DROP, OUTRO):**
- Simulated shutter: 360° (increased motion blur)
- **Method:** ReelSmart Motion Blur or directional blur
- **Effect:** Softer, more flowing motion

**Implementation (Plugin-Based):**

**ReelSmart Motion Blur Pro:**
```
Motion sensitivity:  80%
Blur amount:         Variable by shot
Reduce noise:        On
Edge artifacts:      Minimize
```

**Manual Method (if no plugin):**
```
1. Duplicate layer
2. Offset by +1 frame
3. Blend at 50% opacity
4. Apply directional blur (2-3px in motion direction)
```

---

### ANAMORPHIC CHARACTERISTICS

**Optional Enhancement** (applies if client wants elevated cinematic look)

**Anamorphic Lens Simulation:**

**1. Aspect Ratio:**
- Already using 2.39:1 letterbox ✓

**2. Horizontal Lens Flares:**

**When:** Practicals (lights) in frame
**Characteristics:**
- Direction: Horizontal streak
- Color: Cyan-blue (190° hue)
- Length: 30-50% of frame width
- Intensity: 15-25%
- **Occurs on:**
  - Spotlight on empty chair
  - Window light
  - Any practical light source

**Implementation:**
- Plugin: Video Copilot Optical Flares (Anamorphic preset)
- Manual: Horizontal motion blur on light sources + cyan color

**Settings:**
```
Streak length:    Variable (30-50% frame width)
Falloff:          Exponential
Color:            Cyan (RGB: 100, 180, 255)
Opacity:          20%
Blend:            Screen
```

**3. Oval Bokeh:**

**When:** Out-of-focus elements (if any exist)
**Shape:** Horizontal oval (2:1 ratio)

**Implementation:**
- Camera lens blur with custom bokeh shape
- Create 2:1 oval shape image as bokeh map

**4. Anamorphic Mumps (Edge Distortion):**

**Amount:** 0.05% (extremely subtle)
**Type:** Horizontal stretch at frame edges
**Area affected:** Outer 15% of frame

**Effect:** Subtle horizontal "squeezing" of vertical lines near edges

**Recommendation:**
Keep this MINIMAL. The B&W + selective green + grain + letterbox is already a strong aesthetic. Anamorphic elements should be barely noticeable, adding subliminal cinematic quality without being overt.

---

## TECHNICAL IMPLEMENTATION GUIDE

### SOFTWARE RECOMMENDATIONS

**Primary:** DaVinci Resolve Studio (Best for color + VFX integration)
**Alternative:** Adobe Premiere Pro + After Effects

**DaVinci Resolve Workflow:**

1. **Edit Page:** Rough cut assembly
2. **Color Page:** All grading (this is where you live)
3. **Fusion Page:** VFX elements (grain, flares, glitches)
4. **Deliver Page:** Export

---

### NODE STRUCTURE (DaVinci Resolve)

**Recommended Node Tree for Each Clip:**

```
[1 Input] → [2 B&W Conversion] → [3 Primary Grade] → [4 Curves] →
[5 Secondary - Skin] → [6 Secondary - Green Eyes] → [7 Vignette] →
[8 Grain] → [9 Halation] → [10 CA/Distortion] → [11 Output]
```

**Node Details:**

**Node 1 - Input:**
- Color space transform if needed
- Noise reduction (subtle, 5-10%)

**Node 2 - B&W Conversion:**
- Channel Mixer method (specified earlier)
- Monochrome mode OFF (keep RGB for later)

**Node 3 - Primary Grade:**
- Lift, Gamma, Gain adjustments (per section)
- Primary contrast

**Node 4 - Curves:**
- Custom luma curves (per section)
- RGB parade monitoring

**Node 5 - Secondary (Skin):**
- HSL key for skin tones (15-35° hue)
- Luminance +5% to +8%
- Ensure skin has proper B&W tonality

**Node 6 - Secondary (Green Eyes):**
- HSL key (160° ±15°)
- Apply green color
- Dynamic saturation/luminance (keyframed per section)
- Glow effect (outside node tree, parallel)

**Node 7 - Vignette:**
- Power window (oval)
- Variable intensity (keyframed)

**Node 8 - Grain:**
- Film Grain effect or plugin
- Variable intensity (keyframed per section)

**Node 9 - Halation/Bloom:**
- Soft glow on highlights
- Threshold 75%

**Node 10 - CA/Distortion:**
- Lens Distortion effect
- Channel-separated CA

**Node 11 - Output:**
- Final adjustments
- Color space transform to Rec.709

---

### RENDER SETTINGS

**Export Specifications:**

```
Format:          H.264 (MP4) or ProRes 422 HQ (for mastering)
Resolution:      1920 x 1080
Frame Rate:      30 fps (EXACT - no pulldown)
Bit Rate:        20 Mbps (H.264) or Maximum (ProRes)
Color Space:     Rec. 709
Color Range:     Limited (16-235)
Audio:           48kHz, 24-bit, Stereo
```

**Quality Checks Before Export:**

1. ✓ All cuts on beat (±0.05s tolerance)
2. ✓ Green eyes isolated correctly (no spill, no holes)
3. ✓ Grain consistent across cuts
4. ✓ Audio sync verified at:
   - 17.163s (DROP flash)
   - 21.451s (CLIMAX)
   - All major beats
5. ✓ Letterbox bars pure black (0,0,0)
6. ✓ No clipping (RGB parade < 235)
7. ✓ No crushed blacks (RGB parade > 0) unless intentional

---

## COLOR GRADING REFERENCE IMAGES

**Mood Board (Mental Reference):**

**B&W Inspiration:**
- *Sin City* (2005) - High contrast, selective color
- *Schindler's List* (1993) - Girl in red coat
- *The Lighthouse* (2019) - Harsh blacks, film grain
- *Joker* (2019) - Desaturated except key elements

**Eye Contact Moments:**
- *Blade Runner 2049* (2017) - Intimate close-ups, glowing eyes
- *Under the Skin* (2013) - Alien eye shots, unsettling gaze
- *Ex Machina* (2014) - Ava's penetrating stare

**Grain/Texture:**
- *Dunkirk* (2017) - IMAX 70mm grain structure
- *No Time to Die* (2021) - Kodak Vision3 500T look

---

## FINAL NOTES FOR COLORIST

**Emotional Journey Recap:**

```
VOID → SEARCH → SUSPENSION → EXPLOSION → CONNECTION → CATHARSIS → DISSOLUTION
```

Every grade decision serves this arc.

**Key Principles:**

1. **Contrast is Drama:** High contrast = high emotion
2. **The Eyes are Everything:** They should glow like an emerald in coal
3. **Grain is Texture:** It makes digital feel organic, real
4. **Black is Sacred:** Don't be afraid of pure blacks
5. **Restraint is Power:** Not every moment needs maximum treatment

**The Hero Moment (21.451s):**
If you have to choose ONE moment to get perfect, it's this. The direct gaze. Everything else can be good. This must be PERFECT.

**Final Check:**
Watch the entire piece without focusing on technical. Do you FEEL the journey? Does the DROP hit you? Does the gaze hold you? Does the outro leave you with something?

If yes, the grade is done.
If no, return to the emotional intent and adjust.

**Technical perfection serves emotional truth. Never the reverse.**

---

## APPENDIX: EXACT TIMECODE KEYFRAME MAP

**For precision implementation, here are exact keyframe points for critical parameters:**

### VIGNETTE INTENSITY KEYFRAMES

```
00.000s:  35%
04.320s:  25% (transition 500ms)
10.016s:  15% (transition 1000ms)
17.163s:  45% (INSTANT jump)
21.451s:  40% (transition 200ms)
25.003s:  40%
30.000s:  30% (gradual)
34.293s:  20% (gradual)
37.000s:  0% (fade out)
```

### GRAIN INTENSITY KEYFRAMES

```
00.000s:  15%
04.320s:  18% (transition 200ms)
10.016s:  12% (transition 500ms)
17.163s:  28% (INSTANT jump)
21.451s:  18% (transition 100ms, freeze pattern)
25.003s:  22%
30.000s:  18% (gradual)
34.293s:  10% (gradual)
37.000s:  0% (fade out)
```

### GREEN EYE SATURATION KEYFRAMES

```
First appearance (varies by shot):
- INTRO:          65%
- BUILD:          70%
- PRE-DROP:       75%
- 17.163s DROP:   95% (with +25% luminance spike)
- DROP sustained: 85%
- 21.451s CLIMAX: 90% (with pulse animation)
- PEAK:           80%
- OUTRO:          60%
```

### CONTRAST KEYFRAMES (Primary Contrast Slider)

```
00.000s:  1.25
04.320s:  1.35
10.016s:  1.15
17.163s:  1.50 (INSTANT)
21.451s:  1.45
25.003s:  1.40
30.000s:  1.30
34.293s:  1.20
35.723s:  1.10
```

---

**Document Version:** 1.0
**Date:** 2025-12-25
**Project:** СМОТРЕЛА - Teaser
**Prepared by:** Color Grading & VFX Supervisor

**Total Page Count:** Advanced Technical Specification

This document provides Hollywood-level color grading and VFX specifications. Every parameter has been designed to serve the emotional journey from mystery to catharsis.

**THE GAZE REMEMBERS. MAKE IT UNFORGETTABLE.**
