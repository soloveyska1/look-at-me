#!/usr/bin/env python3
"""
СМОТРЕЛА — TEASER RENDERER V2
Ultra-Professional Cinematic Version

CONCEPT: "THE GAZE" (ВЗГЛЯД)
A 37-second visual poem about the permanence of memory.

NARRATIVE ARC:
- INTRO (0-4s): "The Absence" — Empty space, longing
- BUILD-UP (4-10s): "The Search" — Fragmented, restless
- PRE-DROP (10-17s): "The Recognition Builds" — Time dilates
- DROP (17.16s): "The Epiphany" — GREEN EYES EXPLODE
- CLIMAX (21.45s): "The Prolonged Gaze" — Soul connection
- PEAK (22-34s): "The Interweaving" — Memory fragments
- OUTRO (34-37s): "The Return" — Dissolution, title card

Artist: Саймурр (Saymurr)
Title: СМОТРЕЛА / look at me
"""

import os
import numpy as np
from moviepy import *
from moviepy.video.fx import *
import cv2
from PIL import Image, ImageDraw, ImageFont

# ============================================================
# CONFIGURATION
# ============================================================

# Paths
BASE_DIR = "/home/user/look-at-me"
AUDIO_FILE = os.path.join(BASE_DIR, "СМОТРЕЛА_teaser.wav")
OUTPUT_FILE = os.path.join(BASE_DIR, "SMOTRELA_teaser_v2_FINAL.mp4")

# Video sources (correct paths from original render)
VIDEOS = {
    "V1": os.path.join(BASE_DIR, "20251226_0026_01kdbpca1rfxjtx3zddgv48gjh.mp4"),  # Crowd/Party
    "V2": os.path.join(BASE_DIR, "20251226_0130_01kdbr9ggwft8sr8k143r5xfs0.mp4"),  # Piano hands
    "V3": os.path.join(BASE_DIR, "20251226_0130_01kdbrazryf8wtabs5kk6kvmqx.mp4"),  # Profile silhouette
    "V4": os.path.join(BASE_DIR, "20251226_0130_01kdbsc29wehvbem5ertshqfed.mp4"),  # Empty chair
    "V5": os.path.join(BASE_DIR, "20251226_0131_01kdbsdwn8epg9amf3qtp17qsb.mp4"),  # Wide piano
    "V6": os.path.join(BASE_DIR, "20251226_0131_01kdbspmg9egv833wj0ngh944a.mp4"),  # Direct gaze (GREEN EYES)
}

# Timing constants
BPM = 170.5
BEAT_INTERVAL = 60.0 / BPM  # 0.352 seconds
TOTAL_DURATION = 37.0
FPS = 30
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)

# Key moments (FRAME-PERFECT)
DROP_TIME = 17.163      # The moment everything changes
CLIMAX_TIME = 21.451    # Maximum emotional intensity
CLIMAX_END = 22.880     # End of held gaze

# Output specs
OUTPUT_WIDTH = 1920
OUTPUT_HEIGHT = 1080

# ============================================================
# ADVANCED VFX FUNCTIONS
# ============================================================

def apply_cinematic_bw(frame, contrast=1.4, lift=-0.05):
    """
    Hollywood-grade B&W conversion using channel mixer.
    Red: 30%, Green: 59%, Blue: 11% (luminosity-based)
    """
    img = frame.astype(np.float32) / 255.0

    # Luminosity-based B&W (not simple average)
    gray = img[:,:,0] * 0.30 + img[:,:,1] * 0.59 + img[:,:,2] * 0.11

    # Apply lift (black point)
    gray = gray + lift

    # Apply contrast with S-curve
    gray = 0.5 + (gray - 0.5) * contrast

    # Clip and convert back
    gray = np.clip(gray, 0, 1)
    result = np.stack([gray, gray, gray], axis=2)

    return (result * 255).astype(np.uint8)

