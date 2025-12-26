#!/usr/bin/env python3
"""
СМОТРЕЛА — TEASER RENDERER V3 BRANDED
Ultra-Professional with Artist Branding

НОВОЕ В V3:
- Двойная экспозиция имени артиста (INTRO + OUTRO)
- Символ ◉ (зеленый глаз) как визуальная метка
- Правильная иерархия: САЙМУРР > СМОТРЕЛА
- Широкий tracking для современного вида
- Пульсация зеленой "С" в такт музыке

Artist: Саймурр (ГЛАВНОЕ ИМЯ!)
Track: СМОТРЕЛА / look at me
Genre: Electronic
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
OUTPUT_FILE = os.path.join(BASE_DIR, "SMOTRELA_teaser_v3_BRANDED.mp4")

# Video sources
VIDEOS = {
    "V1": os.path.join(BASE_DIR, "20251226_0026_01kdbpca1rfxjtx3zddgv48gjh.mp4"),
    "V2": os.path.join(BASE_DIR, "20251226_0130_01kdbr9ggwft8sr8k143r5xfs0.mp4"),
    "V3": os.path.join(BASE_DIR, "20251226_0130_01kdbrazryf8wtabs5kk6kvmqx.mp4"),
    "V4": os.path.join(BASE_DIR, "20251226_0130_01kdbsc29wehvbem5ertshqfed.mp4"),
    "V5": os.path.join(BASE_DIR, "20251226_0131_01kdbsdwn8epg9amf3qtp17qsb.mp4"),
    "V6": os.path.join(BASE_DIR, "20251226_0131_01kdbspmg9egv833wj0ngh944a.mp4"),
}

# Timing constants
BPM = 170.5
BEAT_INTERVAL = 60.0 / BPM
TOTAL_DURATION = 37.0
FPS = 30

# Key moments
DROP_TIME = 17.163
CLIMAX_TIME = 21.451
CLIMAX_END = 22.880

# Output specs
OUTPUT_WIDTH = 1920
OUTPUT_HEIGHT = 1080

# Brand colors
COLOR_BACKGROUND = (12, 12, 12)
COLOR_TEXT_PRIMARY = (252, 252, 250)
COLOR_TEXT_SECONDARY = (139, 139, 142)
COLOR_ACCENT_GREEN = (48, 168, 107)

# ============================================================
# VFX FUNCTIONS (from v2)
# ============================================================

def apply_cinematic_bw(frame, contrast=1.4, lift=-0.05):
    """Hollywood-grade B&W conversion"""
    img = frame.astype(np.float32) / 255.0
    gray = img[:,:,0] * 0.30 + img[:,:,1] * 0.59 + img[:,:,2] * 0.11
    gray = gray + lift
    gray = 0.5 + (gray - 0.5) * contrast
    gray = np.clip(gray, 0, 1)
    result = np.stack([gray, gray, gray], axis=2)
    return (result * 255).astype(np.uint8)

def isolate_green_eyes(frame, saturation_boost=1.0, luminance_boost=0.0):
    """Selective color isolation for green eyes"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)
    hue = hsv[:,:,0]
    sat = hsv[:,:,1]
    green_mask = ((hue >= 35) & (hue <= 85) & (sat > 50)).astype(np.float32)
    green_mask = cv2.GaussianBlur(green_mask, (5, 5), 0)
    bw = apply_cinematic_bw(frame, contrast=1.35)
    hsv[:,:,1] = np.clip(hsv[:,:,1] * (1 + saturation_boost * green_mask), 0, 255)
    hsv[:,:,2] = np.clip(hsv[:,:,2] * (1 + luminance_boost * green_mask), 0, 255)
    colored = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    green_mask_3d = np.stack([green_mask] * 3, axis=2)
    result = bw * (1 - green_mask_3d) + colored * green_mask_3d
    return result.astype(np.uint8)

def add_dynamic_grain(frame, intensity=0.15, size=1.0):
    """Film grain simulation"""
    h, w = frame.shape[:2]
    grain_h, grain_w = int(h / size), int(w / size)
    grain = np.random.normal(0, intensity * 255, (grain_h, grain_w))
    grain = cv2.resize(grain, (w, h), interpolation=cv2.INTER_LINEAR)
    grain_3d = np.stack([grain] * 3, axis=2)
    result = frame.astype(np.float32) + grain_3d
    result = np.clip(result, 0, 255)
    return result.astype(np.uint8)

