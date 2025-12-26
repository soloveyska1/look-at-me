#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ◉  С А Й М У Р Р  —  С М О Т Р Е Л А                                    ║
║                                                                              ║
║     ULTRA-PROFESSIONAL TEASER RENDERER V3                                    ║
║     "Вершина профессионализма"                                               ║
║                                                                              ║
║     Features:                                                                ║
║     • INTRO card (0-4s) with artist branding                                 ║
║     • Cinema-level B&W + selective green eye isolation                       ║
║     • Beat-synced pulsation @ 170.5 BPM                                      ║
║     • Film grain, chromatic aberration, halation                             ║
║     • OUTRO card (35-37s) with full branding                                 ║
║     • Frame-perfect sync at DROP (17.163s) and CLIMAX (21.451s)             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import numpy as np
from moviepy import (
    VideoFileClip, AudioFileClip, TextClip, ColorClip, CompositeVideoClip,
    concatenate_videoclips, VideoClip
)
from moviepy.video.fx import CrossFadeIn, CrossFadeOut
import cv2

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = "/home/user/look-at-me"

VIDEOS = {
    "V1": os.path.join(BASE_DIR, "20251226_0026_01kdbpca1rfxjtx3zddgv48gjh.mp4"),  # Crowd
    "V2": os.path.join(BASE_DIR, "20251226_0130_01kdbr9ggwft8sr8k143r5xfs0.mp4"),  # Piano
    "V3": os.path.join(BASE_DIR, "20251226_0130_01kdbrazryf8wtabs5kk6kvmqx.mp4"),  # Profile
    "V4": os.path.join(BASE_DIR, "20251226_0130_01kdbsc29wehvbem5ertshqfed.mp4"),  # Chair
    "V5": os.path.join(BASE_DIR, "20251226_0131_01kdbsdwn8epg9amf3qtp17qsb.mp4"),  # Silhouette
    "V6": os.path.join(BASE_DIR, "20251226_0131_01kdbspmg9egv833wj0ngh944a.mp4"),  # Eyes
}

AUDIO_FILE = os.path.join(BASE_DIR, "СМОТРЕЛА_teaser.wav")
OUTPUT_FILE = os.path.join(BASE_DIR, "SMOTRELA_teaser_v3_ULTIMATE.mp4")

# Audio parameters
BPM = 170.5
BEAT_INTERVAL = 60 / BPM  # 0.352s
TOTAL_DURATION = 37.0

# Critical sync points (frame-perfect)
DROP_TIME = 17.163      # Frame 515
CLIMAX_TIME = 21.451    # Frame 644
BLACK_START = 16.500    # Pre-drop silence
BLACK_END = 17.163      # DROP explosion

# Branding
ARTIST_NAME = "САЙМУРР"
TRACK_NAME = "СМОТРЕЛА"
SUBTITLE = "look at me"

# Colors
EMERALD_GREEN = (48, 168, 107)      # #30A86B - accent color
NEAR_BLACK = (12, 12, 12)           # #0C0C0C - background
OFF_WHITE = (252, 252, 250)         # #FCFCFA - text
GRAY = (139, 139, 142)              # #8B8B8E - secondary text

# =============================================================================
# VFX FUNCTIONS - CINEMA LEVEL
# =============================================================================

def get_beat_phase(t, bpm=170.5):
    """Get phase within current beat (0.0 to 1.0)"""
    beat_duration = 60.0 / bpm
    return (t % beat_duration) / beat_duration

def get_section(t):
    """Determine which section we're in"""
    if t < 4.0:
        return "INTRO"
    elif t < 4.32:
        return "INTRO_OUT"
    elif t < 10.016:
        return "BUILD"
    elif t < 16.5:
        return "PRE_DROP"
    elif t < 17.163:
        return "BLACK"
    elif t < 21.451:
        return "DROP"
    elif t < 22.88:
        return "CLIMAX"
    elif t < 34.293:
        return "PEAK"
    else:
        return "OUTRO"

def cinematic_bw_conversion(frame):
    """
    Cinema-level B&W conversion using channel mixer
    Based on Roger Deakins' approach: 30% R, 59% G, 11% B
    """
    if len(frame.shape) == 2:
        return frame

    r, g, b = frame[:,:,0], frame[:,:,1], frame[:,:,2]
    gray = (0.30 * r + 0.59 * g + 0.11 * b).astype(np.uint8)
    return np.stack([gray, gray, gray], axis=2)