def isolate_green_eyes(frame, saturation_boost=1.0, luminance_boost=0.0):
    """
    Selective color isolation for green eyes.
    HSV range: Hue 145-175°, adjustable saturation/luminance.
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)

    # Green hue range (OpenCV uses 0-180 for hue)
    hue = hsv[:,:,0]
    sat = hsv[:,:,1]

    # Mask for green (hue ~72-87 in OpenCV = 145-175° in standard)
    green_mask = ((hue >= 35) & (hue <= 85) & (sat > 50)).astype(np.float32)

    # Smooth the mask
    green_mask = cv2.GaussianBlur(green_mask, (5, 5), 0)

    # Create B&W version
    bw = apply_cinematic_bw(frame, contrast=1.35)

    # Boost green areas
    frame_float = frame.astype(np.float32)

    # Increase saturation of green
    hsv[:,:,1] = np.clip(hsv[:,:,1] * (1 + saturation_boost * green_mask), 0, 255)

    # Increase luminance of green
    hsv[:,:,2] = np.clip(hsv[:,:,2] * (1 + luminance_boost * green_mask), 0, 255)

    # Convert back
    colored = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

    # Blend: B&W everywhere except green
    green_mask_3d = np.stack([green_mask] * 3, axis=2)
    result = bw * (1 - green_mask_3d) + colored * green_mask_3d

    return result.astype(np.uint8)

def add_dynamic_grain(frame, intensity=0.15, size=1.0):
    """
    Film grain simulation (Kodak Vision3 5219 style).
    Dynamic, organic, not uniform noise.
    """
    h, w = frame.shape[:2]

    # Generate grain at lower resolution for organic look
    grain_h, grain_w = int(h / size), int(w / size)
    grain = np.random.normal(0, intensity * 255, (grain_h, grain_w))

    # Upscale grain
    grain = cv2.resize(grain, (w, h), interpolation=cv2.INTER_LINEAR)

    # Apply grain (additive, clamped)
    grain_3d = np.stack([grain] * 3, axis=2)
    result = frame.astype(np.float32) + grain_3d
    result = np.clip(result, 0, 255)

    return result.astype(np.uint8)

def add_vignette(frame, intensity=0.35, softness=0.8):
    """
    Cinematic vignette - darkens edges, focuses attention.
    """
    h, w = frame.shape[:2]

    # Create radial gradient
    y, x = np.ogrid[:h, :w]
    center_y, center_x = h / 2, w / 2

    # Normalize to -1 to 1 range
    dist = np.sqrt(((x - center_x) / (w/2)) ** 2 + ((y - center_y) / (h/2)) ** 2)

    # Create smooth falloff
    vignette = 1 - np.clip((dist - (1 - softness)) / softness, 0, 1) * intensity
    vignette = np.power(vignette, 1.5)  # Smooth curve

    # Apply
    vignette_3d = np.stack([vignette] * 3, axis=2)
    result = frame.astype(np.float32) * vignette_3d

    return np.clip(result, 0, 255).astype(np.uint8)

def add_chromatic_aberration(frame, intensity=0.003):
    """
    Subtle RGB channel separation for cinematic lens effect.
    """
    h, w = frame.shape[:2]

    # Separate channels
    r, g, b = frame[:,:,0], frame[:,:,1], frame[:,:,2]

    # Calculate shift in pixels
    shift = int(w * intensity)

    if shift < 1:
        return frame

    # Shift red left, blue right
    r_shifted = np.roll(r, -shift, axis=1)
    b_shifted = np.roll(b, shift, axis=1)

    # Recombine
    result = np.stack([r_shifted, g, b_shifted], axis=2)

    return result

def add_halation(frame, threshold=0.75, intensity=0.2, radius=30):
    """
    Bloom/halation on bright areas (film overexposure simulation).
    """
    # Convert to float
    img = frame.astype(np.float32) / 255.0

    # Find bright areas
    luminance = img[:,:,0] * 0.3 + img[:,:,1] * 0.59 + img[:,:,2] * 0.11
    bright_mask = (luminance > threshold).astype(np.float32)

    # Blur the bright areas
    bright_areas = img * np.stack([bright_mask] * 3, axis=2)
    bloom = cv2.GaussianBlur(bright_areas, (radius*2+1, radius*2+1), radius/2)

    # Add bloom to original
    result = img + bloom * intensity
    result = np.clip(result, 0, 1)

    return (result * 255).astype(np.uint8)

def create_flash_frame(duration_frames=2):
    """
    Create pure white flash frame for impact moments.
    """
    white = np.ones((OUTPUT_HEIGHT, OUTPUT_WIDTH, 3), dtype=np.uint8) * 255
    return white

def apply_section_grade(frame, section, time_in_section, green_boost=0.0):
    """
    Apply section-specific color grading.
    Each section has distinct emotional color treatment.
    """

    if section == "INTRO":
        # Cold, isolated, crushed blacks
        result = apply_cinematic_bw(frame, contrast=1.25, lift=-0.08)
        result = add_vignette(result, intensity=0.40, softness=0.7)
        result = add_dynamic_grain(result, intensity=0.12)

    elif section == "BUILD":
        # Increased contrast, fragmented
        result = apply_cinematic_bw(frame, contrast=1.35, lift=-0.05)
        result = add_vignette(result, intensity=0.30, softness=0.75)
        result = add_dynamic_grain(result, intensity=0.18)
        result = add_chromatic_aberration(result, intensity=0.002)

    elif section == "PRE_DROP":
        # Dreamlike, suspended, soft
        result = apply_cinematic_bw(frame, contrast=1.15, lift=0.0)
        result = add_vignette(result, intensity=0.20, softness=0.85)
        result = add_dynamic_grain(result, intensity=0.10)

    elif section == "DROP":
        # MAXIMUM INTENSITY - Green eyes active
        result = isolate_green_eyes(frame, saturation_boost=0.8 + green_boost, luminance_boost=0.15 + green_boost*0.1)
        result = add_vignette(result, intensity=0.45, softness=0.65)
        result = add_dynamic_grain(result, intensity=0.25)
        result = add_chromatic_aberration(result, intensity=0.004)
        result = add_halation(result, threshold=0.70, intensity=0.25)

    elif section == "CLIMAX":
        # Peak intensity, held gaze
        result = isolate_green_eyes(frame, saturation_boost=1.0, luminance_boost=0.22)
        result = add_vignette(result, intensity=0.50, softness=0.60)
        result = add_dynamic_grain(result, intensity=0.15)  # Reduced for clarity
        result = add_halation(result, threshold=0.65, intensity=0.30)

    elif section == "PEAK":
        # High energy, interweaving
        result = isolate_green_eyes(frame, saturation_boost=0.6 + green_boost*0.3, luminance_boost=0.10)
        result = add_vignette(result, intensity=0.35, softness=0.70)
        result = add_dynamic_grain(result, intensity=0.20)
        result = add_chromatic_aberration(result, intensity=0.003)

    elif section == "OUTRO":
        # Fading, acceptance, minimal
        fade = 1.0 - (time_in_section / 3.0)  # Fade over 3 seconds
        result = apply_cinematic_bw(frame, contrast=1.10 + 0.1*fade, lift=0.02)
        result = add_vignette(result, intensity=0.25 * fade, softness=0.80)
        result = add_dynamic_grain(result, intensity=0.08 * fade)

    else:
        result = apply_cinematic_bw(frame, contrast=1.30)
        result = add_vignette(result, intensity=0.30)
        result = add_dynamic_grain(result, intensity=0.15)

    return result

# ============================================================
# TYPOGRAPHY SYSTEM
# ============================================================

def create_title_card(duration=0.7, fade_in=0.3):
    """
    Create the final title card:
    ◉ СМОТРЕЛА
      look at me
                    С А Й М У Р Р
    """
    def make_frame(t):
        # Create black background
        img = Image.new('RGB', (OUTPUT_WIDTH, OUTPUT_HEIGHT), (12, 12, 12))
        draw = ImageDraw.Draw(img)

        # Calculate fade
        if t < fade_in:
            alpha = t / fade_in
        else:
            alpha = 1.0

        # Colors with alpha
        white = (int(252*alpha), int(252*alpha), int(250*alpha))
        gray = (int(180*alpha*0.55), int(180*alpha*0.55), int(182*alpha*0.55))
        green = (int(48*alpha), int(168*alpha), int(107*alpha))

        # Try to load fonts, fallback to default
        try:
            # Main title font (large, bold)
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 88)
            # Subtitle font (smaller, light)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
            # Artist font
            artist_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
            artist_small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            artist_font = ImageFont.load_default()
            artist_small_font = ImageFont.load_default()

        # Draw green iris circle
        iris_x, iris_y = OUTPUT_WIDTH // 2 - 250, OUTPUT_HEIGHT // 2 - 20
        iris_radius = 8
        draw.ellipse([iris_x - iris_radius, iris_y - iris_radius,
                      iris_x + iris_radius, iris_y + iris_radius], fill=green)

        # Draw main title: СМОТРЕЛА
        title_text = "СМОТРЕЛА"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (OUTPUT_WIDTH - title_width) // 2 + 20
        title_y = OUTPUT_HEIGHT // 2 - 40
        draw.text((title_x, title_y), title_text, fill=white, font=title_font)

        # Draw subtitle: look at me
        subtitle_text = "look at me"
        sub_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        sub_width = sub_bbox[2] - sub_bbox[0]
        sub_x = (OUTPUT_WIDTH - sub_width) // 2 + 20
        sub_y = title_y + 100
        draw.text((sub_x, sub_y), subtitle_text, fill=gray, font=subtitle_font)

        # Draw artist name bottom right
        artist_text = "С А Й М У Р Р"
        artist_bbox = draw.textbbox((0, 0), artist_text, font=artist_font)
        artist_x = OUTPUT_WIDTH - artist_bbox[2] - 80
        artist_y = OUTPUT_HEIGHT - 120
        # First letter in green
        draw.text((artist_x, artist_y), "С", fill=green, font=artist_font)
        # Rest in white
        rest_bbox = draw.textbbox((0, 0), "С ", font=artist_font)
        draw.text((artist_x + rest_bbox[2], artist_y), "А Й М У Р Р", fill=white, font=artist_font)

        # Latin transliteration
        latin_text = "saymurr"
        latin_bbox = draw.textbbox((0, 0), latin_text, font=artist_small_font)
        draw.text((artist_x, artist_y + 45), latin_text, fill=gray, font=artist_small_font)

        # Add subtle grain
        frame = np.array(img)
        frame = add_dynamic_grain(frame, intensity=0.12)

        return frame

    return VideoClip(make_frame, duration=duration)

# ============================================================
# NARRATIVE-DRIVEN EDL (Edit Decision List)
# ============================================================

# Each cut has: source, start, end, timeline_start, purpose, section, special_effect
EDL = [
    # ============ INTRO: "THE ABSENCE" (0-4.32s) ============
    # Slow, breathing rhythm - every 2-4 beats
    {"src": "black", "dur": 0.35, "purpose": "Void before existence", "section": "INTRO"},
    {"src": "V4", "in": 2.0, "dur": 1.40, "purpose": "Empty chair - the absence", "section": "INTRO"},
    {"src": "V2", "in": 3.5, "dur": 1.20, "purpose": "Hands on piano - ritual", "section": "INTRO"},
    {"src": "V3", "in": 1.0, "dur": 1.37, "purpose": "Silhouette - ghost of presence", "section": "INTRO"},

    # ============ BUILD-UP: "THE SEARCH" (4.32-10s) ============
    # Accelerating rhythm - every 2 beats → every beat
    {"src": "V1", "in": 2.0, "dur": 0.70, "purpose": "Crowd - searching faces", "section": "BUILD"},
    {"src": "V3", "in": 4.0, "dur": 0.71, "purpose": "Profile - is it her?", "section": "BUILD"},
    {"src": "V1", "in": 5.0, "dur": 0.70, "purpose": "More faces - no", "section": "BUILD"},
    {"src": "V4", "in": 5.0, "dur": 0.70, "purpose": "Chair again - anchor", "section": "BUILD"},
    {"src": "V2", "in": 6.0, "dur": 0.71, "purpose": "Hands accelerate", "section": "BUILD"},
    {"src": "V1", "in": 7.0, "dur": 0.70, "purpose": "Crowd blur", "section": "BUILD"},
    {"src": "V3", "in": 6.0, "dur": 0.70, "purpose": "Profile turns", "section": "BUILD"},
    {"src": "V5", "in": 3.0, "dur": 0.70, "purpose": "Wide shot - isolation", "section": "BUILD"},

    # ============ PRE-DROP: "THE RECOGNITION BUILDS" (10-17.16s) ============
    # Elongating - every 2-4 beats, slow motion feel
    {"src": "V4", "in": 7.0, "dur": 1.76, "purpose": "Chair - altar", "section": "PRE_DROP"},
    {"src": "V3", "in": 8.0, "dur": 1.41, "purpose": "Profile - recognition near", "section": "PRE_DROP"},
    {"src": "V6", "in": 2.0, "dur": 1.41, "purpose": "Eye close-up - almost", "section": "PRE_DROP"},
    {"src": "V4", "in": 9.0, "dur": 1.41, "purpose": "Chair fills frame", "section": "PRE_DROP"},
    {"src": "black", "dur": 0.66, "purpose": "THE BREATH BEFORE - pure void", "section": "PRE_DROP"},

    # ============ DROP: "THE EPIPHANY" (17.16s) ============
    # EXPLOSION - rapid cuts, flash, green eyes reveal
    {"src": "flash", "dur": 0.10, "purpose": "WHITE FLASH - impact", "section": "DROP"},
    {"src": "V6", "in": 5.0, "dur": 0.35, "purpose": "GREEN EYES - THERE!", "section": "DROP", "fx": "drop_reveal"},
    {"src": "V1", "in": 8.0, "dur": 0.35, "purpose": "Crowd flash", "section": "DROP"},
    {"src": "V6", "in": 6.0, "dur": 0.35, "purpose": "Eyes again", "section": "DROP"},
    {"src": "V3", "in": 10.0, "dur": 0.35, "purpose": "Profile sharp", "section": "DROP"},
    {"src": "V6", "in": 7.0, "dur": 0.70, "purpose": "Eyes hold", "section": "DROP"},
    {"src": "V2", "in": 8.0, "dur": 0.35, "purpose": "Hands intensity", "section": "DROP"},
    {"src": "flash", "dur": 0.07, "purpose": "Flash beat", "section": "DROP"},
    {"src": "V6", "in": 8.0, "dur": 0.70, "purpose": "Eyes - connection", "section": "DROP"},

    # ============ CLIMAX: "THE PROLONGED GAZE" (21.45-22.88s) ============
    # THE SOUL OF THE PIECE - 1.43 second hold
    {"src": "V6", "in": 9.0, "dur": 1.43, "purpose": "THE GAZE HOLDS - eternity", "section": "CLIMAX", "fx": "slow_zoom"},

    # ============ PEAK: "THE INTERWEAVING" (22.88-34s) ============
    # Rapid cuts, memory fragments, decelerating
    {"src": "V3", "in": 11.0, "dur": 0.52, "purpose": "Fragment 1", "section": "PEAK"},
    {"src": "V6", "in": 10.0, "dur": 0.52, "purpose": "Eyes flash", "section": "PEAK"},
    {"src": "V1", "in": 9.0, "dur": 0.52, "purpose": "Crowd memory", "section": "PEAK"},
    {"src": "V4", "in": 10.0, "dur": 0.70, "purpose": "Chair - anchor", "section": "PEAK"},
    {"src": "V6", "in": 11.0, "dur": 0.52, "purpose": "Eyes", "section": "PEAK"},
    {"src": "V2", "in": 10.0, "dur": 0.70, "purpose": "Hands continue", "section": "PEAK"},
    {"src": "V3", "in": 12.0, "dur": 0.70, "purpose": "Profile", "section": "PEAK"},
    {"src": "V6", "in": 12.0, "dur": 0.88, "purpose": "Eyes longer", "section": "PEAK"},
    {"src": "V1", "in": 10.0, "dur": 0.70, "purpose": "Crowd fading", "section": "PEAK"},
    {"src": "V4", "in": 11.0, "dur": 1.05, "purpose": "Chair longer", "section": "PEAK"},
    {"src": "V6", "in": 13.0, "dur": 1.05, "purpose": "Eyes softening", "section": "PEAK"},
    {"src": "V2", "in": 11.0, "dur": 1.05, "purpose": "Hands slowing", "section": "PEAK"},
    {"src": "V3", "in": 13.0, "dur": 1.23, "purpose": "Profile peace", "section": "PEAK"},

    # ============ OUTRO: "THE RETURN" (34-37s) ============
    # Dissolution, acceptance, title card
    {"src": "V4", "in": 12.0, "dur": 1.20, "purpose": "Chair - full circle", "section": "OUTRO"},
    {"src": "V6", "in": 14.0, "dur": 1.10, "purpose": "Eyes fading", "section": "OUTRO", "fx": "fade_out"},
    {"src": "title", "dur": 0.70, "purpose": "◉ СМОТРЕЛА - title card", "section": "OUTRO"},
]

# ============================================================
# MAIN RENDER FUNCTION
# ============================================================

def render_teaser():
    print("=" * 60)
    print("СМОТРЕЛА — TEASER RENDERER V2")
    print("Ultra-Professional Cinematic Version")
    print("=" * 60)
    print(f"BPM: {BPM}")
    print(f"Beat interval: {BEAT_INTERVAL:.3f}s")
    print(f"Total duration: {TOTAL_DURATION}s")
    print(f"Key moments: DROP @ {DROP_TIME}s, CLIMAX @ {CLIMAX_TIME}s")
    print()

    # Load video sources
    print("[1/5] Loading video sources...")
    sources = {}
    for name, path in VIDEOS.items():
        try:
            clip = VideoFileClip(path)
            # Resize to output resolution
            clip = clip.resized((OUTPUT_WIDTH, OUTPUT_HEIGHT))
            sources[name] = clip
            print(f"      {name}: {clip.duration:.2f}s")
        except Exception as e:
            print(f"      ERROR loading {name}: {e}")

    # Build clips from EDL
    print(f"\n[2/5] Building {len(EDL)} clips from narrative EDL...")
    clips = []
    timeline_pos = 0.0

    for i, cut in enumerate(EDL):
        src = cut["src"]
        dur = cut["dur"]
        section = cut["section"]
        purpose = cut["purpose"]

        print(f"      [{i+1:02d}/{len(EDL)}] {section}: {purpose[:40]}...")

        try:
            if src == "black":
                # Pure black frame with subtle grain
                def make_black_frame(t):
                    frame = np.ones((OUTPUT_HEIGHT, OUTPUT_WIDTH, 3), dtype=np.uint8) * 12
                    return add_dynamic_grain(frame, intensity=0.05)
                clip = VideoClip(make_black_frame, duration=dur)

            elif src == "flash":
                # White flash
                def make_flash_frame(t):
                    return np.ones((OUTPUT_HEIGHT, OUTPUT_WIDTH, 3), dtype=np.uint8) * 255
                clip = VideoClip(make_flash_frame, duration=dur)

            elif src == "title":
                # Title card
                clip = create_title_card(duration=dur)

            else:
                # Video source
                source_clip = sources[src]
                in_point = cut.get("in", 0)

                # Handle if in_point + dur exceeds source duration
                if in_point + dur > source_clip.duration:
                    in_point = max(0, source_clip.duration - dur - 0.1)

                clip = source_clip.subclipped(in_point, in_point + dur)

                # Apply section-specific grading using fl_image
                sec = section  # Capture for closure

                def make_grading_filter(sec_name):
                    def grading_filter(frame):
                        # Simple grading without time-dependent effects for now
                        green_boost = 0.0
                        if sec_name == "DROP":
                            green_boost = 0.15  # Constant boost in DROP

                        result = apply_section_grade(frame, sec_name, 0, green_boost)
                        return result
                    return grading_filter

                clip = clip.image_transform(make_grading_filter(section))

            clips.append(clip)
            timeline_pos += dur

        except Exception as e:
            print(f"      WARNING: Error processing cut {i+1}: {e}")
            # Add black frame as fallback
            clip = ColorClip(size=(OUTPUT_WIDTH, OUTPUT_HEIGHT), color=(12, 12, 12), duration=dur)
            clips.append(clip)
            timeline_pos += dur

    # Concatenate all clips
    print(f"\n[3/5] Concatenating {len(clips)} clips...")
    final_video = concatenate_videoclips(clips, method="compose")
    print(f"      Video duration: {final_video.duration:.2f}s")

    # Trim to exact duration if needed
    if final_video.duration > TOTAL_DURATION:
        final_video = final_video.subclipped(0, TOTAL_DURATION)

    # Add letterboxing for cinematic 2.39:1 aspect ratio
    print("\n[4/5] Adding letterboxing (2.39:1 cinematic ratio)...")
    letterbox_height = int(OUTPUT_HEIGHT * 0.13)  # ~140px bars

    def add_letterbox(frame):
        frame = frame.copy()
        # Add black bars
        frame[:letterbox_height, :] = [12, 12, 12]
        frame[-letterbox_height:, :] = [12, 12, 12]
        return frame

    final_video = final_video.image_transform(add_letterbox)

    # Add audio
    print("\n[5/5] Adding audio and rendering...")
    audio = AudioFileClip(AUDIO_FILE).subclipped(0, TOTAL_DURATION)
    final_video = final_video.with_audio(audio)

    # Render
    print(f"\n      Rendering to: {OUTPUT_FILE}")
    print(f"      Resolution: {OUTPUT_WIDTH}x{OUTPUT_HEIGHT} @ {FPS}fps")
    print(f"      This will take several minutes...\n")

    final_video.write_videofile(
        OUTPUT_FILE,
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        bitrate='12000k',  # Higher bitrate for quality
        preset='medium',
        threads=4,
    )

    # Cleanup
    for clip in sources.values():
        clip.close()
    final_video.close()

    print("\n" + "=" * 60)
    print("RENDER COMPLETE!")
    print(f"Output: {OUTPUT_FILE}")
    print("=" * 60)
    print("\n◉ СМОТРЕЛА — she was looking")
    print("   Past tense. Present continuous. Future eternal.")
    print()

if __name__ == "__main__":
    render_teaser()