def add_vignette(frame, intensity=0.35, softness=0.8):
    """Cinematic vignette"""
    h, w = frame.shape[:2]
    y, x = np.ogrid[:h, :w]
    center_y, center_x = h / 2, w / 2
    dist = np.sqrt(((x - center_x) / (w/2)) ** 2 + ((y - center_y) / (h/2)) ** 2)
    vignette = 1 - np.clip((dist - (1 - softness)) / softness, 0, 1) * intensity
    vignette = np.power(vignette, 1.5)
    vignette_3d = np.stack([vignette] * 3, axis=2)
    result = frame.astype(np.float32) * vignette_3d
    return np.clip(result, 0, 255).astype(np.uint8)

def add_chromatic_aberration(frame, intensity=0.003):
    """RGB channel separation"""
    h, w = frame.shape[:2]
    r, g, b = frame[:,:,0], frame[:,:,1], frame[:,:,2]
    shift = int(w * intensity)
    if shift < 1:
        return frame
    r_shifted = np.roll(r, -shift, axis=1)
    b_shifted = np.roll(b, shift, axis=1)
    result = np.stack([r_shifted, g, b_shifted], axis=2)
    return result

def add_halation(frame, threshold=0.75, intensity=0.2, radius=30):
    """Bloom on bright areas"""
    img = frame.astype(np.float32) / 255.0
    luminance = img[:,:,0] * 0.3 + img[:,:,1] * 0.59 + img[:,:,2] * 0.11
    bright_mask = (luminance > threshold).astype(np.float32)
    bright_areas = img * np.stack([bright_mask] * 3, axis=2)
    bloom = cv2.GaussianBlur(bright_areas, (radius*2+1, radius*2+1), radius/2)
    result = img + bloom * intensity
    result = np.clip(result, 0, 1)
    return (result * 255).astype(np.uint8)

def apply_section_grade(frame, section, time_in_section, green_boost=0.0):
    """Section-specific color grading"""
    if section == "INTRO":
        result = apply_cinematic_bw(frame, contrast=1.25, lift=-0.08)
        result = add_vignette(result, intensity=0.40, softness=0.7)
        result = add_dynamic_grain(result, intensity=0.12)
    elif section == "BUILD":
        result = apply_cinematic_bw(frame, contrast=1.35, lift=-0.05)
        result = add_vignette(result, intensity=0.30, softness=0.75)
        result = add_dynamic_grain(result, intensity=0.18)
        result = add_chromatic_aberration(result, intensity=0.002)
    elif section == "PRE_DROP":
        result = apply_cinematic_bw(frame, contrast=1.15, lift=0.0)
        result = add_vignette(result, intensity=0.20, softness=0.85)
        result = add_dynamic_grain(result, intensity=0.10)
    elif section == "DROP":
        result = isolate_green_eyes(frame, saturation_boost=0.8 + green_boost, luminance_boost=0.15 + green_boost*0.1)
        result = add_vignette(result, intensity=0.45, softness=0.65)
        result = add_dynamic_grain(result, intensity=0.25)
        result = add_chromatic_aberration(result, intensity=0.004)
        result = add_halation(result, threshold=0.70, intensity=0.25)
    elif section == "CLIMAX":
        result = isolate_green_eyes(frame, saturation_boost=1.0, luminance_boost=0.22)
        result = add_vignette(result, intensity=0.50, softness=0.60)
        result = add_dynamic_grain(result, intensity=0.15)
        result = add_halation(result, threshold=0.65, intensity=0.30)
    elif section == "PEAK":
        result = isolate_green_eyes(frame, saturation_boost=0.6 + green_boost*0.3, luminance_boost=0.10)
        result = add_vignette(result, intensity=0.35, softness=0.70)
        result = add_dynamic_grain(result, intensity=0.20)
        result = add_chromatic_aberration(result, intensity=0.003)
    elif section == "OUTRO":
        fade = 1.0 - (time_in_section / 3.0)
        result = apply_cinematic_bw(frame, contrast=1.10 + 0.1*fade, lift=0.02)
        result = add_vignette(result, intensity=0.25 * fade, softness=0.80)
        result = add_dynamic_grain(result, intensity=0.08 * fade)
    else:
        result = apply_cinematic_bw(frame, contrast=1.30)
        result = add_vignette(result, intensity=0.30)
        result = add_dynamic_grain(result, intensity=0.15)
    return result

# ============================================================
# NEW BRANDING SYSTEM
# ============================================================