def isolate_green_eyes(frame, t, intensity=1.0):
    """
    HSL-based green eye isolation with glow effect
    Keeps green (Hue 120-180°) while desaturating rest
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Green hue range (in OpenCV: 0-180 scale)
    # Target: 160° ± 20° = 140-180° → in OpenCV: 70-90
    lower_green = np.array([55, 60, 40])
    upper_green = np.array([95, 255, 255])

    # Create mask for green areas
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    # Expand mask slightly for glow
    kernel = np.ones((5, 5), np.uint8)
    green_mask_dilated = cv2.dilate(green_mask, kernel, iterations=2)

    # Create B&W version
    bw = cinematic_bw_conversion(frame)

    # Blend: keep green in color areas, B&W elsewhere
    mask_3ch = np.stack([green_mask_dilated/255.0]*3, axis=2)

    # Boost green saturation and luminance
    enhanced_frame = frame.copy().astype(np.float32)
    enhanced_frame[:,:,1] = np.clip(enhanced_frame[:,:,1] * 1.15, 0, 255)  # Boost green channel

    # Beat-synced pulsation
    beat_phase = get_beat_phase(t)
    pulse = 0.85 + 0.15 * np.sin(beat_phase * 2 * np.pi)

    # Apply intensity modulation
    mask_3ch = mask_3ch * intensity * pulse

    result = (bw * (1 - mask_3ch) + enhanced_frame * mask_3ch).astype(np.uint8)

    return result

def add_film_grain(frame, intensity=0.15, t=0):
    """Add organic film grain (Kodak Vision3 style)"""
    section = get_section(t)

    # Vary grain by section
    section_intensity = {
        "INTRO": 0.10,
        "BUILD": 0.14,
        "PRE_DROP": 0.12,
        "BLACK": 0.0,
        "DROP": 0.22,
        "CLIMAX": 0.18,
        "PEAK": 0.16,
        "OUTRO": 0.12
    }

    intensity = section_intensity.get(section, intensity)

    if intensity == 0:
        return frame

    # Generate grain
    noise = np.random.normal(0, intensity * 255, frame.shape).astype(np.float32)

    # Apply grain
    result = np.clip(frame.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    return result

def add_chromatic_aberration(frame, strength=0.003):
    """Add radial chromatic aberration"""
    h, w = frame.shape[:2]

    # Create displacement maps
    y, x = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
    cx, cy = w / 2, h / 2

    # Distance from center (normalized)
    dist = np.sqrt((x - cx)**2 + (y - cy)**2) / np.sqrt(cx**2 + cy**2)

    # Displacement amount (quadratic falloff)
    displacement = dist ** 2 * strength * w

    # Direction from center
    angle = np.arctan2(y - cy, x - cx)
    dx = displacement * np.cos(angle)
    dy = displacement * np.sin(angle)

    # Remap channels
    result = frame.copy()

    # Red channel - shift outward
    map_x_r = (x + dx).astype(np.float32)
    map_y_r = (y + dy).astype(np.float32)
    result[:,:,0] = cv2.remap(frame[:,:,0], map_x_r, map_y_r, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    # Blue channel - shift inward
    map_x_b = (x - dx).astype(np.float32)
    map_y_b = (y - dy).astype(np.float32)
    result[:,:,2] = cv2.remap(frame[:,:,2], map_x_b, map_y_b, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    return result

def add_vignette(frame, strength=0.4, t=0):
    """Add dynamic vignette with beat pulsation"""
    h, w = frame.shape[:2]

    # Beat-synced pulsation
    beat_phase = get_beat_phase(t)
    pulse_strength = strength + 0.05 * np.sin(beat_phase * 2 * np.pi)

    # Section-based adjustment
    section = get_section(t)
    section_mult = {
        "INTRO": 0.8,
        "BUILD": 1.0,
        "PRE_DROP": 1.1,
        "DROP": 1.3,
        "CLIMAX": 1.4,
        "PEAK": 1.1,
        "OUTRO": 1.2
    }
    pulse_strength *= section_mult.get(section, 1.0)

    # Create vignette mask
    y, x = np.meshgrid(np.linspace(-1, 1, h), np.linspace(-1, 1, w), indexing='ij')
    dist = np.sqrt(x**2 + y**2)

    # Smooth falloff
    vignette = 1 - np.clip(dist * pulse_strength, 0, 1) ** 1.5
    vignette = np.stack([vignette] * 3, axis=2)

    return (frame * vignette).astype(np.uint8)

def add_halation(frame, threshold=0.75, radius=25, strength=0.3):
    """Add halation/bloom effect on bright areas (especially green eyes)"""
    # Find bright areas
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    bright_mask = (gray > threshold * 255).astype(np.float32)

    # Also include green channel brightness for eye glow
    green_bright = (frame[:,:,1] > threshold * 255).astype(np.float32)
    bright_mask = np.maximum(bright_mask, green_bright)

    # Blur for glow
    bloom = cv2.GaussianBlur((frame * bright_mask[:,:,np.newaxis]).astype(np.float32),
                              (radius*2+1, radius*2+1), radius/2)

    # Add bloom to original
    result = np.clip(frame.astype(np.float32) + bloom * strength, 0, 255).astype(np.uint8)
    return result

def add_letterbox(frame, ratio=2.39):
    """Add cinematic letterboxing"""
    h, w = frame.shape[:2]
    target_h = int(w / ratio)

    if target_h >= h:
        return frame

    bar_height = (h - target_h) // 2

    result = frame.copy()
    result[:bar_height, :] = NEAR_BLACK
    result[h-bar_height:, :] = NEAR_BLACK

    return result

def apply_section_grade(frame, t):
    """Apply section-specific color grading"""
    section = get_section(t)

    # Convert to float for processing
    img = frame.astype(np.float32) / 255.0

    # Section-specific contrast curves
    contrast_map = {
        "INTRO": 1.25,
        "BUILD": 1.35,
        "PRE_DROP": 1.20,
        "BLACK": 1.0,
        "DROP": 1.50,
        "CLIMAX": 1.45,
        "PEAK": 1.30,
        "OUTRO": 1.15
    }

    contrast = contrast_map.get(section, 1.0)

    # Apply S-curve contrast
    img = 0.5 + (img - 0.5) * contrast
    img = np.clip(img, 0, 1)

    # Lift shadows slightly in intro/outro
    if section in ["INTRO", "OUTRO"]:
        img = img * 0.95 + 0.03

    return (img * 255).astype(np.uint8)

def create_white_flash(duration=0.1, size=(1920, 1080)):
    """Create white flash frame for impact moments"""
    def make_frame(t):
        # Fade from white to transparent
        alpha = 1.0 - (t / duration)
        val = int(255 * alpha)
        return np.full((size[1], size[0], 3), val, dtype=np.uint8)

    return VideoClip(make_frame, duration=duration)

# =============================================================================
# TITLE CARD CREATION
# =============================================================================

def create_intro_card(duration=4.0, size=(1920, 1080)):
    """
    Create intro card with:
    - Pulsating ◉ symbol
    - САЙМУРР with wide tracking
    - Green first letter "С"
    """
    w, h = size

    def make_frame(t):
        # Create black background
        frame = np.full((h, w, 3), NEAR_BLACK, dtype=np.uint8)

        # Phase calculations
        beat_phase = get_beat_phase(t)

        # Animation timeline
        # 0-0.5s: fade in from black
        # 0.5-1.5s: ◉ symbol appears and blinks
        # 1.5-3.5s: САЙМУРР fades in
        # 3.5-4.0s: fade out

        if t < 0.5:
            # Pure black, fade in
            alpha = t / 0.5
        elif t > 3.5:
            # Fade out
            alpha = 1.0 - (t - 3.5) / 0.5
        else:
            alpha = 1.0

        # Draw ◉ symbol (0.5s - 4.0s)
        if t >= 0.5:
            symbol_alpha = min(1.0, (t - 0.5) / 0.3) * alpha

            # Blink effect at specific times
            blink_times = [0.8, 1.2]
            for bt in blink_times:
                if abs(t - bt) < 0.05:
                    symbol_alpha *= 0.3

            # Pulsate on beats
            pulse = 0.85 + 0.15 * np.sin(beat_phase * 2 * np.pi)

            # Draw outer circle
            center = (w // 2, h // 2 - 80)
            radius = int(40 * pulse)
            color = tuple(int(c * symbol_alpha) for c in EMERALD_GREEN)
            cv2.circle(frame, center, radius, color[::-1], -1, cv2.LINE_AA)

            # Draw inner circle (pupil)
            inner_radius = int(15 * pulse)
            cv2.circle(frame, center, inner_radius, NEAR_BLACK[::-1], -1, cv2.LINE_AA)

        # Draw САЙМУРР (1.5s - 4.0s)
        if t >= 1.5:
            text_alpha = min(1.0, (t - 1.5) / 0.5) * alpha

            # Wide tracking: С А Й М У Р Р
            letters = list("САЙМУРР")
            total_width = len(letters) * 90  # Approximate letter spacing
            start_x = (w - total_width) // 2

            for i, letter in enumerate(letters):
                x = start_x + i * 90
                y = h // 2 + 60

                # First letter "С" is green
                if i == 0:
                    color = tuple(int(c * text_alpha) for c in EMERALD_GREEN)
                else:
                    color = tuple(int(c * text_alpha) for c in OFF_WHITE)

                # Pulsate first letter on beats
                if i == 0:
                    pulse = 0.9 + 0.1 * np.sin(beat_phase * 2 * np.pi)
                    color = tuple(int(c * pulse) for c in color)

                cv2.putText(frame, letter, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                           2.5, color[::-1], 4, cv2.LINE_AA)

            # Transliteration "saymurr" below
            if t >= 2.0:
                trans_alpha = min(1.0, (t - 2.0) / 0.3) * alpha
                trans_color = tuple(int(c * trans_alpha * 0.5) for c in GRAY)
                cv2.putText(frame, "s a y m u r r", (w//2 - 130, h//2 + 110),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, trans_color[::-1], 1, cv2.LINE_AA)

        return frame

    return VideoClip(make_frame, duration=duration)

def create_outro_card(duration=2.0, size=(1920, 1080)):
    """
    Create outro card with full branding:
    - САЙМУРР (large)
    - СМОТРЕЛА (medium)
    - look at me (small)
    """
    w, h = size

    def make_frame(t):
        frame = np.full((h, w, 3), NEAR_BLACK, dtype=np.uint8)

        beat_phase = get_beat_phase(t + 35.0)  # Continue from where we left off

        # Fade in
        if t < 0.3:
            alpha = t / 0.3
        else:
            alpha = 1.0

        # САЙМУРР - large
        if t >= 0.0:
            artist_alpha = min(1.0, t / 0.3) * alpha
            letters = list("САЙМУРР")
            total_width = len(letters) * 75
            start_x = (w - total_width) // 2

            for i, letter in enumerate(letters):
                x = start_x + i * 75
                y = h // 2 - 60

                if i == 0:
                    # Green С with glow effect
                    pulse = 0.9 + 0.1 * np.sin(beat_phase * 2 * np.pi)
                    color = tuple(int(c * artist_alpha * pulse) for c in EMERALD_GREEN)
                else:
                    color = tuple(int(c * artist_alpha) for c in OFF_WHITE)

                cv2.putText(frame, letter, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                           2.0, color[::-1], 3, cv2.LINE_AA)

        # Transliteration
        if t >= 0.2:
            trans_alpha = min(1.0, (t - 0.2) / 0.2) * alpha * 0.4
            trans_color = tuple(int(c * trans_alpha) for c in GRAY)
            cv2.putText(frame, "s a y m u r r", (w//2 - 105, h//2 - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, trans_color[::-1], 1, cv2.LINE_AA)

        # Green line separator
        if t >= 0.3:
            line_alpha = min(1.0, (t - 0.3) / 0.2) * alpha
            line_color = tuple(int(c * line_alpha) for c in EMERALD_GREEN)
            cv2.line(frame, (w//2 - 80, h//2 + 10), (w//2 + 80, h//2 + 10),
                    line_color[::-1], 2, cv2.LINE_AA)

        # СМОТРЕЛА - medium
        if t >= 0.4:
            track_alpha = min(1.0, (t - 0.4) / 0.3) * alpha
            track_color = tuple(int(c * track_alpha) for c in OFF_WHITE)
            cv2.putText(frame, "СМОТРЕЛА", (w//2 - 145, h//2 + 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, track_color[::-1], 2, cv2.LINE_AA)

        # "look at me" - small
        if t >= 0.6:
            sub_alpha = min(1.0, (t - 0.6) / 0.2) * alpha * 0.6
            sub_color = tuple(int(c * sub_alpha) for c in GRAY)
            cv2.putText(frame, "look at me", (w//2 - 75, h//2 + 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, sub_color[::-1], 1, cv2.LINE_AA)

        return frame

    return VideoClip(make_frame, duration=duration)

# =============================================================================
# NARRATIVE EDL - V3 ULTIMATE
# =============================================================================

# Ultimate EDL with frame-perfect sync
# Format: (start_time, duration, source, source_start, section, description)
ULTIMATE_EDL = [
    # ═══════════════════════════════════════════════════════════════════════════
    # ACT I: INTRO - "Entering the Memory" (0-4s) - TITLE CARD
    # ═══════════════════════════════════════════════════════════════════════════
    # Handled separately by intro card

    # ═══════════════════════════════════════════════════════════════════════════
    # ACT II: BUILD-UP - "The Search" (4-10s)
    # ═══════════════════════════════════════════════════════════════════════════
    (4.000, 0.70, "V4", 2.0, "BUILD", "Chair - portal appears"),
    (4.700, 0.55, "V2", 1.0, "BUILD", "Hands begin ritual"),
    (5.250, 0.60, "V1", 0.0, "BUILD", "Crowd - searching faces"),
    (5.850, 0.50, "V3", 1.0, "BUILD", "Profile glimpse"),
    (6.350, 0.45, "V1", 2.0, "BUILD", "More faces - not her"),
    (6.800, 0.55, "V6", 0.0, "BUILD", "First glimpse - GREEN EYES"),
    (7.350, 0.50, "V4", 4.0, "BUILD", "Chair - anchor"),
    (7.850, 0.45, "V2", 3.0, "BUILD", "Hands accelerate"),
    (8.300, 0.50, "V1", 4.0, "BUILD", "Crowd blur"),
    (8.800, 0.55, "V3", 3.0, "BUILD", "Profile turning"),
    (9.350, 0.66, "V5", 0.0, "BUILD", "Silhouette - ghost"),

    # ═══════════════════════════════════════════════════════════════════════════
    # ACT III: PRE-DROP - "Suspension" (10-17.163s)
    # ═══════════════════════════════════════════════════════════════════════════
    (10.016, 1.50, "V4", 6.0, "PRE_DROP", "Chair - slow motion, dreamlike"),
    (11.516, 1.20, "V3", 5.0, "PRE_DROP", "Profile - recognition near"),
    (12.716, 1.00, "V6", 2.0, "PRE_DROP", "Eyes - almost there"),
    (13.716, 1.10, "V2", 5.0, "PRE_DROP", "Hands - slow, deliberate"),
    (14.816, 0.90, "V6", 4.0, "PRE_DROP", "Eyes - direct contact"),
    (15.716, 0.78, "V4", 9.0, "PRE_DROP", "Chair fills frame"),

    # THE VOID - Maximum tension
    (16.500, 0.663, "BLACK", 0, "BLACK", "PURE DARKNESS - breath held"),

    # ═══════════════════════════════════════════════════════════════════════════
    # ACT IV: DROP - "Quantum Collapse" (17.163s)
    # ═══════════════════════════════════════════════════════════════════════════
    (17.163, 0.10, "FLASH", 0, "DROP", "WHITE EXPLOSION - impact!"),
    (17.263, 0.35, "V6", 5.0, "DROP", "GREEN EYES REVEALED!"),
    (17.613, 0.30, "V1", 6.0, "DROP", "Crowd flash - she's everywhere"),
    (17.913, 0.35, "V6", 6.0, "DROP", "Eyes again - confirmation"),
    (18.263, 0.30, "V3", 7.0, "DROP", "Profile sharp"),
    (18.563, 0.35, "V6", 7.0, "DROP", "Eyes HOLD - connection"),
    (18.913, 0.32, "V2", 7.0, "DROP", "Hands intensity"),
    (19.233, 0.30, "V4", 10.0, "DROP", "Chair - reality anchor"),
    (19.533, 0.35, "V6", 8.0, "DROP", "Eyes - obsession"),
    (19.883, 0.07, "FLASH", 0, "DROP", "SYNCOPATION BLAST"),
    (19.953, 0.35, "V3", 8.0, "DROP", "Profile - possessed"),
    (20.303, 0.40, "V6", 8.5, "DROP", "Eyes - deeper"),
    (20.703, 0.35, "V1", 8.0, "DROP", "Crowd - faces blur"),
    (21.053, 0.40, "V6", 9.0, "DROP", "Eyes building to climax"),

    # ═══════════════════════════════════════════════════════════════════════════
    # ACT V: CLIMAX - "The Gaze Holds" (21.451s) - LONGEST SHOT
    # ═══════════════════════════════════════════════════════════════════════════
    (21.451, 1.429, "V6", 9.5, "CLIMAX", "THE GAZE - time stops (LONGEST SHOT)"),

    # ═══════════════════════════════════════════════════════════════════════════
    # ACT VI: PEAK - "Interweaving" (22.88-34s)
    # ═══════════════════════════════════════════════════════════════════════════
    (22.880, 0.55, "V2", 9.0, "PEAK", "Hands - release"),
    (23.430, 0.50, "V6", 11.0, "PEAK", "Eyes - softening"),
    (23.930, 0.60, "V1", 10.0, "PEAK", "Crowd - memories"),
    (24.530, 0.55, "V4", 11.0, "PEAK", "Chair - symbol returns"),
    (25.080, 0.50, "V6", 11.5, "PEAK", "Eyes - peaceful"),
    (25.580, 0.60, "V3", 10.0, "PEAK", "Profile - acceptance"),
    (26.180, 0.55, "V2", 10.0, "PEAK", "Hands slowing"),
    (26.730, 0.65, "V6", 12.0, "PEAK", "Eyes - longer"),
    (27.380, 0.70, "V1", 11.0, "PEAK", "Crowd fading"),
    (28.080, 0.75, "V4", 12.0, "PEAK", "Chair - settling"),
    (28.830, 0.65, "V6", 12.5, "PEAK", "Eyes - tender"),
    (29.480, 0.70, "V5", 5.0, "PEAK", "Silhouette - ghost"),
    (30.180, 0.75, "V3", 11.0, "PEAK", "Profile - serene"),
    (30.930, 0.80, "V2", 11.0, "PEAK", "Hands - gentle"),
    (31.730, 0.85, "V6", 13.0, "PEAK", "Eyes - accepting"),
    (32.580, 0.90, "V4", 13.0, "PEAK", "Chair - eternal"),
    (33.480, 0.81, "V5", 8.0, "PEAK", "Silhouette dissolving"),

    # ═══════════════════════════════════════════════════════════════════════════
    # ACT VII: OUTRO - "Dissolution" (34-35s)
    # ═══════════════════════════════════════════════════════════════════════════
    (34.290, 0.71, "V6", 14.0, "OUTRO", "Eyes fading - goodbye"),

    # OUTRO CARD (35-37s) handled separately
]

# =============================================================================
# MAIN RENDER PIPELINE
# =============================================================================

def process_frame_v3(frame, t, section=None):
    """
    Master frame processor with all V3 enhancements
    """
    if section is None:
        section = get_section(t)

    # Skip processing for title cards
    if section in ["INTRO", "INTRO_OUT"]:
        return frame

    # 1. Apply section-specific color grade
    frame = apply_section_grade(frame, t)

    # 2. B&W conversion with green eye isolation
    if section in ["DROP", "CLIMAX", "PEAK"]:
        # Full green eye isolation
        intensity = 1.0 if section == "CLIMAX" else 0.85
        frame = isolate_green_eyes(frame, t, intensity)
    else:
        # More subtle in other sections
        frame = isolate_green_eyes(frame, t, 0.6)

    # 3. Add halation (especially for eyes)
    if section in ["DROP", "CLIMAX"]:
        frame = add_halation(frame, threshold=0.70, radius=30, strength=0.35)
    else:
        frame = add_halation(frame, threshold=0.80, radius=20, strength=0.2)

    # 4. Add chromatic aberration
    ca_strength = 0.004 if section in ["DROP", "CLIMAX"] else 0.002
    frame = add_chromatic_aberration(frame, ca_strength)

    # 5. Add vignette
    frame = add_vignette(frame, strength=0.35, t=t)

    # 6. Add film grain
    frame = add_film_grain(frame, t=t)

    # 7. Add letterbox
    frame = add_letterbox(frame, ratio=2.39)

    return frame

def main():
    print("=" * 70)
    print("◉  С А Й М У Р Р  —  С М О Т Р Е Л А")
    print("   ULTRA-PROFESSIONAL TEASER RENDERER V3")
    print("=" * 70)
    print(f"BPM: {BPM}")
    print(f"DROP: {DROP_TIME}s | CLIMAX: {CLIMAX_TIME}s")
    print(f"Total duration: {TOTAL_DURATION}s")
    print()

    # Load video sources
    print("[1/6] Loading video sources...")
    sources = {}
    for name, path in VIDEOS.items():
        clip = VideoFileClip(path)
        sources[name] = clip
        print(f"      {name}: {clip.duration:.2f}s")

    # Create INTRO card
    print("\n[2/6] Creating INTRO card (0-4s) with САЙМУРР branding...")
    intro_card = create_intro_card(duration=4.0, size=(1920, 1080))
    print("      ◉ Symbol + САЙМУРР with green accent")

    # Build clips from EDL
    print(f"\n[3/6] Building {len(ULTIMATE_EDL)} clips from Ultimate EDL...")
    clips = []

    for i, (start, dur, src, src_start, section, desc) in enumerate(ULTIMATE_EDL):
        print(f"      [{i+1:02d}/{len(ULTIMATE_EDL)}] {section}: {desc[:40]}...")

        if src == "BLACK":
            # Black screen
            def make_black(t, d=dur):
                return np.full((1080, 1920, 3), NEAR_BLACK, dtype=np.uint8)
            clip = VideoClip(make_black, duration=dur)

        elif src == "FLASH":
            # White flash
            clip = create_white_flash(duration=dur, size=(1920, 1080))

        else:
            # Video clip with VFX
            source_clip = sources[src]
            clip = source_clip.subclipped(src_start, src_start + dur)

            # Apply V3 processing
            def process_with_section(gf, t, sec=section):
                frame = gf(t)
                return process_frame_v3(frame, start + t, sec)

            clip = clip.transform(process_with_section)

        clips.append(clip)

    # Create OUTRO card
    print("\n[4/6] Creating OUTRO card (35-37s) with full branding...")
    outro_card = create_outro_card(duration=2.0, size=(1920, 1080))
    print("      САЙМУРР + СМОТРЕЛА + look at me")

    # Concatenate all
    print("\n[5/6] Concatenating timeline...")

    # Intro (0-4s) + Main content (4-35s) + Outro (35-37s)
    main_content = concatenate_videoclips(clips, method="compose")
    print(f"      Main content duration: {main_content.duration:.2f}s")

    # Final assembly
    final_video = concatenate_videoclips([intro_card, main_content, outro_card], method="compose")
    print(f"      Total video duration: {final_video.duration:.2f}s")

    # Add audio
    print("\n[6/6] Adding audio and rendering...")
    audio = AudioFileClip(AUDIO_FILE).subclipped(0, TOTAL_DURATION)
    final_video = final_video.with_audio(audio)

    print(f"\n      Rendering to: {OUTPUT_FILE}")
    print(f"      Resolution: 1920x1080 @ 30fps")
    print(f"      This will take several minutes...")
    print()

    final_video.write_videofile(
        OUTPUT_FILE,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        bitrate="18000k",
        preset="slow",
        threads=4
    )

    # Cleanup
    for clip in sources.values():
        clip.close()

    print()
    print("=" * 70)
    print("◉  RENDER COMPLETE!")
    print(f"   Output: {OUTPUT_FILE}")
    print("=" * 70)
    print()
    print("   V3 Features:")
    print("   ✓ INTRO card with ◉ + САЙМУРР (green С)")
    print("   ✓ Cinema-level B&W + selective green eyes")
    print("   ✓ Beat-synced pulsation @ 170.5 BPM")
    print("   ✓ Film grain, chromatic aberration, halation")
    print("   ✓ Frame-perfect DROP @ 17.163s")
    print("   ✓ CLIMAX hold @ 21.451s (1.429s)")
    print("   ✓ OUTRO card with full branding")
    print("=" * 70)

if __name__ == "__main__":
    main()