def create_intro_card_saymurr(duration=3.5):
    """
    INTRO CARD: Брендинг артиста
    0.5-4.0s

    Структура:
    - 0.0-0.5s: Pure black
    - 0.5-1.5s: Символ ◉ fade in + blink
    - 1.5-2.0s: САЙМУРР fade in
    - 2.0-3.5s: Hold
    - 3.5-4.0s: Fade out
    """
    def make_frame(t):
        img = Image.new('RGB', (OUTPUT_WIDTH, OUTPUT_HEIGHT), COLOR_BACKGROUND)
        draw = ImageDraw.Draw(img)

        # Phase 1: Pure black (0-0.5s)
        if t < 0.5:
            frame = np.array(img)
            return add_dynamic_grain(frame, intensity=0.05)

        # Phase 2: Eye symbol ◉ (0.5-1.5s)
        if t < 1.5:
            progress = (t - 0.5) / 1.0
            alpha = min(1.0, progress * 1.5)

            # Blink animation
            if 0.6 < progress < 0.7:
                scale = 1.0 + (progress - 0.6) * 1.5
            elif 0.7 < progress < 0.8:
                scale = 1.15 - (progress - 0.7) * 1.5
            elif 0.9 < progress < 0.95:
                scale = 1.0 + (progress - 0.9) * 2.4
            elif 0.95 < progress:
                scale = 1.12 - (progress - 0.95) * 2.4
            else:
                scale = 1.0

            # Draw eye
            eye_color = (int(COLOR_ACCENT_GREEN[0]*alpha),
                        int(COLOR_ACCENT_GREEN[1]*alpha),
                        int(COLOR_ACCENT_GREEN[2]*alpha))
            eye_x, eye_y = OUTPUT_WIDTH // 2, OUTPUT_HEIGHT // 2 - 50
            eye_radius = int(14 * scale)

            # Outer circle (iris)
            draw.ellipse([eye_x - eye_radius, eye_y - eye_radius,
                         eye_x + eye_radius, eye_y + eye_radius],
                        fill=eye_color)

            # Inner circle (pupil)
            pupil_radius = int(6 * scale)
            draw.ellipse([eye_x - pupil_radius, eye_y - pupil_radius,
                         eye_x + pupil_radius, eye_y + pupil_radius],
                        fill=COLOR_BACKGROUND)

            frame = np.array(img)
            return add_dynamic_grain(frame, intensity=0.08)

        # Phase 3: Text САЙМУРР (1.5-4.0s)
        if t < 2.0:
            # Fade in
            progress = (t - 1.5) / 0.5
            alpha = min(1.0, progress)
            y_offset = int(20 * (1 - alpha))
        elif t < 3.5:
            # Hold
            alpha = 1.0
            y_offset = 0
        else:
            # Fade out
            fade_progress = (t - 3.5) / 0.5
            alpha = 1.0 - fade_progress
            y_offset = 0

        # Load fonts
        try:
            main_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 140
            )
            small_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20
            )
        except:
            main_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        # Colors with alpha
        green = (int(COLOR_ACCENT_GREEN[0]*alpha),
                int(COLOR_ACCENT_GREEN[1]*alpha),
                int(COLOR_ACCENT_GREEN[2]*alpha))
        white = (int(COLOR_TEXT_PRIMARY[0]*alpha),
                int(COLOR_TEXT_PRIMARY[1]*alpha),
                int(COLOR_TEXT_PRIMARY[2]*alpha))
        gray = (int(COLOR_TEXT_SECONDARY[0]*alpha),
               int(COLOR_TEXT_SECONDARY[1]*alpha),
               int(COLOR_TEXT_SECONDARY[2]*alpha))

        # Calculate positions
        text_y = OUTPUT_HEIGHT // 2 - 20 + y_offset

        # Pulse on beats (only during hold phase)
        pulse_intensity = 0
        if 2.0 < t < 3.5:
            # Beats at ~2.933s, ~3.637s
            beat_times = [2.933, 3.637]
            for beat_t in beat_times:
                if abs(t - beat_t) < 0.15:
                    pulse_progress = abs(t - beat_t) / 0.15
                    pulse_intensity = (1 - pulse_progress) * 0.5

        # Draw "С" (first letter) in green with potential glow
        c_x = 620

        # Add glow if pulsing
        if pulse_intensity > 0:
            # Simple glow simulation with multiple circles
            for i in range(3):
                glow_radius = 30 + i * 15
                glow_alpha = int(pulse_intensity * 80 * (1 - i * 0.3))
                glow_color = (green[0], green[1], green[2], glow_alpha)
                # PIL doesn't easily support RGBA, so skip complex glow
                # Would need PIL RGBA mode or composite

        draw.text((c_x, text_y), "С", fill=green, font=main_font)

        # Rest of letters with wide tracking
        letters = " А Й М У Р Р"
        letter_spacing = 54  # Wide tracking (+120)
        x = c_x + 95

        for letter in letters:
            if letter.strip():
                draw.text((x, text_y), letter, fill=white, font=main_font)
            x += letter_spacing

        # Transliteration
        translit = "s a y m u r r"
        translit_bbox = draw.textbbox((0, 0), translit, font=small_font)
        translit_width = translit_bbox[2] - translit_bbox[0]
        translit_x = (OUTPUT_WIDTH - translit_width) // 2
        draw.text((translit_x, text_y + 165), translit, fill=gray, font=small_font)

        frame = np.array(img)
        frame = add_dynamic_grain(frame, intensity=0.12)

        return frame

    return VideoClip(make_frame, duration=duration)


def create_outro_card_full(duration=1.5):
    """
    OUTRO CARD: Полная информация
    35.5-37.0s

    Иерархия:
    1. САЙМУРР (140px, bold, зеленая С)
    2. Линия-разделитель
    3. СМОТРЕЛА (88px, bold)
    4. look at me (26px, regular, 55% opacity)
    """
    def make_frame(t):
        img = Image.new('RGB', (OUTPUT_WIDTH, OUTPUT_HEIGHT), COLOR_BACKGROUND)
        draw = ImageDraw.Draw(img)

        # Cascading fade in
        if t < 0.3:
            # САЙМУРР fade in
            alpha_artist = t / 0.3
            alpha_track = 0
            alpha_subtitle = 0
        elif t < 0.6:
            # Add СМОТРЕЛА
            alpha_artist = 1.0
            alpha_track = (t - 0.3) / 0.3
            alpha_subtitle = 0
        elif t < 1.0:
            # Add look at me
            alpha_artist = 1.0
            alpha_track = 1.0
            alpha_subtitle = (t - 0.6) / 0.4
        else:
            # Hold with pulse
            alpha_artist = 1.0
            alpha_track = 1.0
            alpha_subtitle = 1.0

        # Load fonts
        try:
            artist_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 140
            )
            track_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 88
            )
            subtitle_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26
            )
            small_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18
            )
        except:
            artist_font = track_font = subtitle_font = small_font = ImageFont.load_default()

        # Colors
        green = (int(COLOR_ACCENT_GREEN[0]*alpha_artist),
                int(COLOR_ACCENT_GREEN[1]*alpha_artist),
                int(COLOR_ACCENT_GREEN[2]*alpha_artist))
        white_artist = (int(COLOR_TEXT_PRIMARY[0]*alpha_artist),
                       int(COLOR_TEXT_PRIMARY[1]*alpha_artist),
                       int(COLOR_TEXT_PRIMARY[2]*alpha_artist))
        white_track = (int(COLOR_TEXT_PRIMARY[0]*alpha_track),
                      int(COLOR_TEXT_PRIMARY[1]*alpha_track),
                      int(COLOR_TEXT_PRIMARY[2]*alpha_track))
        gray = (int(COLOR_TEXT_SECONDARY[0]*alpha_subtitle*0.55),
               int(COLOR_TEXT_SECONDARY[1]*alpha_subtitle*0.55),
               int(COLOR_TEXT_SECONDARY[2]*alpha_subtitle*0.55))

        base_y = 340

        # Pulse calculation (after 1.0s)
        pulse_intensity = 0
        if t > 1.0:
            # Approximate beats in this range
            time_since_hold = t - 1.0
            # Pulse every ~0.35s (beat interval)
            pulse_phase = (time_since_hold % BEAT_INTERVAL) / BEAT_INTERVAL
            if pulse_phase < 0.3:
                pulse_intensity = (1 - pulse_phase / 0.3) * 0.6

        # Artist name: САЙМУРР
        c_x = 560
        c_y = base_y

        # Draw "С" in green
        draw.text((c_x, c_y), "С", fill=green, font=artist_font)

        # Rest in white
        letters = " А Й М У Р Р"
        x = c_x + 95
        for letter in letters:
            if letter.strip():
                draw.text((x, c_y), letter, fill=white_artist, font=artist_font)
            x += 54

        # Transliteration
        translit = "s a y m u r r"
        translit_bbox = draw.textbbox((0, 0), translit, font=small_font)
        translit_x = (OUTPUT_WIDTH - translit_bbox[2]) // 2
        draw.text((translit_x, c_y + 160), translit,
                 fill=(int(COLOR_TEXT_SECONDARY[0]*alpha_artist*0.7),
                      int(COLOR_TEXT_SECONDARY[1]*alpha_artist*0.7),
                      int(COLOR_TEXT_SECONDARY[2]*alpha_artist*0.7)),
                 font=small_font)

        # Separator line
        if alpha_track > 0:
            line_y = base_y + 220
            line_x1 = 860
            line_x2 = 1060
            line_color = (int(COLOR_ACCENT_GREEN[0]*alpha_track*0.6),
                         int(COLOR_ACCENT_GREEN[1]*alpha_track*0.6),
                         int(COLOR_ACCENT_GREEN[2]*alpha_track*0.6))
            draw.line([line_x1, line_y, line_x2, line_y], fill=line_color, width=2)

        # Track name: СМОТРЕЛА
        if alpha_track > 0:
            track_text = "СМОТРЕЛА"
            track_bbox = draw.textbbox((0, 0), track_text, font=track_font)
            track_width = track_bbox[2] - track_bbox[0]
            track_x = (OUTPUT_WIDTH - track_width) // 2
            track_y = base_y + 250
            draw.text((track_x, track_y), track_text, fill=white_track, font=track_font)

        # Subtitle: look at me
        if alpha_subtitle > 0:
            sub_text = "look at me"
            sub_bbox = draw.textbbox((0, 0), sub_text, font=subtitle_font)
            sub_width = sub_bbox[2] - sub_bbox[0]
            sub_x = (OUTPUT_WIDTH - sub_width) // 2
            sub_y = base_y + 365
            draw.text((sub_x, sub_y), sub_text, fill=gray, font=subtitle_font)

        frame = np.array(img)
        frame = add_dynamic_grain(frame, intensity=0.12)

        return frame

    return VideoClip(make_frame, duration=duration)

# ============================================================
# EDL (Updated with branding cards)
# ============================================================

EDL = [
    # ============ INTRO CARD (0-4s) ============
    {"src": "intro_card", "dur": 4.0, "purpose": "САЙМУРР branding intro", "section": "INTRO"},

    # ============ BUILD-UP: "THE SEARCH" (4-10s) ============
    {"src": "V1", "in": 2.0, "dur": 0.70, "purpose": "Crowd - searching faces", "section": "BUILD"},
    {"src": "V3", "in": 4.0, "dur": 0.71, "purpose": "Profile - is it her?", "section": "BUILD"},
    {"src": "V1", "in": 5.0, "dur": 0.70, "purpose": "More faces - no", "section": "BUILD"},
    {"src": "V4", "in": 5.0, "dur": 0.70, "purpose": "Chair again - anchor", "section": "BUILD"},
    {"src": "V2", "in": 6.0, "dur": 0.71, "purpose": "Hands accelerate", "section": "BUILD"},
    {"src": "V1", "in": 7.0, "dur": 0.70, "purpose": "Crowd blur", "section": "BUILD"},
    {"src": "V3", "in": 6.0, "dur": 0.70, "purpose": "Profile turns", "section": "BUILD"},
    {"src": "V5", "in": 3.0, "dur": 0.70, "purpose": "Wide shot - isolation", "section": "BUILD"},

    # ============ PRE-DROP: "THE RECOGNITION BUILDS" (10-17.16s) ============
    {"src": "V4", "in": 7.0, "dur": 1.76, "purpose": "Chair - altar", "section": "PRE_DROP"},
    {"src": "V3", "in": 8.0, "dur": 1.41, "purpose": "Profile - recognition near", "section": "PRE_DROP"},
    {"src": "V6", "in": 2.0, "dur": 1.41, "purpose": "Eye close-up - almost", "section": "PRE_DROP"},
    {"src": "V4", "in": 9.0, "dur": 1.41, "purpose": "Chair fills frame", "section": "PRE_DROP"},
    {"src": "black", "dur": 0.66, "purpose": "THE BREATH BEFORE - pure void", "section": "PRE_DROP"},

    # ============ DROP: "THE EPIPHANY" (17.16s) ============
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
    {"src": "V6", "in": 9.0, "dur": 1.43, "purpose": "THE GAZE HOLDS - eternity", "section": "CLIMAX", "fx": "slow_zoom"},

    # ============ PEAK: "THE INTERWEAVING" (22.88-34s) ============
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
    {"src": "V4", "in": 12.0, "dur": 1.20, "purpose": "Chair - full circle", "section": "OUTRO"},
    {"src": "V6", "in": 14.0, "dur": 0.80, "purpose": "Eyes fading", "section": "OUTRO", "fx": "fade_out"},

    # ============ OUTRO CARD (35.5-37s) ============
    {"src": "outro_card", "dur": 1.5, "purpose": "Full title card САЙМУРР + СМОТРЕЛА", "section": "OUTRO"},
]

# ============================================================
# MAIN RENDER FUNCTION
# ============================================================

def render_teaser():
    print("=" * 60)
    print("СМОТРЕЛА — TEASER RENDERER V3 BRANDED")
    print("Artist: САЙМУРР (Saymurr)")
    print("=" * 60)
    print(f"BPM: {BPM}")
    print(f"Total duration: {TOTAL_DURATION}s")
    print()

    # Load video sources
    print("[1/5] Loading video sources...")
    sources = {}
    for name, path in VIDEOS.items():
        try:
            clip = VideoFileClip(path)
            clip = clip.resized((OUTPUT_WIDTH, OUTPUT_HEIGHT))
            sources[name] = clip
            print(f"      {name}: {clip.duration:.2f}s")
        except Exception as e:
            print(f"      ERROR loading {name}: {e}")

    # Build clips from EDL
    print(f"\n[2/5] Building {len(EDL)} clips from EDL...")
    clips = []
    timeline_pos = 0.0

    for i, cut in enumerate(EDL):
        src = cut["src"]
        dur = cut["dur"]
        section = cut.get("section", "")
        purpose = cut.get("purpose", "")

        print(f"      [{i+1:02d}/{len(EDL)}] {section}: {purpose[:50]}...")

        try:
            if src == "intro_card":
                # New intro card
                clip = create_intro_card_saymurr(duration=dur)

            elif src == "outro_card":
                # New outro card
                clip = create_outro_card_full(duration=dur)

            elif src == "black":
                def make_black_frame(t):
                    frame = np.ones((OUTPUT_HEIGHT, OUTPUT_WIDTH, 3), dtype=np.uint8) * 12
                    return add_dynamic_grain(frame, intensity=0.05)
                clip = VideoClip(make_black_frame, duration=dur)

            elif src == "flash":
                def make_flash_frame(t):
                    return np.ones((OUTPUT_HEIGHT, OUTPUT_WIDTH, 3), dtype=np.uint8) * 255
                clip = VideoClip(make_flash_frame, duration=dur)

            else:
                # Video source
                source_clip = sources[src]
                in_point = cut.get("in", 0)

                if in_point + dur > source_clip.duration:
                    in_point = max(0, source_clip.duration - dur - 0.1)

                clip = source_clip.subclipped(in_point, in_point + dur)

                # Apply grading
                sec = section
                def make_grading_filter(sec_name):
                    def grading_filter(frame):
                        green_boost = 0.15 if sec_name == "DROP" else 0.0
                        result = apply_section_grade(frame, sec_name, 0, green_boost)
                        return result
                    return grading_filter

                clip = clip.image_transform(make_grading_filter(section))

            clips.append(clip)
            timeline_pos += dur

        except Exception as e:
            print(f"      WARNING: Error processing cut {i+1}: {e}")
            clip = ColorClip(size=(OUTPUT_WIDTH, OUTPUT_HEIGHT), color=(12, 12, 12), duration=dur)
            clips.append(clip)
            timeline_pos += dur

    # Concatenate
    print(f"\n[3/5] Concatenating {len(clips)} clips...")
    final_video = concatenate_videoclips(clips, method="compose")
    print(f"      Video duration: {final_video.duration:.2f}s")

    # Trim if needed
    if final_video.duration > TOTAL_DURATION:
        final_video = final_video.subclipped(0, TOTAL_DURATION)

    # Letterboxing
    print("\n[4/5] Adding letterboxing (2.39:1)...")
    letterbox_height = int(OUTPUT_HEIGHT * 0.13)

    def add_letterbox(frame):
        frame = frame.copy()
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
        bitrate='15000k',  # High quality for text
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
    print("\n◉ С А Й М У Р Р — СМОТРЕЛА")
    print("   The artist name you'll remember")
    print()

if __name__ == "__main__":
    render_teaser()
